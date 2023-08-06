from typing import Union

from tap import Tap
import torch
from torch import nn
from torch.optim.optimizer import Optimizer
from .model import KahtModule, KahtDataModule
from .model import ModuleMixIn
from .logger import Logger
import os, sys
from .base import SaveDelegate
from collections import deque
import numpy
import numpy as np
import random
from tqdm import tqdm


class KahtTap(Tap):
    debug: bool = False
    min_steps: int = 1
    max_steps: int = 1
    valid_interval: int = 1
    report_interal: int = 50
    grad_clip: float = -1.0
    log_dir: str = 'logs/'
    log_file: str = '/dev/null'  # custom your log file
    gpu: int = -1
    seed: int = 8964
    accumulated_steps: int = 1
    no_sanity: bool = False

    @property
    def device(self):
        return torch.device(
                f"cuda:{self.gpu}" if self.gpu >= 0 and torch.cuda.is_available() else 'cpu')


class Trainer(SaveDelegate):
    module: KahtModule
    data_module: KahtDataModule

    def __init__(self, config: KahtTap):

        if not os.path.exists(os.path.join('.', config.log_dir)):
            os.mkdir(os.path.join('.', config.log_dir))
        self.min_steps = config.min_steps
        self.max_steps = config.max_steps
        self.current_step: int = 0
        self.valid_every = config.valid_interval
        self.report_every = config.report_interal
        self.device = config.device
        self.grad_clip = config.grad_clip
        self.logger = Logger.shared(filename=os.path.join(config.log_dir, config.log_file))
        self.saved_models = list()
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.log = self.logger.info
        self.critical = self.logger.critical
        self.accumulated_steps = config.accumulated_steps
        self.seed_everything(config.seed)
        self.debug = config.debug
        self.forward_steps = 0
        self.backward_steps = 0
        self.no_sanity = config.no_sanity

    def on_save(self, *args):
        for name in args:
            self.saved_models.append(name)

    def seed_everything(self, seed=8964):
        random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def run_sanity_check(self, module: KahtModule, data_module: KahtDataModule):
        # todo: all zero and all one check
        count = 0
        module.to(self.device)
        module.eval()
        self.info("Training Stage CHECK...")
        losses = deque([], self.report_every)
        pbar = tqdm(range(self.report_every))
        train_generator = data_module.train_dataloader()
        for _ in pbar:
            pbar.set_description(f"Sanity Epoch {_}")
            batch = next(train_generator)
            batch.to(self.device)
            loss = module.sanity_train_one_step(batch)
            losses.append(loss.detach().cpu().numpy())
        # test valid
        self.info(f"Training check ended with loss {numpy.mean(losses):.6f}")
        val_outputs = list()
        self.info("Valid Check...")
        for batch in tqdm(data_module.valid_dataloader(), desc="Val Sanity: "):
            batch.to(self.device)
            out = module.valid_one_task(batch)
            val_outputs.append(out)
        module.on_valid_end(val_outputs)
        module.train()
        self.logger.info("Sanity Check PASS")

    def backward(self, optimizers: Union[Optimizer, list[Optimizer]]):
        if isinstance(optimizers, list):
            if self.grad_clip > 0:
                nn.utils.clip_grad_norm_(self.module.params_for_clip(), self.grad_clip)
            for optim in optimizers:
                assert isinstance(optim, Optimizer)
                optim.step()
                optim.zero_grad()
        elif isinstance(optimizers, Optimizer):
            if self.grad_clip > 0:
                nn.utils.clip_grad_norm_(self.module.params_for_clip(), self.grad_clip)
            optimizers.step()
            optimizers.zero_grad()
        else:
            raise ValueError(f"NOT SUPPORT OPTIM TYPE, support List[Optim] or Optim, GET"
                             f" {type(optimizers)}")

    def train(self, module: KahtModule, data_module: KahtDataModule):
        ...

    def fit(self,
            module: KahtModule,
            data_module: KahtDataModule,
            end_with_test: bool = False):
        try:
            self.module = module
            self.data_module = data_module
            if not self.data_module.is_prepared:
                self.data_module.prepare()
            module.save_delegate = self
            module.trainer = self
            module.configure_logger(self.logger)
            if not self.no_sanity:
                self.log("START SANITY CHECK...")
                self.run_sanity_check(module=module, data_module=data_module)
            else:
                self.log("No SANITY CHECK. JUST TRAINING...")
            if self.debug:
                return
            module.to(self.device)
            module.will_train()
            module.zero_grad()
            optimizers = module.configure_optimizer()
            losses = deque([], self.report_every)
            self.info("START TRAINING...")
            steps_for_accumulated = 0
            train_generator = data_module.train_dataloader()
            while self.current_step < self.max_steps:
                # training
                pbar = tqdm(range(self.report_every))
                for _ in pbar:
                    pbar.set_description(f"Epoch {self.current_step+1}")
                    batch = next(train_generator)
                    if not module.training:
                        module.train()
                    batch.to(self.device)
                    module.on_train_one_step_start(self.logger)
                    model_loss = module.train_one_step(batch)
                    steps_for_accumulated += 1
                    if module.manual_backward:
                        loss = model_loss
                    else:
                        loss = model_loss / self.accumulated_steps
                        loss.backward()
                    loss_data = loss.cpu().item()
                    losses.append(loss_data)
                    pbar.set_postfix({'loss': f"{loss_data:.6f}",
                                      "acc_steps": steps_for_accumulated})
                    if steps_for_accumulated == self.accumulated_steps:
                        # backward
                        if isinstance(optimizers, list):
                            if self.grad_clip > 0:
                                nn.utils.clip_grad_norm_(self.module.params_for_clip(),
                                                         self.grad_clip)
                            for optim in optimizers:
                                assert isinstance(optim, Optimizer)
                                optim.step()
                                optim.zero_grad()
                        elif isinstance(optimizers, Optimizer):
                            if self.grad_clip > 0:
                                nn.utils.clip_grad_norm_(self.module.params_for_clip(),
                                                         self.grad_clip)
                            optimizers.step()
                            optimizers.zero_grad()
                        else:
                            raise ValueError(
                                f"NOT SUPPORT OPTIM TYPE, support List[Optim] or Optim, GET"
                                f" {type(optimizers)}")
                        steps_for_accumulated = 0
                    self.current_step += 1
                # report
                module.report_every(losses=losses)
                # valid
                if self.current_step % self.valid_every == 0:
                    module.eval()
                    self.logger.info(f"Valid after {self.current_step+1} steps...")
                    val_outputs = list()
                    for test_batch in data_module.valid_dataloader():
                        module.will_valid()
                        test_batch.to(self.device)
                        output = module.valid_one_task(test_batch)
                        val_outputs.append(output)
                    module.on_valid_end(val_outputs)
            self.logger.critical("END TRAINING.")
            module.save('_latest')
            if end_with_test:
                module.switch('eval')
                self.logger.info("Testing after train end...")
                test_outputs = list()
                for test_batch in data_module.test_dataloader():
                    module.will_test()
                    test_batch.to(self.device)
                    output = module.test_one_task(test_batch)
                    test_outputs.append(output)
                module.on_valid_end(test_outputs)
            module.on_train_end()

        except KeyboardInterrupt:
            self.info("Detect Keyboard Interrupt. Exit.")
            sys.exit(0)

    def summary(self):
        self.info("Training Stage Summary...")
        self.info(f"Current Epoch {self.current_step}")
