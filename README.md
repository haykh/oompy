# OOMpy a/k/a order-of-magnitude python

[![Python package](https://github.com/haykh/oompy/actions/workflows/github-pytest.yml/badge.svg)](https://github.com/haykh/oompy/actions/workflows/github-pytest.yml)

OOMpy is a python package for working with physical units and quantities. Unlike `astropy` it works in gaussian units, supports a multitude of physical dimensions, constants, and conversion between them. 

## Installation

```sh
pip install oompy
```

## Usage

Importing the main objects:
```python
# import units and constants
from oompy import Units as u
from oompy import Constants as c
```

### Simple manipulations and unit conversions

Several common usage examples:
```python
# example #1
m_m87 = 6.5e9 * u.Msun
rg_m87 = c.G * m_m87 / c.c**2
rg_m87 >> 'au'
#       ^
#       |
# basic conversion
#
# Output: 64.16104122314108 au
```

```python
# example #2
psr_bfield = 1e12 * u.G    # magnetic field in Gauss
gold_density = 19.3 * u.g / u.cm**3
((psr_bfield / c.c)**2).cgs
#                        ^
#                        |
#                 convert to cgs
#
# Output: 1112.6500560536185 g cm^-3
#
(psr_bfield / c.c)**2 / gold_density >> ""
#
# Output: 57.650261971690085
```

```python
# example #3
gamma_factor = 1000
b_field = u.MG        # = Mega Gauss 
omega_B = (c.q_e * b_field / (c.m_e * c.c))
sync_omega = gamma_factor**2 * omega_B

c.hbar * sync_omega >> 'keV'
#                       ^
#                       |
#             understands powers of 10 prefixes 
#               (from 1e-12 to 1e18)
#
# Output: 11.576759893742388 keV

# example #4
# get the reduced physical type of the quantity (i.e., dimension in base units)
~(c.hbar * sync_omega)
#
# Output: {<Type.MASS: 3>: Fraction(1, 1), <Type.LENGTH: 1>: Fraction(2, 1), <Type.TIME: 2>: Fraction(-2, 1)}
```

```python
# example #4
# compare physical quantities in arbitrary units
(c.R_sun >> 'ly') == c.R_sun # True
c.M_sun < (c.m_e >> "lb") # False
c.R_sun >= (c.m_e >> "lb") # Error: incompatible units
```

To see all units and/or constants:
```python
u.all
c.all
```

Create your own quantities:
```python
from oompy import Quantity
# example #5
my_speed = Quantity('25 m sec^-1')
#                      ^
#                      |
#                 as a string
rabbit_speed = Quantity(55, 'mi hr^-1')
#                         ^
#                         |
#                     as a tuple
elephant_speed = Quantity('km hr^-1')
(elephant_speed * my_speed / rabbit_speed) >> 'ly Gyr^-1'
#                                                  ^
#                                                  |
#                                           converts lightyear per Gigayear :)
#
# Output: 0.9421232705492877 ly Gyr^-1
```

### Vague conversions
This technique enables a comparison between incompatible units under certain assumptions. For instance, one might assume that we consider a photon, and thus its energy, wavelength and frequency are connected via `c` and `h`. 

```python
from oompy import Assumptions as assume, Quantity

# uses h
freq = 5 * u.GHz
freq >> assume.Light >> "cm"
#
# Output: 5.995849160000001 cm

# uses h-bar as freq has a dimension of radians per second
freq = 2 * c.pi * u.rad / u.sec
freq >> assume.Light >> "eV"
#
# Output: 4.1356667496413186e-15 eV

# temperature to/from energy
10000 * u.K >> assume.Thermal >> "eV"
#
# Output: 0.8617339407568576 eV

# compute co-moving distance for a redshift
Quantity(5, "") >> assume.Redshift >> "Gly"
#
# Output: 25.878013331255335 Gly
#
# compute redshift for a co-moving distance
5 * u.Gpc >> assume.Redshift >> ""
#
# Output: 1.8018944589315433
```

To list all the available assumptions:
```python
list(assume)
```

## For developers

Testing the code is done in three steps using `black` to check the formatting, `mypy` to check the types and typehints, and `pytest` to run the tests. First install all the dependencies:

```sh
pip install black mypy pytest
```

Then run the tests one-by-one:

```sh
black oompy --check --diff
mypy oompy
pytest
```

These tests are also run automatically on every commit using GitHub Actions.

## To do

- [ ] add more units & constants
  - [x] (added in v1.3.5) knots
  - [ ] fathom
  - [ ] nautical miles
- [x] (added in v1.1.0) comparison of quantities (`==`, `!=`, `>`, `<`, `>=`, `<=`)
- [x] (added in v1.1.0) conversion with an rshift (`>>`) operator
- [x] (added in v1.1.0) base unit extraction (with `~`)
- [x] (added in v1.2.0) add a possibility to perform vague conversions (e.g. Kelvin to eV, Hz to erg) etc.
- [x] (added in v1.3.0) unit tests
- [ ] add support for Ki, Mi, Gi (2e10, 2e20, 2e30)
- [x] (added in v1.3.5) distance to redshift vague conversion
- [x] (added in v1.4.0) work with numpy arrays
- [ ] (TBA in v1.5.0) add formatting and TeX support
- [ ] add a way to work with scaling relations
