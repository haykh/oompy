import numpy as np
from fractions import Fraction
from .units import (
    unit_str_convert_from_to,
    unit_str_to_base,
    raw_quantity_to_base,
    unit_str_to_dim_dict,
    unit_dict_to_dim_dict,
    unit_dict_to_cgs_dict,
)
from .types import Dim, TypeDim, TypeUnit, TypeRawQuantity


def test_unit_str_convert_from_to() -> None:
    values = [
        ("km", "m"),
        ("kin", "Myd"),
        ("kcal", "g cm^2 sec^-2"),
        ("erg yr^-1", "W"),
    ]
    expect = [1e3, 27.7778e-6, 4.184e10, 3.17098e-15]
    for val, exp in zip(values, expect):
        conversion = unit_str_convert_from_to(*val)
        assert np.isclose(
            float(conversion), float(exp)
        ), f"Expected {exp}, got {conversion} for {val[0]} to {val[1]}"


def test_unit_to_base() -> None:
    values = [
        "kmi Mhr^-1",
        "kg^2 mm^-1/2",
        "GG",
    ]
    expect: list[TypeRawQuantity] = [
        (447.04 / 1e6, {"m": 1, "sec": -1}),
        (1e7 * np.sqrt(10), {"g": 2, "m": Fraction(-1, 2)}),
        (1e10, {"g": Fraction(1, 2), "m": Fraction(-1, 2), "sec": -1}),
    ]
    for val, exp in zip(values, expect):
        value, unit_dict = unit_str_to_base(val)
        assert unit_dict == exp[1], f"Expected unit {exp[1]}, got {unit_dict}"
        assert np.isclose(
            float(value), float(exp[0])
        ), f"Expected coefficient {exp[0]}, got {value}"


def test_raw_quantity_to_base() -> None:
    values: list[TypeRawQuantity] = [
        (2.0, {"kmi": 1, "Mhr": -1}),
        (3.0, {"kg": 2, "mm": Fraction(-1, 2)}),
        (4.0, {"GG": 1}),
    ]
    expect: list[TypeRawQuantity] = [
        (2 * 447.04 / 1e6, {"m": 1, "sec": -1}),
        (3e7 * np.sqrt(10), {"g": 2, "m": Fraction(-1, 2)}),
        (4e10, {"g": Fraction(1, 2), "m": Fraction(-1, 2), "sec": -1}),
    ]
    for val, exp in zip(values, expect):
        value, unit_dict = raw_quantity_to_base(val)
        assert unit_dict == exp[1], f"Expected unit {exp[1]}, got {unit_dict}"
        assert np.isclose(
            float(value), float(exp[0])
        ), f"Expected coefficient {exp[0]}, got {value}"


def test_unit_dict_to_dim_dict() -> None:
    values: list[TypeUnit] = [
        {"kmi": 1, "Mhr": -1},
        {"kg": 2, "mm": Fraction(-1, 2)},
        {"GG": 1},
    ]
    expected: list[TypeDim] = [
        {Dim.LENGTH: 1, Dim.TIME: -1},
        {Dim.MASS: 2, Dim.LENGTH: Fraction(-1, 2)},
        {Dim.MASS: Fraction(1, 2), Dim.LENGTH: Fraction(-1, 2), Dim.TIME: -1},
    ]
    for val, exp in zip(values, expected):
        result = unit_dict_to_dim_dict(val)
        assert result == exp, f"Expected {exp}, got {result} for {val}"


def test_unit_str_to_dim_dict() -> None:
    values: list[str] = [
        "kmi Mhr^-1",
        "kg^2 mm^-1/2",
        "GG",
    ]
    expected: list[TypeDim] = [
        {Dim.LENGTH: 1, Dim.TIME: -1},
        {Dim.MASS: 2, Dim.LENGTH: Fraction(-1, 2)},
        {Dim.MASS: Fraction(1, 2), Dim.LENGTH: Fraction(-1, 2), Dim.TIME: -1},
    ]
    for val, exp in zip(values, expected):
        result = unit_str_to_dim_dict(val)
        assert result == exp, f"Expected {exp}, got {result} for {val}"


def test_unit_dict_to_cgs_dict() -> None:
    values: list[TypeUnit] = [
        {"kmi": 1, "Mhr": -1},
        {"kG": 1},
    ]
    expected: list[TypeRawQuantity] = [
        (0.044704, {"cm": 1, "sec": -1}),
        (1e3, {"g": Fraction(1, 2), "cm": Fraction(-1, 2), "sec": -1}),
    ]
    for val, exp in zip(values, expected):
        result = unit_dict_to_cgs_dict(val)
        assert result[0] == exp[0], f"Expected {exp[0]}, got {result[0]} for {val}"
        assert result[1] == exp[1], f"Expected {exp[1]}, got {result[1]} for {val}"
