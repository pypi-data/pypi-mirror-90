import unittest

from binarycpython.utils.grid_options_defaults import *

binary_c_temp_dir = temp_dir()


class test_grid_options_defaults(unittest.TestCase):
    """
    Unit test for the custom_logging module
    """

    def test_grid_options_help(self):
        input_1 = "aa"
        result_1 = grid_options_help(input_1)
        self.assertEqual(result_1, {}, msg="Dict should be empty")

        input_2 = "amt_cores"
        result_2 = grid_options_help(input_2)
        self.assertIn(
            input_2,
            result_2,
            msg="{} should be in the keys of the returned dict".format(input_2),
        )
        self.assertNotEqual(
            result_2[input_2], "", msg="description should not be empty"
        )

        input_3 = "condor_jobid"
        result_3 = grid_options_help(input_3)
        self.assertIn(
            input_3,
            result_3,
            msg="{} should be in the keys of the returned dict".format(input_3),
        )
        self.assertEqual(result_3[input_3], "", msg="description should be empty")


if __name__ == "__main__":
    unittest.main()
