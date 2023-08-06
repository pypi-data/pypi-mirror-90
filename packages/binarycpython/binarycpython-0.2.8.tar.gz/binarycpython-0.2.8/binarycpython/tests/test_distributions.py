"""
Module containing the unittests for the distribution functions. 
"""
import unittest

from binarycpython.utils.distribution_functions import *
from binarycpython.utils.useful_funcs import calc_sep_from_period


class TestDistributions(unittest.TestCase):
    """
    Unittest class

    # https://stackoverflow.com/questions/17353213/init-for-unittest-testcase
    """

    def __init__(self, *args, **kwargs):
        super(TestDistributions, self).__init__(*args, **kwargs)
        # self.gen_stubs()

        self.mass_list = [0.1, 0.2, 1, 10, 15, 50]
        self.logper_list = [-2, -0.5, 1.6, 2.5, 5.3, 10]
        self.q_list = [0.01, 0.2, 0.4, 0.652, 0.823, 1]
        self.per_list = [10 ** logper for logper in self.logper_list]

        self.tolerance = 1e-5

    def test_powerlaw(self):
        """
        unittest for the powerlaw test
        """

        perl_results = [
            0,
            0,
            1.30327367546194,
            0.00653184128064016,
            0.00257054805572128,
            0.000161214690242696,
        ]
        python_results = []

        for mass in self.mass_list:
            python_results.append(powerlaw(1, 100, -2.3, mass))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_three_part_power_law(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [
            10.0001044752901,
            2.03065220596677,
            0.0501192469795434,
            0.000251191267451594,
            9.88540897458207e-05,
            6.19974072148769e-06,
        ]
        python_results = []

        for mass in self.mass_list:
            python_results.append(
                three_part_powerlaw(mass, 0.08, 0.1, 1, 300, -1.3, -2.3, -2.3)
            )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_Kroupa2001(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [
            5.71196495365248,
            2.31977861075353,
            0.143138195684851,
            0.000717390363216896,
            0.000282322598503135,
            1.77061658757533e-05,
        ]
        python_results = []

        for mass in self.mass_list:
            python_results.append(Kroupa2001(mass))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_ktg93(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [
            5.79767807698379,
            2.35458895566605,
            0.155713799148675,
            0.000310689875361984,
            0.000103963454405194,
            4.02817276824841e-06,
        ]
        python_results = []

        for mass in self.mass_list:
            python_results.append(ktg93(mass))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_gaussian(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [
            0.00218800520299544,
            0.0121641269671571,
            0.0657353455837751,
            0.104951743573429,
            0.16899534495487,
            0.0134332780385336,
        ]
        python_results = []

        for logper in self.logper_list:
            python_results.append(gaussian(logper, 4.8, 2.3, -2.0, 12.0))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_Arenou2010_binary_fraction(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [
            0.123079723518677,
            0.178895136157746,
            0.541178340047153,
            0.838798485820276,
            0.838799998443204,
            0.8388,
        ]
        python_results = []

        for mass in self.mass_list:
            python_results.append(Arenou2010_binary_fraction(mass))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_raghavan2010_binary_fraction(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [0.304872297931597, 0.334079955706623, 0.41024, 1, 1, 1]
        python_results = []

        for mass in self.mass_list:
            python_results.append(raghavan2010_binary_fraction(mass))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_Izzard2012_period_distribution(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [
            0,
            0.00941322840619318,
            0.0575068231479569,
            0.0963349886047932,
            0.177058537292581,
            0.0165713385659234,
            0,
            0.00941322840619318,
            0.0575068231479569,
            0.0963349886047932,
            0.177058537292581,
            0.0165713385659234,
            0,
            0.00941322840619318,
            0.0575068231479569,
            0.0963349886047932,
            0.177058537292581,
            0.0165713385659234,
            0,
            7.61631504133159e-09,
            0.168028727846997,
            0.130936282216512,
            0.0559170865520968,
            0.0100358604460285,
            0,
            2.08432736869149e-21,
            0.18713622563288,
            0.143151383185002,
            0.0676299576972089,
            0.0192427864870784,
            0,
            1.1130335685003e-24,
            0.194272603987661,
            0.14771508552257,
            0.0713078479280884,
            0.0221093965810181,
        ]
        python_results = []

        for mass in self.mass_list:
            for per in self.per_list:
                python_results.append(Izzard2012_period_distribution(per, mass))

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_flatsections(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [
            1.01010101010101,
            1.01010101010101,
            1.01010101010101,
            1.01010101010101,
            1.01010101010101,
            1.01010101010101,
        ]
        python_results = []

        for q in self.q_list:
            python_results.append(
                flatsections(q, [{"min": 0.01, "max": 1.0, "height": 1.0}])
            )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)

    def test_sana12(self):
        """
        unittest for three_part_power_law
        """

        perl_results = [
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.121764808010258,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
            0.481676471294883,
            0.481676471294883,
            0.131020615300798,
            0.102503482445846,
            0.0678037785559114,
            0.066436408359805,
        ]
        python_results = []

        for mass in self.mass_list:
            for q in self.q_list:
                for per in self.per_list:
                    mass_2 = mass * q

                    sep = calc_sep_from_period(mass, mass_2, per)
                    sep_min = calc_sep_from_period(mass, mass_2, 10 ** 0.15)
                    sep_max = calc_sep_from_period(mass, mass_2, 10 ** 5.5)
                    python_results.append(
                        sana12(
                            mass, mass_2, sep, per, sep_min, sep_max, 0.15, 5.5, -0.55
                        )
                    )

        # GO over the results and check whether they are equal (within tolerance)
        for i in range(len(python_results)):
            self.assertLess(np.abs(python_results[i] - perl_results[i]), self.tolerance)


if __name__ == "__main__":
    unittest.main()
