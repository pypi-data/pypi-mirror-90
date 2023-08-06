"""
Module containing the predefined distribution functions

The user can use any of these distribution functions to
generate probability distributions for sampling populations

There are distributions for the following parameters:
    - mass
    - period
    - mass ratio
    - binary fraction

Tasks:
    - TODO: make some things globally present? rob does this in his module..i guess it saves calculations but not sure if im gonna do that now
    - TODO: make global constants stuff
    - TODO: add eccentricity distribution: thermal
    - TODO: Add SFH distributions depending on redshift
    - TODO: Add metallicity distributions depending on redshift
    - TODO: Add initial rotational velocity distributions
"""

import math
import numpy as np
from typing import Optional, Union
from binarycpython.utils.useful_funcs import calc_period_from_sep

###
# File containing probability distributions
# Mostly copied from the perl modules
LOG_LN_CONVERTER = 1.0 / math.log(10.0)
distribution_constants = {}  # To store the constants in


def prepare_dict(global_dict: dict, list_of_sub_keys: list) -> None:
    """
    Function that makes sure that the global dict is prepared to have a value set there. This dictionary will store values and factors for the distribution functions, so that they dont have to be calculated each time.

    Args:
        global_dict: globablly acessible dictionary where factors are stored in
        list_of_sub_keys: List of keys that must become be(come) present in the global_dict
    """

    internal_dict_value = global_dict

    # This loop almost mimics a recursive loop into the dictionary.
    # It checks whether the first key of the list is present, if not; set it with an empty dict.
    # Then it overrides itself to be that (new) item, and goes on to do that again, until the list exhausted
    for k in list_of_sub_keys:
        # If the sub key doesnt exist then make an empty dict
        if not internal_dict_value.get(k, None):
            internal_dict_value[k] = {}
        internal_dict_value = internal_dict_value[k]


def set_opts(opts: dict, newopts: dict) -> dict:
    """
    Function to take a default dict and override it with newer values.

    # TODO: consider changing this to just a dict.update

    Args:
        opts: dictionary with default values
        newopts: dictionary with new values

    Returns:
        returns an updated dictionary
    """

    if newopts:
        for opt in newopts.keys():
            if opt in opts.keys():
                opts[opt] = newopts[opt]

    return opts


def flat() -> float:
    """
    Dummy distribution function that returns 1

    Returns:
        a flat uniform distribution: 1
    """

    return 1.0


def number(value: Union[int, float]) -> Union[int, float]:
    """
    Dummy distribution function that returns the input

    Args:
        value: the value that will be returned by this function.

    Returns:
        the value that was provided
    """

    return value


def const(
    min_bound: Union[int, float], max_bound: Union[int, float], val: float = None
) -> Union[int, float]:
    """
    a constant distribution function between min=min_bound and max=max_bound.

    Args:
        min_bound: lower bound of the range
        max_bound: upper bound of the range

    Returns:
            returns the value of 1/(max_bound-min_bound). If val is provided, it will check whether min_bound < val <= max_bound. if not: returns 0
    """

    if val:
        if not min_bound < val <= max_bound:
            print("out of bounds")
            prob = 0
            return prob
    prob = 1.0 / (min_bound - max_bound)
    return prob


def powerlaw_constant(
    min_val: Union[int, float], max_val: Union[int, float], k: Union[int, float]
) -> Union[int, float]:
    """
    Function that returns the constant to normalise a powerlaw

    TODO: what if k is -1?

    Args:
        min_val: lower bound of the range
        max_val: upper bound of the range
        k: powerlaw slope

    Returns:
        constant to normalize the given powerlaw between the min_val and max_val range
    """

    k1 = k + 1.0
    # print(
    #     "Powerlaw consts from {} to {}, k={} where k1={}".format(
    #         min_val, max_val, k, k1
    #     )
    # )

    powerlaw_const = k1 / (max_val ** k1 - min_val ** k1)
    return powerlaw_const


