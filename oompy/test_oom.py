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


def test_assumptions():
    assert (5 * u.GHz >> assume.Light >> "cm") == 5.995849160000001 * u.cm
    assert (
        6000 * u.K >> assume.Thermal >> "eV" >> assume.Light >> "nm"
        == 2397.95920462134 * u.nm
    )
    assert (Quantity(1, "") >> assume.Redshift >> "pc") == 3396224009.3212013 * u.pc
    assert (5 * u.Gpc >> assume.Redshift >> "") == 1.8018944589315433


def test_numpy():
    import numpy as np

    assert np.all(
        (np.array([1, 2, 3]) * u.erg * 2)
        == [
            Quantity(199176423552.0, "g m^2 yr^-2"),
            Quantity(398352847104.0, "g m^2 yr^-2"),
            Quantity(597529270656.0, "g m^2 yr^-2"),
        ]
    )
