from oompy import Units as u, Constants as c, Assumptions as assume, Quantity


def test_constants():
    assert (c.q_e**2 / c.hbar / c.c) ** -1 == 137.0360243279163
    assert (c.c * c.hbar / c.G) ** 0.5 / c.M_sun == 1.0945269968781705e-38
    assert (c.G * c.hbar / c.c**3) ** 0.5 / c.R_earth == 2.5368940598795702e-42
    assert c.m_e**2 * c.c**3 / (c.q_e * c.hbar) == 44140056281357.734 * u.G
    assert abs((8 * c.pi / 3) * c.r_e**2 - c.sigma_T) / c.sigma_T < 1e-6
    assert (
        4 * c.pi * c.G * c.M_sun * c.m_p * c.c / c.sigma_T / c.L_sun
        == 32839.71688359069
    )
    assert (c.M_sun / u.Msun) == 1.0


def test_units():
    assert str(2.0 * u.m + (3 / 4) * u.ft) == "2.2286 m"
    assert (
        15 * u.kpc / u.Mhr + 25e6 * u.mi / u.sec
    ) == 168803499228.80676 * u.m / u.sec
    assert 5 * u.MHz * 0.25 * u.sec == 1250000.0
    psr_bfield = 1e12 * u.G
    gold_density = 19.3 * u.g / u.cm**3
    assert (psr_bfield / c.c) ** 2 / gold_density == 57.650261971690085
    assert 2e6 * u.hp / (15000 * u.erg / u.sec) == 994266495440.0001
    assert ((u.sec * c.q_e * u.G / (c.m_e * c.c * 2 * c.pi)) >> "") == 2799248.72930016
    assert (u.sec * c.q_e * u.G / (c.m_e * c.c * 2 * c.pi)) == 2799248.72930016
    assert (c.m_e * c.c**2 >> "lb knot^2").value == 6.820051733957203e-13
    assert (2 * u.Rsun / u.au * u.rad >> "deg").value == 0.5329042936337913
    m87_mass = 6.9e9 * u.Msun
    m87_dist = 16.5 * u.Mpc
    m87_rg = c.G * m87_mass / c.c**2
    assert ((2 * m87_rg / m87_dist * u.rad) >> "uarcsec").value == 8.255686423117467
    assert ((c.c / c.H_0) >> "CGS").value == 1.3704635062974675e28


def test_assumptions():
    assert (5 * u.GHz >> assume.Light >> "cm") == 5.995849160000001 * u.cm
    assert (
        6000 * u.K >> assume.Thermal >> "eV" >> assume.Light >> "nm"
        == 2397.95920462134 * u.nm
    )
    assert (Quantity(1, "") >> assume.Redshift >> "pc") == 3396224009.3212013 * u.pc
    assert (5 * u.Gpc >> assume.Redshift >> "") == 1.8018944589315433
    print(f"rest-mass energy of an electron is {c.m_e * c.c**2 >> 'MeV':.2f}")


def test_numpy():
    import numpy as np

    assert np.all(
        (np.array([2 * u.kg, 3 * u.lb, 4 * u.Msun]) * c.c**2)
        == [
            Quantity(1.7975103574736352e17, "J"),
            Quantity(1.2230055556069862e17, "J"),
            Quantity(7.148590841051199e47, "J"),
        ]
    )

    assert np.all(
        (np.array([1, 2, 3]) * u.erg * 2)
        == [
            Quantity(199176423552.0, "g m^2 yr^-2"),
            Quantity(398352847104.0, "g m^2 yr^-2"),
            Quantity(597529270656.0, "g m^2 yr^-2"),
        ]
    )

    dists = np.array([1 * u.fathom, 3 * u.Nmi, 5 * u.au])
    masses = np.array([2, 3, 4]) * u.kg
    times = np.array([0.25 * u.Gyr, 0.1 * u.sec, 0.0001 * u.month])
    factors = np.ones(3)

    assert np.all(
        masses * (dists / times) ** 2 * factors
        == [
            Quantity(1.0746683786302514e-31, "J"),
            Quantity(9260740800.0, "J"),
            Quantity(3.2361095694635258e19, "J"),
        ]
    )


def test_repr():
    assert f"{c.c:.2e}" == "3.00e+08 m sec^-1"
    assert f"{25.0 * u.Msun * c.c**2 >> 'erg':.2e}" == "4.47e+55 erg"
    assert f"{(u.Nmi / u.fathom >> ''):.4f}" == "1012.6859"
