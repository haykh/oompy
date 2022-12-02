from fractions import Fraction
from typing import Union, Dict, Tuple


def addOrAppend(dct, ky, vl):
    return (
        dct.update({ky: vl}) if ky not in dct.keys() else dct.update({ky: dct[ky] + vl})
    )


def StripCoeff(unit_str: str) -> Tuple[float, str]:
    coeff = 1.0
    if len(unit_str.split(" ")) > 1:
        try:
            coeff = float(unit_str.split(" ")[0])
            unit_str = " ".join(unit_str.split(" ")[1:])
        except:
            pass
    return coeff, unit_str


def ParseFraction(frac: str) -> "Fraction":
    return Fraction(
        Fraction(frac.split("/")[0]),
        Fraction(frac.split("/")[1]) if len(frac.split("/")) > 1 else None,
    )


def ParseUnit(unit_str: str) -> Tuple[float, Dict[str, "Fraction"]]:
    coeff, unit_str = StripCoeff(unit_str)
    unit_dict = {}  # type: dict[str, Fraction]
    for u in unit_str.split(" "):
        pwr = (
            ParseFraction(u.split("^")[1]) if len(u.split("^")) > 1 else Fraction(1, 1)
        )
        unit = u.split("^")[0]
        addOrAppend(unit_dict, unit, pwr if unit != "" else Fraction(0, 1))
    return coeff, unit_dict


def Stringize(fct: Union[Dict, Tuple]) -> str:
    if isinstance(fct, dict):
        return " ".join(
            [f"{u}^{p}" if p != 1 else f"{u}" for u, p in fct.items() if p != 0]
        )
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
    return Stringize(ParseUnit(unit))
