from .types import Dim, TypeDim, TypeRational, TypeNumeric, TypeRawQuantity, TypeUnit
from .utils import add_unit, raw_quantity_to_str, str_quantity_to_raw, str_unit_to_dict

# from typing import Union, Dict, Tuple

# from .utils import addOrAppend, Stringize, ParseUnit, StripCoeff

Powers: dict[str, float] = {
    "y": 1e-24,
    "z": 1e-21,
    "a": 1e-18,
    "f": 1e-15,
    "p": 1e-12,
    "n": 1e-9,
    "u": 1e-6,
    "m": 1e-3,
    "c": 1e-2,
    "d": 1e-1,
    "k": 1e3,
    "M": 1e6,
    "G": 1e9,
    "T": 1e12,
    "P": 1e15,
    "E": 1e18,
    "Z": 1e21,
    "Y": 1e24,
}


CGSUnits: dict[Dim, str] = {
    Dim.NONE: "",
    Dim.LENGTH: "cm",
    Dim.TIME: "sec",
    Dim.MASS: "g",
    Dim.TEMPERATURE: "K",
    Dim.INFORMATION: "bit",
    Dim.ANGLE: "rad",
}

BaseUnits: dict[Dim, str] = {
    Dim.NONE: "",
    Dim.LENGTH: "m",
    Dim.TIME: "sec",
    Dim.MASS: "g",
    Dim.TEMPERATURE: "K",
    Dim.INFORMATION: "bit",
    Dim.ANGLE: "rad",
}

UnitEquivalencies: dict[str, tuple[float, str]] = {
    # length
    "ft": (0.3048, "m"),
    "in": (0.0254, "m"),
    "yd": (0.9144, "m"),
    "mi": (1609.344, "m"),
    "Nmi": (1852, "m"),
    "fathom": (6, "ft"),
    "Rsun": (695700, "km"),
    "au": (149597870700.0, "m"),
    "ly": (9460730472580800.0, "m"),
    "pc": (3.085677581491362e16, "m"),
    # time
    "day": (86400.0, "sec"),
    "yr": (31557600.0, "sec"),
    "month": (30.436875 * 24 * 60 * 60, "sec"),
    "min": (60.0, "sec"),
    "hr": (3600.0, "sec"),
    # mass
    "me": (9.109383701528e-28, "g"),
    "Msun": (1.98847e33, "g"),
    "lb": (453.5924, "g"),
    # velocity
    "knot": (1.852, "km hr^-1"),
    # force
    "N": (1, "kg m sec^-2"),
    "dyn": (1e-5, "N"),
    # energy
    "erg": (1.0, "g cm^2 sec^-2"),
    "eV": (1.602177e-12, "erg"),
    "J": (1.0, "kg m^2 sec^-2"),
    "cal": (4.184e7, "erg"),
    # power
    "hp": (7456998715.8, "erg sec^-1"),
    "W": (1e7, "erg sec^-1"),
    # magnetic field
    "G": (1.0, "erg^1/2 cm^-3/2"),
    "T": (1e4, "G"),
    # charge
    "statC": (1.0, "cm^3/2 g^1/2 sec^-1"),
    "qe": (4.80320427e-10, "statC"),
    "C": (2997924580.0, "statC"),
    # current
    "A": (1.0, "C sec^-1"),
    # information
    "B": (8, "bit"),
    # frequency
    "Hz": (1.0, "sec^-1"),
    # angle
    "deg": (0.017453292519943295, "rad"),
    "arcsec": (4.84813681109536e-06, "rad"),
    "arcmin": (0.0002908882086657216, "rad"),
}

LatexUnitMapping: dict[str, str] = {
    "Msun": "M_\\bigodot",
    "Rsun": "R_\\bigodot",
    "me": "m_e",
    "au": "AU",
    "sec": "s",
}


def unit_str_convert_from_to(unit_to: str, unit_from: str) -> TypeNumeric:
    """Converts a unit from one to another using either the UnitEquivalencies dictionary, or the powers of 10 prefixes.

    Parameters
    ----------
    unit_to : str
        The unit to convert to, e.g. "m".

    unit_from : str
        The unit to convert from, e.g. "km".

    Returns
    -------
    TypeNumeric
        The conversion factor from the unit_from to the unit_to. E.g., 1000.0 for "km" to "m".

    Raises
    ------
    AssertionError
        When units do not match.
    """
    base_unit_to = unit_str_to_base(unit_to)
    base_unit_from = unit_str_to_base(unit_from)
    assert (
        base_unit_to[1] == base_unit_from[1]
    ), "Units do not have the same base dimension"
    return base_unit_to[0] / base_unit_from[0]


