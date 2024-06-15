__version__ = "2.0.1"

from .oom import UnitsClass, ConstantsClass, Quantity, Assumptions, MplUnitConverter

Units = UnitsClass()
Constants = ConstantsClass()

__all__ = ["Quantity", "Units", "Constants", "Assumptions", "Utils", "MplUnitConverter"]


def matplotlib_support():
    import matplotlib.units as units

    units.registry[Quantity] = MplUnitConverter()
