from typing import Protocol
from torch import device
import torch
import random


class Transferable:
    def to(self, gpu: torch.device):
        for k, v in vars(self).items():
            if isinstance(v, torch.Tensor):
                setattr(self, k, v.to(gpu))
            elif isinstance(v, list):
                _i = random.choice(v)
                if isinstance(_i, int):
                    setattr(self, k, torch.tensor(v, device=gpu))
            else:
                continue


class SaveDelegate(Protocol):
    def on_save(self, *args):
        ...
