# OOM a/k/a order-of-magnitude v1.3.1

OOM is a python package for working with physical units and quantities. Unlike `astropy` it works in gaussian units, supports a multitude of physical dimensions, constants, and conversion between them. 

## Installation

```sh
pip install git+https://github.com/haykh/oom.git@master
```

## Usage

Importing the main objects:
```python
# import units and constants
from oom import Units as u
from oom import Constants as c
```

### Simple manipulations and unit conversions

Several common usage examples:
```python
# example #1
m_m87 = 6.5e9 * u.Msun
rg_m87 = c.G * m_m87 / c.c**2
print (rg_m87 >> 'au')
#             ^
#             |
#       basic conversion
```

![demo1](demo/demo1.gif)

```python
# example #2
psr_bfield = 1e12 * u.G    # magnetic field in Gauss
gold_density = 19.3 * u.g / u.cm**3
print (((psr_bfield / c.c)**2).cgs)
#                               ^
#                               |
#                        convert to cgs
print ((psr_bfield / c.c)**2 / gold_density >> "")
```

![demo2](demo/demo2.gif)

```python
# example #3
gamma_factor = 1000
b_field = u.MG        # = Mega Gauss 
omega_B = (c.q_e * b_field / (c.m_e * c.c))
sync_omega = gamma_factor**2 * omega_B

print (c.hbar * sync_omega >> 'keV')
#                               ^
#                               |
#                     understands powers of 10 prefixes 
#                       (from 1e-12 to 1e18)

# example #4
# get the reduced physical type of the quantity (i.e., dimension in base units)
print (~(c.hbar * sync_omega))
```

![demo3](demo/demo3.gif)

```python
# example #5
# compare physical quantities in arbitrary units
print ((c.R_sun >> 'ly') == c.R_sun)
# evaluates to True
print (c.M_sun < (c.m_e >> "lb"))
# evaluates to False
print (c.R_sun >= (c.m_e >> "lb"))
# ! errors out (different units)
```

To see all units and/or constants:
```python
print (u.all)
print (c.all)
```

Create your own quantities:
```python
from oom import Quantity
# example #4
my_speed = Quantity('25 m sec^-1')
#                      ^
#                      |
#                 as a string
rabbit_speed = Quantity(55, 'mi hr^-1')
#                         ^
#                         |
#                     as a tuple
elephant_speed = Quantity('km hr^-1')
print ((elephant_speed * my_speed / rabbit_speed) >> 'ly Gy^-1')
#                                                    ^
#                                                    |
#                                             converts lightyear per Gigayear :)
print ((elephant_speed * my_speed / rabbit_speed) >> elephant_speed)
#                                                    ^
#                                                    |
#                                         infer unit from another quantity
```

See demo [on replit.com](https://replit.com/@haykh1/oom-demo?v=1). 

### Vague conversions
This technique enables a comparison between incompatible units under certain assumptions. For instance, one might assume that we consider a photon, and thus its energy, wavelength and frequency are connected via `c` and `h`. 

```python
from oom import Assumptions as assume

# uses h
freq = 5 * u.GHz
freq >> assume.Light >> "cm"

# uses h-bar as freq has a dimension of radians per second
freq = 2 * c.pi * u.rad / u.sec
freq >> assume.Light >> "eV"

# temperature to/from energy
10000 * u.K >> assume.Thermal >> "eV"
```

To list all the available assumptions:
```python
print (list(assume))
```

## For developers

Testing the code is done in three steps using `black` to check the formatting, `mypy` to check the types and typehints, and `pytest` to run the tests. First install all the dependencies:

```sh
pip install black mypy pytest
```

Then run the tests one-by-one:

```sh
black oom --check --diff
mypy oom
pytest
```

These tests are also run automatically on every commit using GitHub Actions.

## To do

- [ ] add more units & constants
- [x] (added in v1.1.0) comparison of quantities (`==`, `!=`, `>`, `<`, `>=`, `<=`)
- [x] (added in v1.1.0) conversion with an rshift (`>>`) operator
- [x] (added in v1.1.0) base unit extraction (with `~`)
- [x] (added in v1.2.0) add a possibility to perform vague conversions (e.g. Kelvin to eV, Hz to erg) etc.
- [x] (added in v1.3.0) unit tests
- [ ] distance to redshift vague conversion
- [ ] add formatting and TeX support
- [ ] add a way to work with scaling relations
