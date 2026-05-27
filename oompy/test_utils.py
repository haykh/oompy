from fractions import Fraction
from .utils import (
    add_unit,
    _is_number,
    _str_quantity_to_tuple,
    parse_fraction,
    str_quantity_to_raw,
    raw_quantity_to_str,
)

from .types import TypeRational, TypeUnit, TypeRawQuantity


def test_add_unit() -> None:
    before: list[TypeUnit] = [
        {"g": Fraction(1, 2), "cm": -2},
        {"g": 2, "cm": Fraction(1, 3)},
        {"sec": Fraction(-1)},
        {"g": Fraction(1, 2), "cm": -2},
    ]
    additions: list[tuple[str, TypeRational]] = [
        ("g", Fraction(-1, 2)),
        ("cm", Fraction(2, 3)),
        ("sec", -1),
        ("sec", -1),
    ]
    expected: list[TypeUnit] = [
        {"cm": -2},
        {"g": 2, "cm": 1},
        {"sec": -2},
        {"g": Fraction(1, 2), "cm": -2, "sec": -1},
    ]
    for b4, add, expect in zip(before, additions, expected):
        add_unit(b4, *add)
        assert (
            b4 == expect
        ), f"Expected {expect}, got {b4} after adding {add} to {before}"


def test_is_number() -> None:
    numbers = ["123", "3.14", "3.14e33", "-123", "-3.14", "-3.14e-10"]
    notnumbers = ["abc", "3.14.14", "3 14", ""]
    for num in numbers:
        assert _is_number(num), f"{num} should be a number"
    for notnum in notnumbers:
        assert not _is_number(notnum), f"{notnum} should not be a number"


def test_str_quantity_to_tuple() -> None:
    values = ["3.14 kg^2 mm^-1", "G^2 sec^-1", "-3e14 T^2", "5e3 cm^2 GG^-1"]
    expected = [
        (3.14, "kg^2 mm^-1"),
        (1.0, "G^2 sec^-1"),
        (-3e14, "T^2"),
        (5e3, "cm^2 GG^-1"),
    ]
    for val, exp in zip(values, expected):
        coeff, unit = _str_quantity_to_tuple(val)
        assert coeff == exp[0], f"Expected coefficient {exp[0]}, got {coeff}"
        assert unit == exp[1], f"Expected unit {exp[1]}, got {unit}"


def test_parse_fraction() -> None:
    values = ["3/4", "5", "10/2", "7/1", "0/5", "3.14", "2e2/3.14"]
    expected = [
        Fraction(3, 4),
        Fraction(5, 1),
        Fraction(10, 2),
        Fraction(7, 1),
        Fraction(0),
        Fraction(157, 50),
        Fraction(10000, 157),
    ]
    raises = ["3/4/5", "abc", "3//4", "3/0", "3.14/abc", "abc/3.14"]
    for val, exp in zip(values, expected):
        frac = parse_fraction(val)
        assert frac == exp, f"Expected fraction {exp}, got {frac}"
    for val in raises:
        try:
            _ = parse_fraction(val)
            assert False, f"Expected ValueError for input {val}"
        except (ValueError, ZeroDivisionError, AssertionError):
            pass


def test_str_quantity_to_raw() -> None:
    values = ["3.14 kg^2 mm^-1/2", "G^2 sec^-1", "-3e14 T^2", "5e3 cm^2/3 GG^-1"]
    expected: list[TypeRawQuantity] = [
        (3.14, {"kg": 2, "mm": Fraction(-1, 2)}),
        (1.0, {"G": 2, "sec": Fraction(-1)}),
        (-3e14, {"T": 2}),
        (5e3, {"cm": Fraction(2, 3), "GG": -1}),
    ]
    for val, exp in zip(values, expected):
        raw = str_quantity_to_raw(val)
        assert raw == exp, f"Expected raw quantity {exp}, got {raw}"


def test_raw_quantity_to_str() -> None:
    values: list[TypeRawQuantity] = [
        (3.14, {"kg": 2, "mm": Fraction(-1, 2)}),
        (1.0, {"G": 2, "sec": Fraction(-1)}),
        (-3e14, {"T": 2}),
        (5e3, {"cm": Fraction(2, 3), "GG": -1}),
    ]
    for fmt in ["", ".2f", ".4e"]:
        expected = [
            f"{3.14:{fmt}} kg^2 mm^-1/2",
            f"{1.0:{fmt}} G^2 sec^-1",
            f"{-3e14:{fmt}} T^2",
            f"{5e3:{fmt}} cm^2/3 GG^-1",
        ]
        for val, exp in zip(values, expected):
            qstr = raw_quantity_to_str(val, fmt)
            assert qstr == exp, f"Expected string {exp}, got {qstr}"


def test_JoinUnits() -> None:
    pass
