import os
import sys
import time
import json
import textwrap
import unittest

from binarycpython import _binary_c_bindings

from binarycpython.utils.functions import (
    binarycDecoder,
    temp_dir,
    inspect_dict,
    merge_dicts,
    handle_ensemble_string_to_json,
)

# https://docs.python.org/3/library/unittest.html
TMP_DIR = temp_dir()
os.makedirs(os.path.join(TMP_DIR, "test"), exist_ok=True)

####
def return_argstring(
    m1=15.0,
    m2=14.0,
    separation=0,
    orbital_period=453000000000,
    eccentricity=0.0,
    metallicity=0.02,
    max_evolution_time=15000,
    defer_ensemble=0,
    ensemble_filters_off=1,
    ensemble_filter="SUPERNOVAE",
):
    """
    Function to make a argstring that we can use in these tests
    """

    # Make the argstrings
    argstring_template = "binary_c M_1 {0:g} M_2 {1:g} separation {2:g} orbital_period {3:g} \
eccentricity {4:g} metallicity {5:g} max_evolution_time {6:g} ensemble 1 ensemble_defer {7} \
ensemble_filters_off {8} ensemble_filter_{9} 1 probability 0.1"

    argstring = argstring_template.format(
        m1,
        m2,
        separation,
        orbital_period,
        eccentricity,
        metallicity,
        max_evolution_time,
        defer_ensemble,
        ensemble_filters_off,
        ensemble_filter,
    )

    return argstring


#######################################################################################################################################################
### General run_system test
#######################################################################################################################################################


class test_run_system(unittest.TestCase):
    """
    Unit test for run_system
    """

    def test_output(self):
        m1 = 15.0  # Msun
        m2 = 14.0  # Msun
        separation = 0  # 0 = ignored, use period
        orbital_period = 4530.0  # days
        eccentricity = 0.0
        metallicity = 0.02
        max_evolution_time = 15000
        argstring = "binary_c M_1 {0:g} M_2 {1:g} separation {2:g} orbital_period {3:g} eccentricity {4:g} metallicity {5:g} max_evolution_time {6:g}  ".format(
            m1,
            m2,
            separation,
            orbital_period,
            eccentricity,
            metallicity,
            max_evolution_time,
        )

        output = _binary_c_bindings.run_system(argstring=argstring)

        self.assertIn(
            "SINGLE_STAR_LIFETIME",
            output,
            msg="Output didn't contain SINGLE_STAR_LIFETIME",
        )


#######################################################################################################################################################
### memaddr test
#######################################################################################################################################################


class test_return_store_memaddr(unittest.TestCase):
    """
    Unit test for return_store_memaddr
    """

    def test_return_store_memaddr(self):
        output = _binary_c_bindings.return_store_memaddr()

        # print("function: test_return_store")
        # print("store memory adress:")
        # print(textwrap.indent(str(output), "\t"))

        self.assertNotEqual(output, -1, "memory adress not created properly")

        # TODO: check if we can built in some signal for how successful this was.
        _ = _binary_c_bindings.free_store_memaddr(output)


#######################################################################################################################################################
### ensemble tests
#######################################################################################################################################################