def raw_quantity_to_base(quant: TypeRawQuantity) -> TypeRawQuantity:
    """Converts a raw quantity (coefficient and unit dictionary) to its base unit representation.

    Parameters
    ----------
    quant : TypeRawQuantity
        The raw quantity to convert, e.g. (1.0, {"kg": 2, "mm": Fraction(-1, 2)}).

    Returns
    -------
    TypeRawQuantity
        A tuple containing the coefficient as a float and a dictionary of base units with their powers.
        For example, (3.16e7, {"g": 2, "m": Fraction(-1, 2)}).
    """
    value: TypeNumeric = quant[0]
    unit_dict: TypeUnit = quant[1]

    # check if all base units
    if all(unit in BaseUnits.values() for unit in unit_dict):
        return quant

    newvalue: TypeNumeric = value
    newunit_dict: TypeUnit = {}
    for unit, power in unit_dict.items():
        if unit in BaseUnits.values():
            add_unit(newunit_dict, unit, power)
        elif unit in UnitEquivalencies.keys():
            # unit conversion necessary
            eq_val, eq_unit_str = UnitEquivalencies[unit]
            eq_unit_dict = str_unit_to_dict(eq_unit_str)
            for eq_unit, eq_power in eq_unit_dict.items():
                add_unit(newunit_dict, eq_unit, power * eq_power)
            newvalue *= eq_val**power
        elif (
            unit[1:] in BaseUnits.values() or unit[1:] in UnitEquivalencies.keys()
        ) and (unit[0] in Powers):
            # power-of-10 prefix
            prefix = Powers[unit[0]]
            add_unit(newunit_dict, unit[1:], power)
            newvalue *= prefix**power

    return raw_quantity_to_base((newvalue, newunit_dict))


def unit_str_to_base(unit_str: str) -> TypeRawQuantity:
    """Converts a unit string to its base unit representation.

    Parameters
    ----------
    unit_str : str
        The unit string to convert, e.g. "kg^2 mm^-1/2".

    Returns
    -------
    TypeRawQuantity
        A tuple containing the coefficient as a float and a dictionary of base units with their powers.
        For example, (3.16e7, {"g": 2, "m": Fraction(-1, 2)}).
    """
    return raw_quantity_to_base(str_quantity_to_raw(unit_str))


def unit_dict_to_dim_dict(unit_dict: TypeUnit) -> TypeDim:
    """Converts a unit dictionary to a dictionary of base types with their powers.

    Parameters
    ----------
    unit_dict : TypeUnit
        The unit dictionary to convert, e.g. {"kg": 2, "mm": Fraction(-1, 2)}.

    Returns
    -------
    TypeDim
        A dictionary where keys are Dim enums and values are their powers as TypeRational.
        For example, {Dim.MASS: 2, Dim.LENGTH: Fraction(-1, 2)}.
    """
    base_unit_dict: TypeUnit = raw_quantity_to_base((1.0, unit_dict))[1]
    newf: dict[Dim, TypeRational] = {}
    for f, power in base_unit_dict.items():
        for k, v in BaseUnits.items():
            if f == v:
                newf[k] = power
                break
    assert len(newf) == len(base_unit_dict), "Wrong base type inferrence"
    if len(newf) > 1:
        for f2 in newf.keys():
            if f2 == Dim.NONE:
                del newf[f2]
                break
    return newf


def unit_dict_to_cgs_dict(unit_dict: TypeUnit) -> TypeRawQuantity:
    """Converts a unit dictionary to a CGS unit dictionary.

    Parameters
    ----------
    unit_dict : TypeUnit
        The unit dictionary to convert, e.g. {"kg": 2, "mm": Fraction(-1, 2)}.

    Returns
    -------
    TypeRawQuantity
        A tuple containing the coefficient as a float and a dictionary of CGS units with their powers.
        For example, (3.16e6, {"g": 2, "cm": Fraction(-1, 2)}).
    """
    base_quant = raw_quantity_to_base((1.0, unit_dict))
    base_value, base_unit_dict = base_quant
    cgs_value = base_value
    cgs_unit_dict: TypeUnit = {}
    for unit, pow in base_unit_dict.items():
        assert unit in BaseUnits.values(), f"Unit {unit} not in base units"
        cgs_unit: str | None = None
        for d, u in BaseUnits.items():
            if u == unit:
                cgs_unit = CGSUnits[d]
                break
        assert cgs_unit is not None, "corresponding CGS unit was not found"
        conversion = unit_str_convert_from_to(unit, cgs_unit)
        cgs_value *= conversion**pow
        cgs_unit_dict[cgs_unit] = pow
    return (cgs_value, cgs_unit_dict)


def unit_str_to_dim_dict(unit_str: str) -> TypeDim:
    """Converts a unit string to a dictionary of base types with their powers.

    Parameters
    ----------
    unit_str : str
        The unit string to convert, e.g. "kg^2 mm^-1/2".

    Returns
    -------
    TypeDim
        A dictionary where keys are Dim enums and values are their powers as TypeRational.
        For example, {Dim.MASS: 2, Dim.LENGTH: Fraction(-1, 2)}.
    """
    base_quant = unit_str_to_base(unit_str)
    return unit_dict_to_dim_dict(base_quant[1])
