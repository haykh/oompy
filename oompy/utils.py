from fractions import Fraction

from .types import TypeRational, TypeNumeric, TypeUnit, TypeRawQuantity


def add_unit(unit_dict: TypeUnit, newunit_str: str, newunit_pow: TypeRational) -> None:
    """Adds a unit with its power to a dictionary inplace, or updates it if it already exists.
    If the value becomes zero, it is removed from the dictionary.

    Parameters
    ----------
    unit_dict : TypeUnit
        The dictionary to update, which maps unit names to their powers.

    newunit_str : str
        The unit name to add or update in the dictionary.

    newunit_pow : TypeRational
        The power of the unit to add or update in the dictionary. This can be a Fraction or a numeric type.
    """
    if newunit_str not in unit_dict:
        unit_dict.update({newunit_str: newunit_pow})
    else:
        unit_dict[newunit_str] += newunit_pow
    if unit_dict[newunit_str] == 0:
        del unit_dict[newunit_str]


def _is_number(s: str) -> bool:
    """Checks if a string can be converted to a float."""
    try:
        _ = float(s)
        return True
    except ValueError:
        return False


def _str_quantity_to_tuple(quant_str: str) -> tuple[TypeNumeric, str]:
    """Converts a string of raw dimensional quantity to a tuple of value + unit.

    Parameters
    ----------
    quant_str : str
        The unit string to strip the coefficient from. For example, "3.14 m^2 sec^-1".

    Returns
    -------
    tuple[TypeNumeric, str]
        A tuple containing the coefficient as a float and the unit string without the coefficient.
        For example, (3.14, "m^2 sec^-1").
    """
    quant_splitted: list[str] = quant_str.split(" ")
    if len(quant_splitted) > 1:
        if _is_number(quant_splitted[0]):
            return float(quant_splitted[0]), " ".join(quant_splitted[1:])
    return 1.0, quant_str


def parse_fraction(frac: str) -> Fraction:
    """Parses a string into a Fraction object.

    Parameters
    ----------
    frac : str
        The string to parse. It can be a simple fraction like "1/2" or just a number like "3".

    Returns
    -------
    Fraction
        A Fraction object representing the parsed value. If the string is just a number, it returns
        that number as a fraction with a denominator of 1.

    Raises
    ------
    ValueError
        If more than one '/' is present or if the format is invalid.

    ZeroDivisionError
        If the denominator is zero.

    AssertionError
        If the parts of the fraction are not valid numbers.
    """
    splitted: list[str] = frac.split("/")
    if len(splitted) == 1:
        assert _is_number(frac), f"Invalid fraction format: {frac}"
        return Fraction(frac)
    elif len(splitted) == 2:
        assert _is_number(splitted[0]) and _is_number(
            splitted[1]
        ), f"Invalid fraction format: {frac}"
        if float(splitted[1]) == 0:
            raise ZeroDivisionError
        return Fraction(Fraction(splitted[0]), Fraction(splitted[1]))
    else:
        raise ValueError(f"Invalid fraction format: {frac}")


def str_quantity_to_raw(quant_str: str) -> TypeRawQuantity:
    """Converts a string quantity to a raw one, tuple with coefficient and unit dictionary.

    Parameters
    ----------
    quant_str : str
        The string to convert, e.g. "3.14 m^2 sec^-1/2".

    Returns
    -------
    TypeRawQuantity
        A tuple containing the coefficient as a float and a dictionary of units with their powers.
        For example, (3.14, {"m": 2, "sec": Fraction(-1, 2)}).
    """
    coeff, unit_str = _str_quantity_to_tuple(quant_str)
    unit_dict: TypeUnit = {}
    for u in unit_str.split(" "):
        pwr = (
            parse_fraction(u.split("^")[1]) if len(u.split("^")) > 1 else Fraction(1, 1)
        )
        unit = u.split("^")[0]
        add_unit(unit_dict, unit, pwr if unit != "" else Fraction(0, 1))
    return coeff, unit_dict


def raw_quantity_to_str(quant: TypeRawQuantity, fmt: str = "") -> str:
    """Converts a raw quantity (coefficient and unit dictionary) to a string representation.

    Parameters
    ----------
    quant : TypeRawQuantity
        The raw quantity to convert, e.g. (3.14, {"m": 2, "sec": Fraction(-1, 2)}).

    fmt : str, optional
        The format string for the coefficient, by default "" -- no formatting. Use "%H" for human-readable format.

    Returns
    -------
    str
        A string representation of the raw quantity, e.g. "3.14 m^2 sec^-1/2".
    """
    coeff, unit_dict = quant

    # @TODO: implement human-readable format
    unit_str = " ".join(
        f"{unit}^{pwr}" if pwr != 1 else unit for unit, pwr in unit_dict.items()
    )
    return f"{coeff:{fmt}} {unit_str}".strip()


def str_unit_to_dict(unit_str: str) -> TypeUnit:
    """Converts a string of units to a dictionary of units with their powers.

    Parameters
    ----------
    unit_str : str
        The unit string to convert. For example, "m^2 sec^-1".

    Returns
    -------
    TypeUnit
        A dictionary mapping unit names to their powers. For example, {"m": 2, "sec": -1}.
    """
    _, unit_dict = str_quantity_to_raw(unit_str)
    return unit_dict


# def JoinUnits(unit: str) -> str:
#     return Stringize(ParseUnit(unit))