def powerlaw(
    min_val: Union[int, float],
    max_val: Union[int, float],
    k: Union[int, float],
    x: Union[int, float],
) -> Union[int, float]:
    """
    Single powerlaw with index k at x from min to max

    Args:
        min_val: lower bound of the powerlaw
        max_val: upper bound of the powerlaw
        k: slope of the power law
        x: position at which we want to evaluate

    Returns:
        `probability` at the given position(x)
    """

    # Handle faulty value
    if k == -1:
        print("wrong value for k")
        raise ValueError

    if (x < min_val) or (x > max_val):
        print("input value is out of bounds!")
        return 0

    powerlaw_const = powerlaw_constant(min_val, max_val, k)

    # powerlaw
    prob = powerlaw_const * (x ** k)
    # print(
    #     "Power law from {} to {}: const = {}, y = {}".format(
    #         min_val, max_val, const, y
    #     )
    # )
    return prob


def calculate_constants_three_part_powerlaw(
    m0: Union[int, float],
    m1: Union[int, float],
    m2: Union[int, float],
    m_max: Union[int, float],
    p1: Union[int, float],
    p2: Union[int, float],
    p3: Union[int, float],
) -> Union[int, float]:
    """
    Function to calculate the constants for a three-part powerlaw

    TODO: use the powerlaw_constant function to calculate all these values

    Args:
        m0: lower bound mass
        m1: second boundary, between the first slope and the second slope
        m2: third boundary, between the second slope and the third slope
        m_max: upper bound mass
        p1: first slope
        p2: second slope
        p3: third slope

    Returns:
        array of normalisation constants
    """

    # print("Initialising constants for the three-part powerlaw: m0={} m1={} m2={}\
    # m_max={} p1={} p2={} p3={}\n".format(m0, m1, m2, m_max, p1, p2, p3))

    array_constants_three_part_powerlaw = [0, 0, 0]

    array_constants_three_part_powerlaw[1] = (
        ((m1 ** p2) * (m1 ** (-p1)))
        * (1.0 / (1.0 + p1))
        * (m1 ** (1.0 + p1) - m0 ** (1.0 + p1))
    )
    array_constants_three_part_powerlaw[1] += (
        (m2 ** (1.0 + p2) - m1 ** (1.0 + p2))
    ) * (1.0 / (1.0 + p2))
    array_constants_three_part_powerlaw[1] += (
        ((m2 ** p2) * (m2 ** (-p3)))
        * (1.0 / (1.0 + p3))
        * (m_max ** (1.0 + p3) - m2 ** (1.0 + p3))
    )
    array_constants_three_part_powerlaw[1] = 1.0 / (
        array_constants_three_part_powerlaw[1] + 1e-50
    )

    array_constants_three_part_powerlaw[0] = array_constants_three_part_powerlaw[1] * (
        (m1 ** p2) * (m1 ** (-p1))
    )
    array_constants_three_part_powerlaw[2] = array_constants_three_part_powerlaw[1] * (
        (m2 ** p2) * (m2 ** (-p3))
    )

    return array_constants_three_part_powerlaw
    # $$array[1]=(($m1**$p2)*($m1**(-$p1)))*
    # (1.0/(1.0+$p1))*
    # ($m1**(1.0+$p1)-$m0**(1.0+$p1))+
    # (($m2**(1.0+$p2)-$m1**(1.0+$p2)))*
    # (1.0/(1.0+$p2))+
    # (($m2**$p2)*($m2**(-$p3)))*
    # (1.0/(1.0+$p3))*
    # ($mmax**(1.0+$p3)-$m2**(1.0+$p3));
    # $$array[1]=1.0/($$array[1]+1e-50);
    # $$array[0]=$$array[1]*$m1**$p2*$m1**(-$p1);
    # $$array[2]=$$array[1]*$m2**$p2*$m2**(-$p3);
    # #print "ARRAY SET @_ => @$array\n";
    # $threepart_powerlaw_consts{"@_"}=[@$array];


