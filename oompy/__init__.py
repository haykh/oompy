__version__ = "1.4.0"

from .oom import UnitsClass, ConstantsClass, Quantity, Assumptions

Units = UnitsClass()
Constants = ConstantsClass()

__all__ = ["Quantity", "Units", "Constants", "Assumptions", "Utils"]

from pkg_resources import get_distribution, DistributionNotFound

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
