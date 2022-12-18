from enum import Enum
from fractions import Fraction
from typing import Union, Dict, Tuple

from .utils import addOrAppend, Stringize, ParseUnit, StripCoeff

Powers = {
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


class Type(Enum):
    DIMENSIONLESS = 0
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


CGSUnits = {
    Type.DIMENSIONLESS: "",
    Type.LENGTH: "cm",
    Type.TIME: "sec",
    Type.MASS: "g",
    Type.TEMPERATURE: "K",
    Type.INFORMATION: "bit",
    Type.ANGLE: "rad",
}

BaseUnits = {
    Type.DIMENSIONLESS: "",
    Type.LENGTH: "m",
    Type.TIME: "sec",
    Type.MASS: "g",
    Type.TEMPERATURE: "K",
    Type.INFORMATION: "bit",
    Type.ANGLE: "rad",
}

UnitEquivalencies = {
    # length
    "ft": (0.3048, "m"),
    "in": (0.0254, "m"),
    "yd": (0.9144, "m"),
    "mi": (1609.344, "m"),
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
    # charge
    "statC": (1.0, "cm^3/2 g^1/2 sec^-1"),
    # information
    "B": (8, "bit"),
    # frequency
    "Hz": (1.0, "sec^-1"),
    # angle
    "deg": (0.017453292519943295, "rad"),
}


def ReduceUnitToBase(unit: str = "") -> str:
    coeff, factorized = ParseUnit(unit)
    newunits = {}  # type: dict[str, Fraction]
    for u, p in factorized.items():
        if u in BaseUnits.values():
            addOrAppend(newunits, u, p)
        elif u in UnitEquivalencies.keys():
            eq_c, eq_u = UnitEquivalencies[u]
            eq_str = Stringize((eq_c, eq_u))
            eq_base = ReduceUnitToBase(eq_str)
            nc, nu = ParseUnit(eq_base)
            for u2, p2 in nu.items():
                addOrAppend(newunits, u2, p * p2)
            coeff *= nc**p
        elif u[1:] in BaseUnits.values() and u[0] in Powers.keys() and u[1:] != "":
            addOrAppend(newunits, u[1:], p)
            coeff *= Powers[u[0]] ** p
        elif (
            u[1:] in UnitEquivalencies.keys() and u[0] in Powers.keys() and u[1:] != ""
        ):
            eq_c, eq_u = UnitEquivalencies[u[1:]]
            eq_str = Stringize((eq_c, eq_u))
            eq_base = ReduceUnitToBase(eq_str)
            nc, nu = ParseUnit(eq_base)
            for u2, p2 in nu.items():
                addOrAppend(newunits, u2, p * p2)
            coeff *= nc**p * Powers[u[0]] ** p
        else:
            raise Exception(f"Invalid unit: {u}")
    return Stringize((coeff, newunits))


def GetBaseType(unit: str = "") -> Dict["Type", "Fraction"]:
    _, factorized = ParseUnit(ReduceUnitToBase(unit))
    newf = {}
    for f in factorized.keys():
        for k, v in BaseUnits.items():
            if f == v:
                newf[k] = factorized[f]
                break
    assert len(newf) == len(factorized), "Wrong base type inferrence"
    if len(newf) > 1:
        for f2 in newf.keys():
            if f2 == Type.DIMENSIONLESS:
                newf.pop(f2)
                break
    return newf


def RaiseUnitsToPower(unit: str, pwr: Union[int, float, Fraction]) -> str:
    pwr = Fraction(pwr).limit_denominator(1000000)
    c, u = ParseUnit(unit)
    return Stringize(
        (c**pwr, Stringize({b: Fraction(Fraction(pwr) * p) for b, p in u.items()}))
    )


def ConvertUnit(src: str, dst: str) -> Tuple[float, str]:
    assert GetBaseType(src) == GetBaseType(
        dst
    ), "Cannot convert between different base types"
    _, dst_u = StripCoeff(dst)
    red_src = ReduceUnitToBase(src)
    red_dst = ReduceUnitToBase(dst)
    c1, _ = StripCoeff(red_src)
    c2, _ = StripCoeff(red_dst)
    return c1 / c2, dst_u