class TestEnsemble(unittest.TestCase):
    def test_minimal_ensemble_output(self):
        """
        Tase case to check if the ensemble output is correctly written to the buffer instead of printed
        """

        m1 = 2  # Msun
        m2 = 0.1  # Msun

        #############################################################################################
        # The 2 runs below use the ensemble but do not defer the output to anything else, so that the
        # results are returned directly after the run

        # Direct output commands
        argstring_1 = return_argstring(
            m1=m1, m2=m2, ensemble_filter="STELLAR_TYPE_COUNTS", defer_ensemble=0
        )
        # Get outputs
        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)

        test_ensemble_jsons_string = [
            line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
        ]

        test_json = handle_ensemble_string_to_json(
            test_ensemble_jsons_string[0][len("ENSEMBLE_JSON ") :]
        )

        # print(test_json.keys())
        # print(test_json)

        self.assertIsNotNone(
            test_json,
            msg="Ensemble output not correctly written passed to the buffer in _binary_c_bindings",
        )
        self.assertIn("number_counts", test_json.keys())

    def test_return_persistent_data_memaddr(self):
        """
        Test case to check if the memory adress has been created succesfully
        """

        output = _binary_c_bindings.return_persistent_data_memaddr()

        print("function: test_run_system")
        print("Binary_c output:")
        print(textwrap.indent(str(output), "\t"))

        self.assertIsInstance(output, int, msg="memory adress has to be an integer")
        self.assertNotEqual(
            output, 0, "memory adress seems not to have a correct value"
        )

    def test_passing_persistent_data_to_run_system(self):
        # Function to test the passing of the persistent data memoery adress, and having ensemble_defer = True
        # We should see that the results of multiple systems have been added to the one output json

        # Make argstrings
        argstring_1 = return_argstring(defer_ensemble=0)
        argstring_1_deferred = return_argstring(defer_ensemble=1)
        argstring_2 = return_argstring(defer_ensemble=0)

        #
        persistent_data_memaddr = _binary_c_bindings.return_persistent_data_memaddr()

        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
        ensemble_jsons_1 = [
            line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
        ]
        json_1 = handle_ensemble_string_to_json(
            ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :]
        )

        # Doing 2 systems in a row.
        output_1_deferred = _binary_c_bindings.run_system(
            argstring=argstring_1_deferred,
            persistent_data_memaddr=persistent_data_memaddr,
        )
        output_2 = _binary_c_bindings.run_system(
            argstring=argstring_2, persistent_data_memaddr=persistent_data_memaddr
        )
        ensemble_jsons_2 = [
            line for line in output_2.splitlines() if line.startswith("ENSEMBLE_JSON")
        ]
        json_2 = handle_ensemble_string_to_json(
            ensemble_jsons_2[0][len("ENSEMBLE_JSON ") :]
        )

        # Doing system one again.
        output_1_again = _binary_c_bindings.run_system(argstring=argstring_1)
        ensemble_jsons_1 = [
            line
            for line in output_1_again.splitlines()
            if line.startswith("ENSEMBLE_JSON")
        ]
        json_1_again = handle_ensemble_string_to_json(
            ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :]
        )

        self.assertEqual(
            json_1,
            json_1_again,
            msg="The system with the same initial settings did not give the same output",
        )
        self.assertNotEqual(
            json_1,
            json_2,
            msg="The output of the deferred two systems should not be the same as the first undeferred output",
        )

    def test_adding_ensemble_output(self):
        """
        Function that adds the output of 2 ensembles and compares it to the output that we get by deferring the first output
        """

        m1 = 2  # Msun
        m2 = 0.1  # Msun
        extra_mass = 10

        #############################################################################################
        # The 2 runs below use the ensemble but do not defer the output to anything else, so that the
        # results are returned directly after the run

        # Direct output commands
        argstring_1 = return_argstring(
            m1=m1, m2=m2, ensemble_filter="STELLAR_TYPE_COUNTS", defer_ensemble=0
        )
        argstring_2 = return_argstring(
            m1=m1 + extra_mass,
            m2=m2,
            ensemble_filter="STELLAR_TYPE_COUNTS",
            defer_ensemble=0,
        )

        # Get outputs
        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
        output_2 = _binary_c_bindings.run_system(argstring=argstring_2)

        test_1_ensemble_jsons_1 = [
            line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
        ]
        test_1_ensemble_jsons_2 = [
            line for line in output_2.splitlines() if line.startswith("ENSEMBLE_JSON")
        ]

        test_1_json_1 = handle_ensemble_string_to_json(
            test_1_ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :]
        )
        test_1_json_2 = handle_ensemble_string_to_json(
            test_1_ensemble_jsons_2[0][len("ENSEMBLE_JSON ") :]
        )

        test_1_merged_dict = merge_dicts(test_1_json_1, test_1_json_2)

        with open(os.path.join(TMP_DIR, "test", "adding_json_1.json"), "w") as file:
            file.write(json.dumps(test_1_json_1, indent=4))
        with open(os.path.join(TMP_DIR, "test", "adding_json_2.json"), "w") as file:
            file.write(json.dumps(test_1_json_2, indent=4))
        with open(
            os.path.join(TMP_DIR, "test", "adding_json_merged.json"), "w"
        ) as file:
            file.write(json.dumps(test_1_json_2, indent=4))

        print("Single runs done\n")

        #############################################################################################
        # The 2 runs below use the ensemble and both defer the output so that after they are finished
        # nothing is printed. After that we explicitly free the memory of the persistent_data and
        # have the output returned in that way

        # Deferred commands
        argstring_1_deferred = return_argstring(
            m1=m1, m2=m2, ensemble_filter="STELLAR_TYPE_COUNTS", defer_ensemble=1
        )
        argstring_2_deferred = return_argstring(
            m1=m1 + extra_mass,
            m2=m2,
            ensemble_filter="STELLAR_TYPE_COUNTS",
            defer_ensemble=1,
        )

        # Get a memory location
        test_2_persistent_data_memaddr = (
            _binary_c_bindings.return_persistent_data_memaddr()
        )

        # Run the systems and defer the output each time
        _ = _binary_c_bindings.run_system(
            argstring=argstring_1_deferred,
            persistent_data_memaddr=test_2_persistent_data_memaddr,
        )
        _ = _binary_c_bindings.run_system(
            argstring=argstring_2_deferred,
            persistent_data_memaddr=test_2_persistent_data_memaddr,
        )

        # Have the persistent_memory adress be released and have the json outputted
        test_2_output = (
            _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
                test_2_persistent_data_memaddr
            )
        )
        test_2_ensemble_json = [
            line
            for line in test_2_output.splitlines()
            if line.startswith("ENSEMBLE_JSON")
        ]
        test_2_json = handle_ensemble_string_to_json(
            test_2_ensemble_json[0][len("ENSEMBLE_JSON ") :]
        )

        with open(
            os.path.join(TMP_DIR, "test", "adding_json_deferred.json"), "w"
        ) as file:
            file.write(json.dumps(test_2_json, indent=4))

        print("Double deferred done\n")

        #############################################################################################
        # The 2 runs below use the ensemble and the first one defers the output to the memory,
        # Then the second one uses that memory to combine its results with, but doesn't defer the
        # data after that, so it will print it after the second run is done

        test_3_persistent_data_memaddr = (
            _binary_c_bindings.return_persistent_data_memaddr()
        )

        # Run the systems and defer the output once and the second time not, so that the second run
        # automatically prints out the results
        _ = _binary_c_bindings.run_system(
            argstring=argstring_1_deferred,
            persistent_data_memaddr=test_3_persistent_data_memaddr,
        )
        test_3_output_2 = _binary_c_bindings.run_system(
            argstring=argstring_2,
            persistent_data_memaddr=test_3_persistent_data_memaddr,
        )
        test_3_ensemble_jsons = [
            line
            for line in test_3_output_2.splitlines()
            if line.startswith("ENSEMBLE_JSON")
        ]
        test_3_json = handle_ensemble_string_to_json(
            test_3_ensemble_jsons[0][len("ENSEMBLE_JSON ") :]
        )

        with open(
            os.path.join(TMP_DIR, "test", "adding_json_deferred_and_output.json"), "w"
        ) as f:
            f.write(json.dumps(test_3_json, indent=4))

        print("Single deferred done\n")

        #
        assert_message_1 = """
        The structure of the manually merged is not the same as the merged by double deferring
        """
        assert_message_2 = """
        The structure of the manually merged is not the same as the merged by deferring once
        and output on the second run
        """

        #
        # print(json.dumps(test_1_merged_dict, indent=4))
        # print(json.dumps(test_2_json, indent=4))

        # TODO: add more asserts.
        #
        self.assertEqual(
            inspect_dict(test_1_merged_dict, print_structure=False),
            inspect_dict(test_2_json, print_structure=False),
            msg=assert_message_1,
        )
        # assert inspect_dict(test_1_merged_dict, print_structure=False) == inspect_dict(test_3_json, print_structure=False), assert_message_2

    def test_free_and_json_output(self):
        """
        Function that tests the freeing of the memory adress and the output of the json
        """

        m1 = 2  # Msun
        m2 = 0.1  # Msun

        # Get argstring:
        argstring_1 = return_argstring(
            m1=m2, m2=m2, ensemble_filter="STELLAR_TYPE_COUNTS", defer_ensemble=1
        )

        # Get a memory adress:
        persistent_data_memaddr = _binary_c_bindings.return_persistent_data_memaddr()

        # Evolve and defer output
        output_1_deferred = _binary_c_bindings.run_system(
            argstring=argstring_1, persistent_data_memaddr=persistent_data_memaddr
        )

        # Free memory adress
        json_output_by_freeing = (
            _binary_c_bindings.free_persistent_data_memaddr_and_return_json_output(
                persistent_data_memaddr
            )
        )
        # print(textwrap.indent(str(json_output_by_freeing), "\t"))

        parsed_json = handle_ensemble_string_to_json(
            json_output_by_freeing.splitlines()[0][len("ENSEMBLE_JSON ") :],
        )

        self.assertIn(
            "number_counts",
            parsed_json.keys(),
            msg="Output not correct. 'number_counts' not part of the keys",
        )

    def test_combine_with_empty_json(self):
        """
        Test for merging with an empty dict
        """

        argstring_1 = return_argstring(defer_ensemble=0)
        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
        ensemble_jsons_1 = [
            line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
        ]
        json_1 = handle_ensemble_string_to_json(
            ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :]
        )

        assert_message = "combining output json with empty dict should give same result as initial json"

        self.assertEqual(merge_dicts(json_1, {}), json_1, assert_message)

    #############
    def _test_full_ensemble_output(self):
        """
        Function to just output the whole ensemble
        TODO: put this one back
        """

        argstring_1 = return_argstring(defer_ensemble=0, ensemble_filters_off=0)
        # print(argstring_1)

        output_1 = _binary_c_bindings.run_system(argstring=argstring_1)
        ensemble_jsons_1 = [
            line for line in output_1.splitlines() if line.startswith("ENSEMBLE_JSON")
        ]
        json_1 = handle_ensemble_string_to_json(
            ensemble_jsons_1[0][len("ENSEMBLE_JSON ") :]
        )

        keys = json_1.keys()

        # assert statements:
        self.assertIn("number_counts", keys)
        self.assertIn("HRD", keys)
        self.assertIn("HRD(t)", keys)
        self.assertIn("Xyield", keys)
        self.assertIn("distributions", keys)
        self.assertIn("scalars", keys)


def all():
    test_run_system()
    test_return_store_memaddr()
    test_unload_store_memaddr()
    test_minimal_ensemble_output()
    test_return_persistent_data_memaddr()
    test_passing_persistent_data_to_run_system()
    test_full_ensemble_output()
    test_adding_ensemble_output()
    test_free_and_json_output()
    test_combine_with_empty_json()


# ####
# if __name__ == "__main__":
#     # test_minimal_ensemble_output()
#     # test_return_persistent_data_memaddr()
#     # test_passing_persistent_data_to_run_system()
#     # test_full_ensemble_output()
#     # test_adding_ensemble_output()
#     # test_free_and_json_output()
#     # test_combine_with_empty_json()
#     all()
#     print("Done")

if __name__ == "__main__":
    unittest.main()
