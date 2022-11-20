from setuptools import setup, find_packages

long_description = "Python Module for calculations with physical units (supports Gaussian units)."

setup(
    name             = 'oom',
    description      = 'Order of Magnitude',
    packages         = find_packages(),
    author           = 'morninbru',
    author_email     = 'haykh.astro [at] gmail.com',
    version          = "1.0",
    license          = "BSD",
    zip_safe         = False,
    keywords         = "python, oom, order of magnitude, units, physical units, gaussian units",
    long_description = long_description
)
