from vunit_hooks import VUnitHooks as VH
from vunit.ui import Library
from typing import Mapping, Collection
from os.path import join, basename

def _lookup_file(name: str, src_files: Collection[str]) -> str:
    """Returns the path to the first file named `name`, or None if not available"""
    for path in src_files:
        if basename(path) == name:
            return path
    return None


class VUnitRunner(VH):
    def handle_library(self, logical_name: str, vu_lib: Library, src_files: Collection[str]):
        if logical_name == 'lib':
            tb_with_lower_level_control = vu_lib.entity("tb_with_lower_level_control")
            tb_with_lower_level_control.scan_tests_from_file(_lookup_file("test_control.vhd", src_files))


