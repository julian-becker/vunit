# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2019, Lars Asplund lars.anders.asplund@gmail.com

"""
Generating tests
----------------

Demonstrates generating multiple test runs of the same test bench
with different generic values. Also demonstrates use of ``output_path`` generic
to create test bench output files in location specified by VUnit python runner.
"""

from edalize.vunit_hooks import VUnitHooks as VH
from vunit import VUnit
from vunit.ui import Library
from typing import Mapping, Collection
from itertools import product
from os.path import join, dirname

def make_post_check(data_width, sign):
    """
    Return a check function to verify test case output
    """

    def post_check(output_path):
        """
        This function recives the output_path of the test
        """

        expected = ", ".join([str(data_width),
                              str(sign).lower()]) + "\n"

        output_file = join(output_path, "generics.txt")

        print("Post check: %s" % output_file)
        with open(output_file, "r") as fread:
            got = fread.read()
            if not got == expected:
                print("Content mismatch, got %r expected %r" % (got, expected))
                return False
        return True

    return post_check


def generate_tests(obj, signs, data_widths):
    """
    Generate test by varying the data_width and sign generics
    """

    for sign, data_width in product(signs, data_widths):
        # This configuration name is added as a suffix to the test bench name
        config_name = "data_width=%i,sign=%s" % (data_width, sign)

        # Add the configuration with a post check function to verify the output
        obj.add_config(
            name=config_name,
            generics=dict(
                data_width=data_width,
                sign=sign),
            post_check=make_post_check(data_width, sign)
        )


class VUnitRunner(VH):
    def handle_library(self, logical_name: str, vu_lib: Library):
        if logical_name == 'lib':
            tb_generated = vu_lib.test_bench("tb_generated")

            # Just set a generic for all configurations within the test bench
            tb_generated.set_generic("message", "set-for-entity")

            for test in tb_generated.get_tests():
                if test.name == "Test 2":
                    # Test 2 should only be run with signed width of 16
                    generate_tests(test, [True], [16])
                    test.set_generic("message", "set-for-test")
                else:
                    # Run all other tests with signed/unsigned and data width in range [1,5[
                    generate_tests(test, [False, True], range(1, 5))

 
