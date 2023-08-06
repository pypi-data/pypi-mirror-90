import unittest

from binarycpython.utils.custom_logging_functions import *

binary_c_temp_dir = temp_dir()


class test_custom_logging(unittest.TestCase):
    """
    Unit test for the custom_logging module
    """

    def test_autogen_C_logging_code(self):

        input_dict_1 = None
        output_1 = autogen_C_logging_code(input_dict_1, verbose=1)
        self.assertEqual(output_1, None, msg="Error. return value should be None")

        input_dict_2 = {
            "MY_STELLAR_DATA": [
                "model.time",
                "star[0].mass",
                "model.probability",
                "model.dt",
            ]
        }
        output_2 = autogen_C_logging_code(input_dict_2, verbose=1)

        test_output_2 = 'Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));'
        self.assertEqual(
            output_2, test_output_2, msg="Output doesnt match the test_output_2"
        )

        input_dict_3 = {"MY_STELLAR_DATA": 2}
        output_3 = autogen_C_logging_code(input_dict_3, verbose=1)
        self.assertEqual(output_3, None, msg="Output should be None")

    def test_binary_c_log_code(self):
        input_1 = "None"
        output_1 = binary_c_log_code(input_1, verbose=1)
        self.assertEqual(output_1, None, msg="Output should be None")

        input_2 = 'Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));'
        output_2 = binary_c_log_code(input_2, verbose=1)
        test_value_2 = '#pragma push_macro("MAX")\n#pragma push_macro("MIN")\n#undef MAX\n#undef MIN\n#include "binary_c.h"\n#include "RLOF/RLOF_prototypes.h"\n\n// add visibility __attribute__ ((visibility ("default"))) to it \nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata);\nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata)\n{\n    // struct stardata_t * stardata = (struct stardata_t *)x;\n    Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));;\n}\n\n#undef MAX \n#undef MIN\n#pragma pop_macro("MIN")\n#pragma pop_macro("MAX")    '
        self.assertEqual(
            output_2,
            test_value_2,
            msg="Output does not match what it should be: {}".format(test_value_2),
        )

    def test_binary_c_write_log_code(self):
        input_1 = '#pragma push_macro("MAX")\n#pragma push_macro("MIN")\n#undef MAX\n#undef MIN\n#include "binary_c.h"\n#include "RLOF/RLOF_prototypes.h"\n\n// add visibility __attribute__ ((visibility ("default"))) to it \nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata);\nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata)\n{\n    // struct stardata_t * stardata = (struct stardata_t *)x;\n    Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));;\n}\n\n#undef MAX \n#undef MIN\n#pragma pop_macro("MIN")\n#pragma pop_macro("MAX")    '
        binary_c_write_log_code(
            input_1,
            os.path.join(binary_c_temp_dir, "test_binary_c_write_log_code.txt"),
            verbose=1,
        )

        self.assertTrue(
            os.path.isfile(
                os.path.join(binary_c_temp_dir, "test_binary_c_write_log_code.txt")
            ),
            msg="File not created",
        )
        with open(
            os.path.join(binary_c_temp_dir, "test_binary_c_write_log_code.txt")
        ) as f:
            content_file = repr(f.read())
        self.assertEqual(repr(input_1), content_file, msg="Contents are not similar")

    def test_from_binary_c_config(self):
        # not going to test everything here, just the version and any output at all

        BINARY_C_DIR = os.getenv("BINARY_C")
        if BINARY_C_DIR:
            BINARY_C_CONFIG = os.path.join(BINARY_C_DIR, "binary_c-config")

        self.assertTrue(
            os.path.isfile(BINARY_C_CONFIG),
            msg="{} doesn't exist".format(BINARY_C_CONFIG),
        )

        input_1 = "aa"
        output_1 = from_binary_c_config(BINARY_C_CONFIG, input_1)
        self.assertTrue(output_1.startswith("Usage"))

        input_2 = "version"
        output_2 = from_binary_c_config(BINARY_C_CONFIG, input_2)
        self.assertEqual(output_2, "2.1.7", msg="binary_c version doesnt match")

    def test_return_compilation_dict(self):
        # Just going to check whether the dictionary has the components it needs
        # TODO: check whether we need to make this better

        output = return_compilation_dict(verbose=1)

        self.assertTrue("cc" in output)
        self.assertTrue("ld" in output)
        self.assertTrue("ccflags" in output)
        self.assertTrue("libs" in output)
        self.assertTrue("inc" in output)

    def test_create_and_load_logging_function(self):
        #
        input_1 = '#pragma push_macro("MAX")\n#pragma push_macro("MIN")\n#undef MAX\n#undef MIN\n#include "binary_c.h"\n#include "RLOF/RLOF_prototypes.h"\n\n// add visibility __attribute__ ((visibility ("default"))) to it \nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata);\nvoid binary_c_API_function custom_output_function(struct stardata_t * stardata)\n{\n    // struct stardata_t * stardata = (struct stardata_t *)x;\n    Printf("MY_STELLAR_DATA %g %g %g %g\\n",((double)stardata->model.time),((double)stardata->star[0].mass),((double)stardata->model.probability),((double)stardata->model.dt));;\n}\n\n#undef MAX \n#undef MIN\n#pragma pop_macro("MIN")\n#pragma pop_macro("MAX")    '
        output_1 = create_and_load_logging_function(input_1, verbose=1)

        self.assertTrue(isinstance(output_1[0], int), msg="memaddr is not an int")
        self.assertTrue(output_1[0] > 0, msg="memaddr is an int but not set correctly")
        self.assertTrue(
            "libcustom_logging" in output_1[1],
            msg="Name of the libcustom_logging not correct",
        )


if __name__ == "__main__":
    unittest.main()
