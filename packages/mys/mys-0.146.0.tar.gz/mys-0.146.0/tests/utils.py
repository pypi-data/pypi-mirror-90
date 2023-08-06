import re
import os
import shutil
from unittest.mock import patch
import difflib
import unittest
import mys.cli

class TestCase(unittest.TestCase):

    maxDiff = None

    def assert_in(self, needle, haystack):
        try:
            self.assertIn(needle, haystack)
        except AssertionError:
            differ = difflib.Differ()
            diff = differ.compare(needle.splitlines(), haystack.splitlines())

            raise AssertionError(
                '\n' + '\n'.join([diffline.rstrip('\n') for diffline in diff]))

def read_file(filename):
    with open(filename, 'r') as fin:
        return fin.read()

def remove_directory(name):
    if os.path.exists(name):
        shutil.rmtree(name)

def remove_ansi(string):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')

    return ansi_escape.sub('', string)

def remove_build_directory(name):
    remove_directory('tests/build/' + name)

def create_new_package(package_name):
    with Path('tests/build'):
        remove_directory(package_name)

        command = [
            'mys', '-d', 'new',
            '--author', 'Test Er <test.er@mys.com>',
            package_name
        ]

        with patch('sys.argv', command):
            mys.cli.main()

def create_new_package_with_files(package_name, module_name, src_module_name=None):
    if src_module_name is None:
        src_module_name = module_name

    create_new_package(package_name)

    with Path('tests/build'):
        os.remove(f'{package_name}/src/lib.mys')
        os.remove(f'{package_name}/src/main.mys')
        shutil.copyfile(f'../../tests/files/{module_name}.mys',
                        f'{package_name}/src/{src_module_name}.mys')

def test_package(package_name):
    with Path('tests/build/' + package_name):
        with patch('sys.argv', ['mys', '--debug', 'test', '--verbose']):
            mys.cli.main()

def build_and_test_module(module_name):
    package_name = f'test_{module_name}'
    create_new_package_with_files(package_name, module_name)
    test_package(package_name)

class Path:

    def __init__(self, new_dir):
        self.new_dir = new_dir
        self.old_dir = None

    def __enter__(self):
        self.old_dir = os.getcwd()
        os.chdir(self.new_dir)

        return self

    def __exit__(self, *args, **kwargs):
        os.chdir(self.old_dir)

        return False


class EnvVar:    

    def __init__(self, name, new_value):
        self.name = name
        self.new_value = new_value
        self.old_value = None

    def __enter__(self):
        self.old_value = os.getenv(self.name, None)
        os.environ[self.name] = self.new_value

        return self

    def __exit__(self, *args, **kwargs):
        if self.old_value is None:
            del os.environ[self.name]
        else:
            os.environ[self.name] = self.old_value

        return False
