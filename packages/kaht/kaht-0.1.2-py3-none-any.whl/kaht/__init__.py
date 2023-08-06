from .model import ModuleMixIn, KahtDataModule, KahtModule
from .base import SaveDelegate, Transferable
from .metrics import KGLPMetrics, perform_metrics
from .trainer import KahtTap, Trainer

__version__ = '0.1.2'


@property
def version():
    return __version__


del metrics

__all__ = ['Trainer', 'KahtTap', 'ModuleMixIn', 'KahtModule', 'KahtDataModule',
           'KGLPMetrics',
           'perform_metrics', 'SaveDelegate', 'Transferable', '__version__']