def three_part_powerlaw(
    m: Union[int, float],
    m0: Union[int, float],
    m1: Union[int, float],
    m2: Union[int, float],
    m_max: Union[int, float],
    p1: Union[int, float],
    p2: Union[int, float],
    p3: Union[int, float],
) -> Union[int, float]:
    """
    Generalized three-part power law, usually used for mass distributions

    Args:
        m: mass at which we want to evaluate the distribution.
        m0: lower bound mass
        m1: second boundary, between the first slope and the second slope
        m2: third boundary, between the second slope and the third slope
        m_max: upper bound mass
        p1: first slope
        p2: second slope
        p3: third slope

    Returns:
        'probability' at given mass m
    """

    # TODO: add check on whether the values exist

    three_part_powerlaw_constants = calculate_constants_three_part_powerlaw(
        m0, m1, m2, m_max, p1, p2, p3
    )

    #
    if m < m0:
        prob = 0  # Below lower bound
    elif m0 < m <= m1:
        prob = three_part_powerlaw_constants[0] * (m ** p1)  # Between M0 and M1
    elif m1 < m <= m2:
        prob = three_part_powerlaw_constants[1] * (m ** p2)  # Between M1 and M2
    elif m2 < m <= m_max:
        prob = three_part_powerlaw_constants[2] * (m ** p3)  # Between M2 and M_MAX
    else:
        prob = 0  # Above M_MAX

    return prob


def gaussian_normalizing_const(
    mean: Union[int, float],
    sigma: Union[int, float],
    gmin: Union[int, float],
    gmax: Union[int, float],
) -> Union[int, float]:
    """
    Function to calculate the normalisation constant for the gaussian

    Args:
        mean: mean of the gaussian
        sigma: standard deviation of the gaussian
        gmin: lower bound of the range to calculate the probabilities in
        gmax: upper bound of the range to calculate the probabilities in

    Returns:
        normalisation constant for the gaussian distribution(mean, sigma) between gmin and gmax
    """

    # First time; calculate multipllier for given mean and sigma
    ptot = 0
    resolution = 1000
    d = (gmax - gmin) / resolution

    for i in range(resolution):
        y = gmin + i * d
        ptot += d * gaussian_func(y, mean, sigma)

    # TODO: Set value in global
    return ptot


def gaussian_func(
    x: Union[int, float], mean: Union[int, float], sigma: Union[int, float]
) -> Union[int, float]:
    """
    Function to evaluate a gaussian at a given point, but this time without any boundaries.

    Args:
        x: location at which to evaluate the distribution
        mean: mean of the gaussian
        sigma: standard deviation of the gaussian

    Returns:
        value of the gaussian at x
    """
    gaussian_prefactor = 1.0 / math.sqrt(2.0 * math.pi)

    r = 1.0 / (sigma)
    y = (x - mean) * r
    return gaussian_prefactor * r * math.exp(-0.5 * y ** 2)


def gaussian(
    x: Union[int, float],
    mean: Union[int, float],
    sigma: Union[int, float],
    gmin: Union[int, float],
    gmax: Union[int, float],
) -> Union[int, float]:
    """
    Gaussian distribution function. used for e..g Duquennoy + Mayor 1991

    Args:
        x: location at which to evaluate the distribution
        mean: mean of the gaussian
        sigma: standard deviation of the gaussian
        gmin: lower bound of the range to calculate the probabilities in
        gmax: upper bound of the range to calculate the probabilities in

    Returns:
        'probability' of the gaussian distribution between the boundaries, evaluated at x
    """

    # # location (X value), mean and sigma, min and max range
    # my ($x,$mean,$sigma,$gmin,$gmax) = @_;

    if (x < gmin) or (x > gmax):
        prob = 0
    else:
        # normalize over given range
        # TODO: add loading into global var
        normalisation = gaussian_normalizing_const(mean, sigma, gmin, gmax)
        prob = normalisation * gaussian_func(x, mean, sigma)

    return prob


#####
# Mass distributions
#####


