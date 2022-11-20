# OOM a/k/a order-of-magnitude

OOM is a python package for working with physical units and quantities. Unlike `astropy` it works in gaussian units and supports a multitude of physical units as well as constants.

## Installation

```sh
pip install git+...
```

## Usage

Importing the main objects:
```python
# import units and constants
from oom import Units as u
from oom import Constants as c
```

Several common usage examples:
```python
# example #1
m_m87 = 6.5e9 * u.Msun
rg_m87 = c.G * m_m87 / c.c**2
print (rg_m87.to('au'))
#              ^
#              |
#        basic conversion

# example #2
psr_bfield = 1e12 * u.G    # magnetic field in Gauss
gold_density = 19.3 * u.g / u.cm**3
print (((psr_bfield / c.c)**2 / gold_density).cgs)
#                                              ^
#                                              |
#                                       convert to cgs

# example #3
gamma_factor = 1000
b_field = u.MG        # = Mega Gauss 
omega_B = (c.q_e * b_field / (c.m_e * c.c))
sync_omega = gamma_factor**2 * omega_B

print ((c.hbar * sync_omega).to('keV'))
#                                ^
#                                |
#                      understands powers of 10 prefixes 
#                        (from 1e-12 to 1e18)
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
print ((my_speed / rabbit_speed).to())
```

## To do

- [ ] add more units
- [ ] add more constants
- [ ] add a possibility to perform vague conversions (e.g. Kelvin to eV, Hz to erg) etc.
- [ ] add a formatting and TeX support
- [ ] add a way to work with scaling relations