import unittest
from binarycpython.utils.functions import *

#############################
# Script that contains unit tests for functions from the binarycpython.utils.functions file


class test_get_help_super(unittest.TestCase):
    """
    Unit test for get_help_super
    """

    def test_all_output(self):
        """
        Function to test the get_help_super function
        """

        get_help_super_output = get_help_super()
        get_help_super_keys = get_help_super_output.keys()

        self.assertIn("stars", get_help_super_keys, "missing section")
        self.assertIn("binary", get_help_super_keys, "missing section")
        self.assertIn("nucsyn", get_help_super_keys, "missing section")
        self.assertIn("output", get_help_super_keys, "missing section")
        self.assertIn("i/o", get_help_super_keys, "missing section")
        self.assertIn("algorithms", get_help_super_keys, "missing section")
        self.assertIn("misc", get_help_super_keys, "missing section")


class test_get_help_all(unittest.TestCase):
    """
    Unit test for get_help_all
    """

    def test_all_output(self):
        """
        Function to test the get_help_all function
        """

        get_help_all_output = get_help_all(print_help=False)
        get_help_all_keys = get_help_all_output.keys()

        self.assertIn("stars", get_help_all_keys, "missing section")
        self.assertIn("binary", get_help_all_keys, "missing section")
        self.assertIn("nucsyn", get_help_all_keys, "missing section")
        self.assertIn("output", get_help_all_keys, "missing section")
        self.assertIn("i/o", get_help_all_keys, "missing section")
        self.assertIn("algorithms", get_help_all_keys, "missing section")
        self.assertIn("misc", get_help_all_keys, "missing section")


class test_get_help(unittest.TestCase):
    def test_input(self):
        """
        Function to test the get_help function
        """

        self.assertEqual(
            get_help("M_1", print_help=False)["parameter_name"],
            "M_1",
            msg="get_help('M_1') should return the correct parameter name",
        )


def all():
    test_get_help()
    test_get_help_all()
    test_get_help_super()


if __name__ == "__main__":
    unittest.main()
