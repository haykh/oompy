from typing import Any, get_args
from enum import Enum
from fractions import Fraction

# str_quantity == "3.14 cm^2 g^-1/2"
# raw_quantity == ( 3.14, { "cm", Fraction(2, 1), "g", Fraction(-1, 2) } )


class Dim(Enum):
    NONE = 0
    LENGTH = 1
    TIME = 2
    MASS = 3
    B_FIELD = 4
    CHARGE = 5
    SPEED = 6
    ENERGY = 7
    FORCE = 8
    ACCELERATION = 9
    INFORMATION = 10
    TEMPERATURE = 11
    ANGLE = 12


type TypeRational = int | Fraction
type TypeNumeric = TypeRational | float
type TypeUnit = dict[str, TypeRational]
type TypeDim = dict[Dim, TypeRational]
type TypeRawQuantity = tuple[TypeNumeric, TypeUnit]

type TypeConvertibleToQuantity = TypeRawQuantity | str | tuple[
    TypeNumeric, str
] | TypeNumeric | TypeUnit


def isinstance_of(a: Any, typ: Any) -> bool:
    """
    Check if `a` is an instance of the given typing-based type (e.g., int | float | None).

    This unwraps Union types and handles None correctly.
    """
    types: tuple[type, ...] = tuple(t for t in get_args(typ) if t is not type(None))
    return isinstance(a, types) or a is None