def Kroupa2001(m: Union[int, float], newopts: dict = None) -> Union[int, float]:
    """
    Probability distribution function for kroupa 2001 IMF, where the default values to the three_part_powerlaw are: default = {"m0": 0.1, "m1": 0.5, "m2": 1, "mmax": 100, "p1": -1.3, "p2": -2.3,"p3": -2.3}

    Args:
        m: mass to evaluate the distribution at
        newopts: optional dict to override the default values.

    Returns:
        'probability' of distribution function evaluated at m
    """

    # Default params and override them
    default = {
        "m0": 0.1,
        "m1": 0.5,
        "m2": 1,
        "mmax": 100,
        "p1": -1.3,
        "p2": -2.3,
        "p3": -2.3,
    }

    value_dict = default.copy()

    if newopts:
        value_dict.update(newopts)

    return three_part_powerlaw(
        m,
        value_dict["m0"],
        value_dict["m1"],
        value_dict["m2"],
        value_dict["mmax"],
        value_dict["p1"],
        value_dict["p2"],
        value_dict["p3"],
    )


def ktg93(m: Union[int, float], newopts: dict = None) -> Union[int, float]:
    """
    Probability distribution function for KTG93 IMF, where the default values to the three_part_powerlaw are: default = {"m0": 0.1, "m1": 0.5, "m2": 1, "mmax": 80, "p1": -1.3, "p2": -2.2,"p3": -2.7}

    Args:
        m: mass to evaluate the distribution at
        newopts: optional dict to override the default values.

    Returns:
        'probability' of distribution function evaluated at m
    """
    # TODO: ask rob what this means

    # if($m eq 'uncertainties')
    # {
    # # return (pointer to) the uncertainties hash
    # return {
    #     m0=>{default=>0.1,
    #      fixed=>1},
    #     m1=>{default=>0.5,
    #      fixed=>1},
    #     m2=>{default=>1.0,
    #      fixed=>1},
    #     mmax=>{default=>80.0,
    #        fixed=>1},
    #     p1=>{default=>-1.3,
    #      low=>-1.3,
    #      high=>-1.3},
    #     p2=>{default=>-2.2,
    #      low=>-2.2,
    #      high=>-2.2},
    #     p3=>{default=>-2.7,
    #      low=>-2.7,
    #      high=>-2.7}
    # };
    # }

    # set options
    # opts = set_opts({'m0':0.1, 'm1':0.5, 'm2':1.0, 'mmax':80, 'p1':-1.3, 'p2':-2.2, 'p3':-2.7},
    # newopts)

    defaults = {
        "m0": 0.1,
        "m1": 0.5,
        "m2": 1.0,
        "mmax": 80,
        "p1": -1.3,
        "p2": -2.2,
        "p3": -2.7,
    }
    value_dict = defaults.copy()

    if newopts:
        value_dict.update(newopts)

    return three_part_powerlaw(
        m,
        value_dict["m0"],
        value_dict["m0"],
        value_dict["m2"],
        value_dict["m0"],
        value_dict["m0"],
        value_dict["m0"],
        value_dict["m0"],
    )


# sub ktg93_lnspace
# {
#     # wrapper for KTG93 on a ln(m) grid
#     my $m=$_[0];
#     return ktg93(@_) * $m;
# }


def imf_tinsley1980(m: Union[int, float]) -> Union[int, float]:
    """
    Probability distribution function for tinsley 1980 IMF (defined up until 80Msol): three_part_powerlaw(m, 0.1, 2.0, 10.0, 80.0, -2.0, -2.3, -3.3)

    Args:
        m: mass to evaluate the distribution at

    Returns:
        'probability' of distribution function evaluated at m
    """

    return three_part_powerlaw(m, 0.1, 2.0, 10.0, 80.0, -2.0, -2.3, -3.3)


