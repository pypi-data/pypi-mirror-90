import shutil
import sys
import subprocess
import os
import difflib
import unittest
from unittest.mock import patch
from unittest.mock import call
from unittest.mock import Mock
from io import StringIO

import mys.cli

from .utils import read_file
from .utils import remove_directory
from .utils import remove_files
from .utils import remove_ansi

class Test(unittest.TestCase):

    maxDiff = None

    def assert_in(self, needle, haystack):
        try:
            self.assertIn(needle, haystack)
        except AssertionError:
            differ = difflib.Differ()
            diff = differ.compare(needle.splitlines(), haystack.splitlines())

            raise AssertionError(
                '\n' + '\n'.join([diffline.rstrip('\n') for diffline in diff]))

    def setUp(self):
        print()

    def tearDown(self):
        print()

    def build_and_test_module(self, module_name):
        package_name = f'test_{module_name}'
        remove_directory(package_name)
        command = [
            'mys', 'new',
            '--author', 'Test Er <test.er@mys.com>',
            package_name
        ]

        with patch('sys.argv', command):
            mys.cli.main()

        shutil.copyfile(f'tests/files/{module_name}.mys',
                        f'{package_name}/src/{module_name}.mys')
        os.remove(f'{package_name}/src/lib.mys')
        os.remove(f'{package_name}/src/main.mys')

        # Enter the package directory.
        path = os.getcwd()
        os.chdir(package_name)

        try:
            # Test.
            with patch('sys.argv', ['mys', '--debug', 'test', '--verbose']):
                mys.cli.main()
        finally:
            os.chdir(path)

    def test_calc(self):
        self.build_and_test_module('calc')

    def test_enums(self):
        self.build_and_test_module('enums')

    def test_hello_world(self):
        self.build_and_test_module('hello_world')

    def test_loops(self):
        self.build_and_test_module('loops')

    def test_various_1(self):
        self.build_and_test_module('various_1')

    def test_various_2(self):
        self.build_and_test_module('various_2')

    def test_various_3(self):
        self.build_and_test_module('various_3')

    def test_special_symbols(self):
        self.build_and_test_module('special_symbols')

    def test_imports(self):
        # Enter the package directory.
        path = os.getcwd()
        os.chdir('tests/files/imports/mypkg')

        try:
            # Clean.
            with patch('sys.argv', ['mys', 'clean']):
                mys.cli.main()

            # Build.
            with patch('sys.argv', ['mys', 'test', '-v']):
                mys.cli.main()
        finally:
            os.chdir(path)

    def test_print(self):
        package_name = 'test_print'
        remove_directory(package_name)
        command = [
            'mys', 'new',
            '--author', 'Test Er <test.er@mys.com>',
            package_name
        ]

        with patch('sys.argv', command):
            mys.cli.main()

        module_name = 'print'
        shutil.copyfile(f'tests/files/{module_name}.mys',
                        f'{package_name}/src/main.mys')
        os.remove(f'{package_name}/src/lib.mys')

        # Enter the package directory.
        path = os.getcwd()
        os.chdir(package_name)

        try:
            # Run.
            env = os.environ
            env['PYTHONPATH'] = path
            proc = subprocess.run([sys.executable, '-m', 'mys', 'run'],
                                  input="Lobster #1\n10\n",
                                  capture_output=True,
                                  text=True,
                                  env=env)

            if proc.returncode != 0:
                print(proc.stdout)
                print(proc.stderr)

                raise Exception("Build error.")

            output = remove_ansi(proc.stdout)

            self.assert_in(
                'A string literal!\n'
                '1\n'
                '1.5\n'
                'False\n'
                'True\n'
                'Foo(v=5)\n'
                '(-500, "Hi!")\n'
                '[1, 2, 3]\n'
                'Bar(a=Foo(v=3), b=True, c="kalle")\n'
                'Foo(v=5)\n'
                '[(Foo(v=3), True), (Foo(v=5), False)]\n'
                'True\n'
                'False\n'
                'True\n'
                'None\n'
                'Fie(a=5, _b=False, _c=None)\n'
                'G\n'
                '7\n'
                "['j', 'u', 'l']\n"
                'Fam(x=None)\n'
                'Fam(x=Foo(v=4))\n'
                'Fam(x=Bar(a=None, b=False, c="kk"))\n'
                'Foo(v=-1)\n'
                'Bar(a=None, b=True, c="")\n'
                '[Foo(v=5), Bar(a=None, b=True, c="fes")]\n'
                'b""\n'
                'b"\\x01\\x02\\x03"!\n'
                '20\n'
                '1\n' # Todo: Should print "Animal.Cow".
                'Name: Lobster #1\n'
                'Age: 10\n',
                output)
            self.assertTrue(('{1: 2, 3: 4}\n' in output)
                            or ('{3: 4, 1: 2}\n' in output))
            self.assertTrue(('{ho: Foo(v=4), hi: Foo(v=5)}\n' in output)
                            or ('{"hi": Foo(v=5), "ho": Foo(v=4)}\n' in output))

        finally:
            os.chdir(path)
