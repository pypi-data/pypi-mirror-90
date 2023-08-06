import unittest
import numpy as np
from binarycpython.utils.spacing_functions import *


class test_spacing_functions(unittest.TestCase):
    """
    Unit test for spacing functions
    """

    def test_const(self):
        const_return = const(1, 10, 10)
        self.assertEqual(
            const_return,
            np.linespace(1, 10, 10),
            msg="Output didn't contain SINGLE_STAR_LIFETIME",
        )