def imf_scalo1986(m: Union[int, float]) -> Union[int, float]:
    """
    Probability distribution function for Scalo 1986 IMF (defined up until 80Msol): three_part_powerlaw(m, 0.1, 1.0, 2.0, 80.0, -2.35, -2.35, -2.70)

    Args:
        m: mass to evaluate the distribution at

    Returns:
        'probability' of distribution function evaluated at m
    """
    return three_part_powerlaw(m, 0.1, 1.0, 2.0, 80.0, -2.35, -2.35, -2.70)


def imf_scalo1998(m: Union[int, float]) -> Union[int, float]:
    """
    From scalo 1998

    Probability distribution function for Scalo 1998 IMF (defined up until 80Msol): three_part_powerlaw(m, 0.1, 1.0, 10.0, 80.0, -1.2, -2.7, -2.3)

    Args:
        m: mass to evaluate the distribution at

    Returns:
        'probability' of distribution function evaluated at m
    """

    return three_part_powerlaw(m, 0.1, 1.0, 10.0, 80.0, -1.2, -2.7, -2.3)


def imf_chabrier2003(m: Union[int, float]) -> Union[int, float]:
    """
    Probability distribution function for IMF of Chabrier 2003 PASP 115:763-795

    Args:
        m: mass to evaluate the distribution at

    Returns:
        'probability' of distribution function evaluated at m
    """

    chabrier_logmc = math.log10(0.079)
    chabrier_sigma2 = 0.69 * 0.69
    chabrier_a1 = 0.158
    chabrier_a2 = 4.43e-2
    chabrier_x = -1.3
    if m < 0:
        print("below bounds")
        raise ValueError
    if 0 < m < 1.0:
        A = 0.158
        dm = math.log10(m) - chabrier_logmc
        prob = chabrier_a1 * math.exp(-(dm ** 2) / (2.0 * chabrier_sigma2))
    else:
        prob = chabrier_a2 * (m ** chabrier_x)
    prob = prob / (0.1202462 * m * math.log(10))
    return prob


########################################################################
# Binary fractions
########################################################################


def Arenou2010_binary_fraction(m: Union[int, float]) -> Union[int, float]:
    """
    Arenou 2010 function for the binary fraction as f(M1)

    GAIA-C2-SP-OPM-FA-054
    www.rssd.esa.int/doc_fetch.php?id=2969346

    Args:
        m: mass to evaluate the distribution at

    Returns:
        binary fraction at m
    """

    return 0.8388 * math.tanh(0.688 * m + 0.079)


# print(Arenou2010_binary_fraction(0.4))


def raghavan2010_binary_fraction(m: Union[int, float]) -> Union[int, float]:
    """
    Fit to the Raghavan 2010 binary fraction as a function of
    spectral type (Fig 12). Valid for local stars (Z=Zsolar).

    The spectral type is converted  mass by use of the ZAMS
    effective temperatures from binary_c/BSE (at Z=0.02)
    and the new "long_spectral_type" function of binary_c
    (based on Jaschek+Jaschek's Teff-spectral type table).

    Rob then fitted the result

    Args:
        m: mass to evaluate the distribution at

    Returns:
        binary fraction at m
    """

    return min(
        1.0,
        max(
            (m ** 0.1) * (5.12310e-01) + (-1.02070e-01),
            (1.10450e00) * (m ** (4.93670e-01)) + (-6.95630e-01),
        ),
    )


# print(raghavan2010_binary_fraction(2))

########################################################################
# Period distributions
########################################################################


def duquennoy1991(logper: Union[int, float]) -> Union[int, float]:
    """
    Period distribution from Duquennoy + Mayor 1991. Evaluated the function gaussian(logper, 4.8, 2.3, -2, 12)

    Args:
        logper: logarithm of period to evaluate the distribution at

    Returns:
        'probability' at gaussian(logper, 4.8, 2.3, -2, 12)
    """
    return gaussian(logper, 4.8, 2.3, -2, 12)


