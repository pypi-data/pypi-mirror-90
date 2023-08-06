from abc import ABC
from typing import Protocol, List, Any, Generator, Union, Iterable, Literal, Callable
from torch.utils.data.dataloader import DataLoader
from torch.optim.optimizer import Optimizer
import torch
from logging import Logger
from .base import Transferable, SaveDelegate
from typing import Optional

import random

MODE = Literal['eval', 'train']
SAVED_SUFFIX = Literal['_best', '_latest']
TEST_CHOICES = Literal['best', 'latest']


class LoggerMixin:
    logger: Optional[Logger] = None
    log: Callable
    warn: Callable
    critical: Callable
    debug: Callable

    def configure_logger(self, _logger: Logger):
        self.logger = _logger
        self.log = _logger.info
        self.warn = _logger.warning
        self.critical = _logger.critical
        self.debug = _logger.debug


class KahtDataModule:
    is_prepared: bool = False

    def prepare(self):
        raise NotImplementedError

    def train_dataloader(self, *args, **kwargs) -> Generator[Transferable, None, None]:
        raise NotImplementedError

    def test_dataloader(self) -> Iterable: ...

    def valid_dataloader(self) -> Iterable[Transferable]: ...


class ModuleMixIn:
    # logger: Logger
    # log: Callable
    # warn: Callable
    # critical: Callable
    # debug: Callable
    mode: MODE

    save_delegate: SaveDelegate

    def will_train(self, *args, **kwargs): ...

    def on_train_one_step_start(self, logger: Logger): ...

    def train_one_step(self, batch) -> torch.Tensor:
        raise NotImplementedError

    def configure_optimizer(self) -> Union[Optimizer, List[Optimizer]]: ...

    def train_steps_end(self, outputs: List[Any]): ...

    def on_train_end(self): ...

    def will_test(self, *args, **kwargs): ...

    def test_one_task(self, batch): ...

    def on_test_end(self, outpus: List[Any]): ...

    def will_valid(self, *args, **kwargs): ...

    def valid_one_task(self, batch) -> Any: ...

    def on_valid_end(self, outpus: List[Any]): ...

    def params_for_clip(self): ...

    def report_every(self, losses: Iterable): ...

    def save(self, suffix: SAVED_SUFFIX, *args):
        """ Save and return saved result.
        :param suffix:
        :return:
        """
        raise NotImplementedError

    @property
    def training(self) -> bool:
        return self.mode == 'train'

    def switch(self, mode: MODE):
        raise NotImplementedError


class KahtModule(torch.nn.Module, LoggerMixin):
    mode: MODE

    save_delegate: SaveDelegate

    # set true if backward in module; else backward in trainer
    manual_backward: bool = False

    trainer = None

    def will_train(self, *args, **kwargs):
        ...

    def on_train_one_step_start(self, logger: Logger):
        ...

    def sanity_train_one_step(self, batch) -> torch.Tensor:
        return self.train_one_step(batch)

    def train_one_step(self, task_batch) -> torch.Tensor:
        raise NotImplementedError

    def configure_optimizer(self) -> Union[Optimizer, List[Optimizer]]:
        raise NotImplementedError

    def train_steps_end(self, outputs: List[Any]):
        ...

    def on_train_end(self):
        ...

    def will_test(self, *args, **kwargs):
        ...

    def test_one_task(self, batch):
        ...

    def on_test_end(self, outpus: list[Any]):
        ...

    def will_valid(self, *args, **kwargs):
        ...

    def valid_one_task(self, batch) -> Any:
        ...

    def on_valid_end(self, outpus: List[Any]):
        ...

    def params_for_clip(self):
        parameters = filter(lambda p: p.requires_grad, self.parameters())
        return parameters

    def report_every(self, losses: Iterable):
        ...

    model_name: str = 'KahtModule'
    _current_epoch: int = 0

    def next(self):
        pass

    def __init__(self):
        super(KahtModule, self).__init__()

    @property
    def current_epoch(self):
        return self.trainer.current_step

    def switch(self, mode: MODE):
        if mode == 'eval':
            self.eval()
        elif mode == 'train':
            self.train()

    def save_checkpoint(self, filename: str):
        torch.save(self, filename)

    def save(self, suffix: SAVED_SUFFIX, /, others: str = ''):
        filename = f"{self.model_name}_STEP{self.current_epoch}_{others}_{suffix}.ckpt"
        self.save_checkpoint(filename)
        self.save_delegate.on_save(filename)
