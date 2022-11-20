from enum import Enum
from fractions import Fraction
from typing import Union

def addOrAppend(dct, ky, vl): return dct.update(
        {ky: vl}) if ky not in dct.keys() else dct.update({ky: dct[ky] + vl})

Powers = {
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
    "E": 1e18
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

CGSUnits = {
    Type.DIMENSIONLESS: "",
    Type.LENGTH: "cm",
    Type.TIME: "sec",
    Type.MASS: "g",
    Type.TEMPERATURE: "K",
    Type.INFORMATION: "bit"
}

BaseUnits = {
    Type.DIMENSIONLESS: "",
    Type.LENGTH: "m",
    Type.TIME: "sec",
    Type.MASS: "g",
    Type.TEMPERATURE: "K",
    Type.INFORMATION: "bit"
}

UnitEquivalencies = {
    # length
    "ft": (0.3048, "m"),
    "in": (0.0254, "m"),
    "yd": (0.9144, "m"),
    "mi": (1609.344, "m"),
    "au": (149597870700., "m"),
    "ly": (9460730472580800., "m"),
    "pc": (3.085677581491362e16, "m"),
    # time
    "day": (86400., "sec"),
    "yr": (31557600., "sec"),
    "month": (30.436875 * 24 * 60 * 60, "sec"),
    "min": (60., "sec"),
    "hr": (3600., "sec"),
    # mass
    "me": (9.109383701528e-28, "g"),
    "Msun": (1.98847e33, "g"),
    "lb": (453.5924, "g"),
    # energy
    "erg": (1.0, "g cm^2 sec^-2"),
    "eV": (1.602177e-12, "erg"),
    "J": (1.0, "kg m^2 sec^-2"),
    "cal": (4.184e7, "erg"),
    # power
    "hp": (7456998715.8, "erg sec^-1"),
    "W": (1e7, "erg sec^-1"),
    # magnetic field
    "G": (1., "erg^1/2 cm^-3/2"),
    # charge
    "statC": (1., "cm^3/2 g^1/2 sec^-1"),
    # information
    "B": (8, "bit"),
    # frequency
    "Hz": (1., "sec^-1"),
}

ConstantValues = {
    # fundamental
    "G": (6.6743015e-11, "m^3 kg^-1 sec^-2"),
    "c": (299792458., "m sec^-1"),
    "hbar": (1.054571817e-34, "J sec"),
    "h": (6.62607015e-34, "J sec"),
    # secondary
    "sigma_SB": (5.670367e-8, "W m^-2 K^-4"),
    "k_B": (1.3806503e-23, "m^2 kg sec^-2 K^-1"),
    # astronomical
    "M_sun": (1.98847e33, "g"),
    "R_sun": (695700, "km"),
    "L_sun": (3.828e26, "W"),
    "M_earth": (5.9722e24, "kg"),
    "R_earth": (6371, "km"),
    # particle physics
    "m_e": (9.109383701528e-28, "g"),
    "q_e": (4.80320427e-10, "statC"),
    "r_e": (2.817940322719e-15, "m"),
    "m_p": (1.672623099e-24, "g"),
    "sigma_T": (6.6524587158e-29, "m^2"),
    "alpha_F": (1.0 / 137.035999873, ""),
}


def StripCoeff(unit_str: str) -> tuple[float, str]:
    coeff = 1.0
    if len(unit_str.split(' ')) > 1:
        try:
            coeff = float(unit_str.split(' ')[0])
            unit_str = " ".join(unit_str.split(' ')[1:])
        except:
            pass
    return coeff, unit_str


def ParseFraction(frac: str) -> 'Fraction':
    return Fraction(Fraction(frac.split('/')[0]), Fraction(frac.split('/')[1]) if len(frac.split('/')) > 1 else None)

def ParseUnit(unit_str: str) -> tuple[float, dict[str, 'Fraction']]:
    coeff, unit_str = StripCoeff(unit_str)
    unit_dict = {}
    for u in unit_str.split(' '):
        pwr = (ParseFraction(u.split('^')[1]) if len(u.split('^')) > 1 else Fraction(1, 1))
        addOrAppend(unit_dict, u.split('^')[0], pwr)
    return coeff, unit_dict

def Stringize(fct: any) -> str:
    if isinstance(fct, dict):
        return " ".join([f"{u}^{p}" if p != 1 else f"{u}" for u, p in fct.items() if p != 0])
    elif isinstance(fct, tuple):
        if isinstance(fct[1], dict):
            return f"{fct[0]} {Stringize(fct[1])}" if fct[0] != 1 else Stringize(fct[1])
        elif isinstance(fct[1], str):
            return f"{fct[0]} {fct[1]}" if fct[0] != 1 else fct[1]
        else:
            raise Exception("Invalid type")
    else:
        raise Exception("Invalid format for Stringize")


def JoinUnits(unit: str) -> str:
    return (Stringize(ParseUnit(unit)))


def ReduceUnitToBase(unit: str = "") -> str:
    coeff, factorized = ParseUnit(unit)
    newunits = {}
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
        elif u[1:] in BaseUnits.values() and u[0] in Powers.keys() and u[1:] != '':
            addOrAppend(newunits, u[1:], p)
            coeff *= Powers[u[0]]**p
        elif u[1:] in UnitEquivalencies.keys() and u[0] in Powers.keys() and u[1:] != '':
            eq_c, eq_u = UnitEquivalencies[u[1:]]
            eq_str = Stringize((eq_c, eq_u))
            eq_base = ReduceUnitToBase(eq_str)
            nc, nu = ParseUnit(eq_base)
            for u2, p2 in nu.items():
                addOrAppend(newunits, u2, p * p2)
            coeff *= nc**p * Powers[u[0]]**p
        else:
            raise Exception(f"Invalid unit: {u}")
    return Stringize((coeff, newunits))


def GetBaseType(unit: str = "") -> dict['Type', 'Fraction']:
    coeff, factorized = ParseUnit(ReduceUnitToBase(unit))
    newf = {}
    for f in factorized.keys():
        for k, v in BaseUnits.items():
            if f == v:
                newf[k] = factorized[f]
                break
    assert len(newf) == len(factorized), "Wrong base type inferrence"
    return newf

def RaiseUnitsToPower(unit, pwr):
    pwr = Fraction(pwr).limit_denominator(1000000)
    c, u = ParseUnit(unit)
    return Stringize((c**pwr, Stringize({b: Fraction(Fraction(pwr) * p) for b, p in u.items()})))

def ConvertUnit(src: str, dst: str) -> tuple[float, str]:
    assert GetBaseType(src) == GetBaseType(dst), \
            "Cannot convert between different base types"
    _, dst_u = StripCoeff(dst)
    red_src = ReduceUnitToBase(src)
    red_dst = ReduceUnitToBase(dst)
    c1, _ = StripCoeff(red_src)
    c2, _ = StripCoeff(red_dst)
    return c1 / c2, dst_u


ValidQuantity = Union['Quantity', tuple, int, float]


class Quantity:
    def __init__(self, *args) -> None:
        if (len(args) == 1) and isinstance(args[0], Quantity):
            self.value = args[0].value
            self.unit = args[0].unit
        elif (len(args) == 1) and isinstance(args[0], str):
            self.value, self.unit = StripCoeff(args[0])
        elif (len(args) == 1) and isinstance(args[0], (int, float)):
            self.value = args[0]
            self.unit = ""
        elif (len(args) == 2) and isinstance(args[0], (int, float)) and isinstance(args[1], str):
            self.value = args[0]
            self.unit = args[1]
        else:
            raise Exception("Invalid arguments for Quantity.__init__")

    def __repr__(self) -> str:
        return f"{self.value} {self.unit}"

    def __str__(self) -> str:
        return self.__repr__()

    def to(self, unit: (str or 'Quantity') = None) -> 'Quantity':
        if unit is None:
            return self.cgs
        elif self.unit == unit:
            return self
        elif isinstance(unit, Quantity):
            return self.to(unit.unit)
        elif isinstance(unit, str):
            return Quantity(*ConvertUnit(Stringize((self.value, self.unit)), unit))
        else:
            raise Exception("Invalid unit")

    @property
    def cgs(self) -> 'Quantity':
        return self.to(Stringize({CGSUnits[b]: p for b, p in GetBaseType(self.unit).items()}))

    def __add__(self, other: ValidQuantity) -> 'Quantity':
        if isinstance(other, Quantity):
            if self.unit == other.unit:
                return Quantity(self.value + other.value, self.unit)
            else:
                return self + other.to(self.unit)
        elif isinstance(other, tuple):
            return self + Quantity(*other)
        elif isinstance(other, (int, float)):
            assert self.unit == "", "Invalid arguments for Quantity.__add__"
            return Quantity(self.value + other, self.unit)
        else:
            raise Exception("Invalid arguments for Quantity.__add__")

    def __radd__(self, other: ValidQuantity) -> 'Quantity':
        return self + other

    def __neg__(self) -> 'Quantity':
        return Quantity(-self.value, self.unit)

    def __sub__(self, other: ValidQuantity) -> 'Quantity':
        return self + (-other)

    def __rsub__(self, other: ValidQuantity) -> 'Quantity':
        return (-self) + other

    def __mul__(self, other: ValidQuantity) -> 'Quantity':
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, JoinUnits(" ".join([self.unit, other.unit])))
        elif isinstance(other, tuple):
            return self * Quantity(*other)
        elif isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        else:
            raise Exception("Invalid arguments for Quantity.__mul__")

    def __rmul__(self, other: ValidQuantity) -> 'Quantity':
        return self * other

    def __pow__(self, other: ValidQuantity) -> 'Quantity':
        if isinstance(other, Quantity):
            assert other.unit == "", "Invalid arguments for Quantity.__pow__"
            return self**(other.value)
        elif isinstance(other, tuple):
            return self**Quantity(*other)
        elif isinstance(other, (int, float)):
            return Quantity(self.value**other, RaiseUnitsToPower(self.unit, other))

    def __truediv__(self, other: ValidQuantity) -> 'Quantity':
        return self * (other**(-1))

    def __rtruediv__(self, other: ValidQuantity) -> 'Quantity':
        return (self**(-1)) * other

class UnitsClass:
    def __init__(self) -> None:
        allunits = [[p + u for p in [''] + list(Powers.keys())] for u in list(BaseUnits.values()) + list(UnitEquivalencies.keys()) if u != '']
        self.units = {u: Quantity(u) for u in sum(allunits, [])}
    def __getattribute__(self, name):
        if name == "all":
            return list(BaseUnits.values()) + list(UnitEquivalencies.keys())
        else:
            return super().__getattribute__("units")[name]

class ConstantsClass:
    def __init__(self) -> None:
        self.constants = {k: Quantity(*v) for k, v in ConstantValues.items()}
    def __getattribute__(self, name):
        if name == "all":
            return {k: Quantity(*v).cgs for k, v in ConstantValues.items()}
        else:
            return super().__getattribute__("constants")[name]
        

Units = UnitsClass()
Constants = ConstantsClass()