def sana12(
    M1: Union[int, float],
    M2: Union[int, float],
    a: Union[int, float],
    P: Union[int, float],
    amin: Union[int, float],
    amax: Union[int, float],
    x0: Union[int, float],
    x1: Union[int, float],
    p: Union[int, float],
) -> Union[int, float]:
    """
    distribution of initial orbital periods as found by Sana et al. (2012)
    which is a flat distribution in ln(a) and ln(P) respectively for stars
    * less massive than 15Msun (no O-stars)
    * mass ratio q=M2/M1<0.1
    * log(P)<0.15=x0 and log(P)>3.5=x1
    and is be given by dp/dlogP ~ (logP)^p for all other binary configurations (default p=-0.55)

    arguments are M1, M2, a, Period P, amin, amax, x0=log P0, x1=log P1, p

    example args: 10, 5, sep(M1, M2, P), sep, ?, -2, 12, -0.55

    # TODO: Fix this function!

    Args:
        M1: Mass of primary
        M2: Mass of secondary
        a: separation of binary
        P: period of binary
        amin: minimum separation of the distribution (lower bound of the range)
        amax: maximum separation of the distribution (upper bound of the range)
        x0: log of minimum period of the distribution (lower bound of the range)
        x1: log of maximum period of the distribution (upper bound of the range)
        p: slope of the distributoon

    Returns:
        'probability' of orbital period P given the other parameters
    """

    res = 0
    if (M1 < 15) or (M2 / M1 < 0.1):
        res = 1.0 / (math.log(amax) - math.log(amin))
    else:
        p1 = 1.0 + p

        # For more details see the LyX document of binary_c for this distribution
        # where the variables and normalizations are given
        # we use the notation x=log(P), xmin=log(Pmin), x0=log(P0), ... to determine the
        x = LOG_LN_CONVERTER * math.log(P)
        xmin = LOG_LN_CONVERTER * math.log(calc_period_from_sep(M1, M2, amin))
        xmax = LOG_LN_CONVERTER * math.log(calc_period_from_sep(M1, M2, amax))

        # print("M1 M2 amin amax P x xmin xmax")
        # print(M1, M2, amin, amax, P, x, xmin, xmax)
        # my $x0 = 0.15;
        # my $x1 = 3.5;

        A1 = 1.0 / (
            x0 ** p * (x0 - xmin) + (x1 ** p1 - x0 ** p1) / p1 + x1 ** p * (xmax - x1)
        )
        A0 = A1 * x0 ** p
        A2 = A1 * x1 ** p

        if x < x0:
            res = 3.0 / 2.0 * LOG_LN_CONVERTER * A0
        elif x > x1:
            res = 3.0 / 2.0 * LOG_LN_CONVERTER * A2
        else:
            res = 3.0 / 2.0 * LOG_LN_CONVERTER * A1 * x ** p

    return res


# print(sana12(10, 2, 10, 100, 1, 1000, math.log(10), math.log(1000), 6))


def interpolate_in_mass_izzard2012(
    M: Union[int, float], high: Union[int, float], low: Union[int, float]
) -> Union[int, float]:
    """
    Function to interpolate in mass

    TODO: fix this function.
    TODO: describe the args
    high: at M=16.3
    low: at 1.15

    Args:
        M: mass
        high:
        low:

    Returns:

    """

    log_interpolation = False

    if log_interpolation:
        return (high - low) / (math.log10(16.3) - math.log10(1.15)) * (
            math.log10(M) - math.log10(1.15)
        ) + low
    else:
        return (high - low) / (16.3 - 1.15) * (M - 1.15) + low


def Izzard2012_period_distribution(
    P: Union[int, float], M1: Union[int, float], log10Pmin: Union[int, float] = 1
) -> Union[int, float]:
    """
    period distribution which interpolates between
    Duquennoy and Mayor 1991 at low mass (G/K spectral type <~1.15Msun)
    and Sana et al 2012 at high mass (O spectral type >~16.3Msun)

    This gives dN/dlogP, i.e. DM/Raghavan's Gaussian in log10P at low mass
    and Sana's power law (as a function of logP) at high mass

    TODO: fix this function

    Args:
        P: period
        M1: Primary star mass
        log10Pmin: minimum period in base log10 (optional)

    Returns:
        'probability' of interpolated distribution function at P and M1

    """

    # Check if there is input and force it to be at least 1
    log10Pmin //= -1.0
    log10Pmin = max(-1.0, log10Pmin)

    # save mass input and limit mass used (M1 from now on) to fitted range
    Mwas = M1
    M1 = max(1.15, min(16.3, M1))
    # print("Izzard2012 called for M={} (trunc'd to {}), P={}\n".format(Mwas, M1, P))

    # Calculate the normalisations
    # need to normalize the distribution for this mass
    # (and perhaps secondary mass)
    prepare_dict(distribution_constants, ["Izzard2012", M1])
    if not distribution_constants["Izzard2012"][M1].get(log10Pmin):
        distribution_constants["Izzard2012"][M1][
            log10Pmin
        ] = 1  # To prevent this loop from going recursive
        N = 200.0  # Resolution for normalisation. I hope 1000 is enough
        dlP = (10.0 - log10Pmin) / N
        C = 0  # normalisation const.
        for lP in np.arange(log10Pmin, 10, dlP):
            C += dlP * Izzard2012_period_distribution(10 ** lP, M1, log10Pmin)

        distribution_constants["Izzard2012"][M1][log10Pmin] = 1.0 / C
    # print(
    #     "Normalization constant for Izzard2012 M={} (log10Pmin={}) is\
    #     {}\n".format(
    #         M1, log10Pmin, distribution_constants["Izzard2012"][M1][log10Pmin]
    #     )
    # )

    lP = math.log10(P)
    # log period

    # # fits
    mu = interpolate_in_mass_izzard2012(M1, -17.8, 5.03)
    sigma = interpolate_in_mass_izzard2012(M1, 9.18, 2.28)
    K = interpolate_in_mass_izzard2012(M1, 6.93e-2, 0.0)
    nu = interpolate_in_mass_izzard2012(M1, 0.3, -1)
    g = 1.0 / (1.0 + 1e-30 ** (lP - nu))

    lPmu = lP - mu
    # print(
    #     "M={} ({}) P={} : mu={} sigma={} K={} nu={} norm=%g\n".format(
    #         Mwas, M1, P, mu, sigma, K, nu
    #     )
    # )

    # print "FUNC $distdata{Izzard2012}{$M}{$log10Pmin} * (exp(- (x-$mu)**2/(2.0*$sigma*$sigma) ) + $K/MAX(0.1,$lP)) * $g;\n";

    if (lP < log10Pmin) or (lP > 10.0):
        return 0

    else:
        return (
            distribution_constants["Izzard2012"][M1][log10Pmin]
            * (math.exp(-lPmu * lPmu / (2.0 * sigma * sigma)) + K / max(0.1, lP))
            * g
        )


########################################################################
# Mass ratio distributions
########################################################################


def flatsections(x: float, opts: dict) -> Union[float, int]:
    """
    Function to generate flat distributions, possibly in multiple sections

    Args:
        x: mass ratio value
        opts: list containing the flat sections. Which are themselves dictionaries, with keys "max": upper bound, "min": lower bound and "height": value

    Returns:
        probability of that mass ratio.
    """

    c = 0
    y = 0

    for opt in opts:
        dc = (opt["max"] - opt["min"]) * opt["height"]
        # print("added flatsection ({}-{})*{} = {}\n".format(
        #   opt['max'], opt['min'], opt['height'], dc))
        c += dc
        if opt["min"] <= x <= opt["max"]:
            y = opt["height"]
            # print("Use this\n")

    c = 1.0 / c
    y = y * c

    # print("flatsections gives C={}: y={}\n",c,y)
    return y


# print(flatsections(1, [{'min': 0, 'max': 2, 'height': 3}]))

########################################################################
# Eccentricity distributions
########################################################################

########################################################################
# Star formation histories
########################################################################

########################################################################
# Metallicity distributions
########################################################################
