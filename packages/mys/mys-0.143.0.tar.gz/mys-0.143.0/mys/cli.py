import time
import tarfile
import re
import subprocess
import os
import sys
import argparse
import shutil
from traceback import print_exc
from tempfile import TemporaryDirectory
import getpass
import glob
import multiprocessing
import json
import toml
import yaspin
from colors import yellow
from colors import red
from colors import green
from colors import cyan
from colors import strip_color
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PythonLexer
from humanfriendly import format_timespan
from .transpile import transpile
from .transpile import Source
from .version import __version__

MYS_DIR = os.path.dirname(os.path.realpath(__file__))

DOWNLOAD_DIRECTORY = 'build/dependencies'

BULB = '💡'
INFO = 'ℹ️'
ERROR = '❌️'

OPTIMIZE = {
    'speed': '3',
    'size': 's',
    'debug': '0'
}

PACKAGE_TOML_FMT = '''\
[package]
name = "{package_name}"
version = "0.1.0"
authors = [{authors}]
description = "Add a short package description here."

[dependencies]
# foobar = "*"
'''

GITIGNORE = '''\
/build
'''

GITATTRIBUTES = '''\
*.mys linguist-language=python
'''

README_FMT = '''\
{title}
{line}

This package provides...

Examples
========

.. code-block:: python

   from {package_name} import add

   def main():
       print('1 + 2 =', add(1, 2))
'''

LICENSE = '''\
The MIT License (MIT)

Copyright (c) 2020 Mys Lang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

LIB_MYS = '''\
def add(first: i32, second: i32) -> i32:
    return first + second

@test
def test_add():
    assert add(1, 2) == 3
'''

MAIN_MYS_FMT = '''\
def main():
    print("Hello, world!")
'''

MAKEFILE_FMT = '''\
MYS_CXX ?= {ccache}$(CXX)
MYS ?= mys
CFLAGS += -Ibuild
CFLAGS += -I{mys_dir}/lib
CFLAGS += -Ibuild/transpiled/include
# CFLAGS += -Wall
CFLAGS += -Wno-unused-variable
CFLAGS += -Wno-unused-value
# CFLAGS += -Wno-parentheses-equality
CFLAGS += -Wno-unused-but-set-variable
CFLAGS += -O{optimize}
CFLAGS += -std=c++17
CFLAGS += -fdata-sections
CFLAGS += -ffunction-sections
CFLAGS += -fdiagnostics-color=always
ifeq ($(TEST), yes)
CFLAGS += -DMYS_TEST
OBJ_SUFFIX = test.o
else
ifeq ($(APPLICATION), yes)
CFLAGS += -DMYS_APPLICATION
endif
OBJ_SUFFIX = o
endif
LDFLAGS += -std=c++17
# LDFLAGS += -static
# LDFLAGS += -Wl,--gc-sections
LDFLAGS += -fdiagnostics-color=always
{transpiled_cpp}
{objs}
EXE = build/app
TEST_EXE = build/test

all:
\t$(MAKE) -f build/Makefile build/transpile
\t$(MAKE) -f build/Makefile {all_deps}

test:
\t$(MAKE) -f build/Makefile build/transpile
\t$(MAKE) -f build/Makefile $(TEST_EXE)

build/transpile: {transpile_srcs_paths}
\t$(MYS) $(TRANSPILE_DEBUG) transpile {transpile_options} -o build/transpiled {transpile_srcs}
\ttouch $@

$(TEST_EXE): $(OBJ) build/mys.$(OBJ_SUFFIX)
\t$(MYS_CXX) $(LDFLAGS) -o $@ $^

$(EXE): $(OBJ) build/mys.$(OBJ_SUFFIX)
\t$(MYS_CXX) $(LDFLAGS) -o $@ $^

%.mys.$(OBJ_SUFFIX): %.mys.cpp build/mys.hpp.gch
\t$(MYS_CXX) $(CFLAGS) -c $< -o $@

build/mys.hpp.gch: {mys_dir}/lib/mys.hpp
\t$(MYS_CXX) $(CFLAGS) -c $< -o $@

build/mys.$(OBJ_SUFFIX): {mys_dir}/lib/mys.cpp build/mys.hpp.gch
\t$(MYS_CXX) $(CFLAGS) -c $< -o $@
'''

TEST_MYS_FMT = '''\
{imports}

def main():
    passed: int = 0
    failed: int = 0
    total: int = 0
{tests}

    print('Passed:', passed)
    print('Failed:', failed)
    print('Total:', total)

    if failed > 0:
        raise Exception()
'''

TEST_FMT = '''\
    try:
        total += 1
        {test}()
        passed += 1
    except Exception as e:
        print(e)
        failed += 1
'''

TRANSPILE_OPTIONS_FMT = '-n {package_name} -p {package_path} {flags}'

SETUP_PY_FMT = '''\
from setuptools import setup


setup(name='{name}',
      version='{version}',
      description='{description}',
      long_description=open('README.rst', 'r').read(),
      author={author},
      author_email={author_email},
      install_requires={dependencies})
'''

MANIFEST_IN = '''\
include package.toml
recursive-include src *.mys
'''


class BadPackageNameError(Exception):
    pass


def default_jobs():
    return max(1, multiprocessing.cpu_count() - 1)


def duration_start():
    return time.time()


def duration_stop(start_time):
    end_time = time.time()
    duration = format_timespan(end_time - start_time)

    return f' ({duration})'


def box_print(lines, icon, width=None):
    if width is None:
        width = 0

        for line in lines:
            width = max(width, len(strip_color(line)))

    print(f'┌{"─" * (width - 3)} {icon} ─┐')

    for line in lines:
        w = width - len(strip_color(line))
        print(f'│ {line}{" " * w} │')

    print(f'└{"─" * (width + 2)}┘')


SPINNER = [
    ' ⠋', ' ⠙', ' ⠹', ' ⠸', ' ⠼', ' ⠴', ' ⠦', ' ⠧', ' ⠇', ' ⠏'
]


class Spinner(yaspin.api.Yaspin):

    def __init__(self, text):
        super().__init__(yaspin.Spinner(SPINNER, 80), text=text, color='yellow')
        self._start_time = duration_start()

    def __exit__(self, exc_type, exc_val, traceback):
        duration = duration_stop(self._start_time)

        if exc_type is None:
            self.write(green(' ✔ ') + self.text + duration)
        else:
            self.write(red(' ✘ ') + self.text + duration)

        return super().__exit__(exc_type, exc_val, traceback)


def run_with_spinner(command, message, env=None):
    output = ''

    try:
        with Spinner(text=message):
            result = subprocess.run(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    encoding='utf-8',
                                    env=env)
            output = result.stdout
            result.check_returncode()
    except Exception:
        lines = []

        for line in output.splitlines():
            if 'make: *** ' in line:
                continue

            lines.append(line)

        raise Exception('\n'.join(lines).rstrip())


def run(command, message, verbose, env=None):
    if verbose:
        start_time = duration_start()

        try:
            subprocess.run(command, check=True, env=env)
            print(green(' ✔ ') + message + duration_stop(start_time))
        except Exception:
            print(red(' ✘ ') + message + duration_stop(start_time))
            raise
    else:
        run_with_spinner(command, message, env)


def git_config_get(item, default=None):
    try:
        return subprocess.check_output(['git', 'config', '--get', item],
                                       encoding='utf-8').strip()
    except Exception:
        return default


def find_authors(authors):
    if authors is not None:
        return ', '.join([f'"{author}"'for author in authors])

    user = git_config_get('user.name', getpass.getuser())
    email = git_config_get('user.email', f'{user}@example.com')

    return f'"{user} <{email}>"'


def validate_package_name(package_name):
    if not re.match(r'^[a-z][a-z0-9_]*$', package_name):
        raise BadPackageNameError()


def do_new(_parser, args):
    package_name = os.path.basename(args.path)
    authors = find_authors(args.authors)

    try:
        with Spinner(text=f"Creating package {package_name}"):
            validate_package_name(package_name)

            os.makedirs(args.path)
            path = os.getcwd()
            os.chdir(args.path)

            try:
                with open('package.toml', 'w') as fout:
                    fout.write(PACKAGE_TOML_FMT.format(package_name=package_name,
                                                       authors=authors))

                with open('.gitignore', 'w') as fout:
                    fout.write(GITIGNORE)

                with open('.gitattributes', 'w') as fout:
                    fout.write(GITATTRIBUTES)

                with open('README.rst', 'w') as fout:
                    fout.write(README_FMT.format(
                        package_name=package_name,
                        title=package_name.replace('_', ' ').title(),
                        line='=' * len(package_name)))

                with open('LICENSE', 'w') as fout:
                    fout.write(LICENSE)

                shutil.copyfile(os.path.join(MYS_DIR, 'lint/pylintrc'), 'pylintrc')
                os.mkdir('src')

                with open('src/lib.mys', 'w') as fout:
                    fout.write(LIB_MYS)

                with open('src/main.mys', 'w') as fout:
                    fout.write(MAIN_MYS_FMT.format(package_name=package_name))
            finally:
                os.chdir(path)
    except BadPackageNameError:
        box_print(['Package names must start with a letter and only',
                   'contain letters, numbers and underscores. Only lower',
                   'case letters are allowed.',
                   '',
                   'Here are a few examples:',
                   '',
                   f'{cyan("mys new foo")}'
                   f'{cyan("mys new f1")}'
                   f'{cyan("mys new foo_bar")}'],
                  ERROR)
        raise Exception()

    cd = cyan(f'cd {package_name}')

    box_print(['Build and run the new package by typing:',
               '',
               f'{cd}',
               f'{cyan("mys run")}'],
              BULB,
              width=53)


class Author:

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Config:

    def __init__(self):
        self.authors = []
        self.config = self.load_package_configuration()

    def load_package_configuration(self):
        with open('package.toml') as fin:
            config = toml.loads(fin.read())

        package = config.get('package')

        if package is None:
            raise Exception("'[package]' not found in package.toml.")

        for name in ['name', 'version', 'authors']:
            if name not in package:
                raise Exception(f"'[package].{name}' not found in package.toml.")

        for author in package['authors']:
            mo = re.match(r'^([^<]+)<([^>]+)>$', author)

            if not mo:
                raise Exception(f"Bad author '{author}'.")

            self.authors.append(Author(mo.group(1).strip(), mo.group(2).strip()))

        if 'description' not in package:
            package['description'] = ''

        if 'dependencies' not in config:
            config['dependencies'] = {}

        return config

    def __getitem__(self, key):
        return self.config[key]


def setup_build():
    os.makedirs('build/transpiled', exist_ok=True)
    os.makedirs('build/dependencies', exist_ok=True)


def rename_one_matching(pattern, to):
    paths = glob.glob(pattern)

    if len(paths) != 1:
        raise Exception(
            f'{len(paths)} paths are matching when expecting exactly one to match')

    os.rename(paths[0], to)


def prepare_download_dependency_from_registry(name, version):
    if version == '*':
        archive = f'mys-{name}-latest.tar.gz'
        package_specifier = f'mys-{name}'
    else:
        archive = f'mys-{name}-{version}.tar.gz'
        package_specifier = f'mys-{name}=={version}'

    archive_path = f'build/dependencies/{archive}'

    if os.path.exists(archive_path):
        return None
    else:
        return (name, version, package_specifier, archive, archive_path)


def extract_dependency(verbose, name, version, archive, archive_path):
    if version == '*':
        rename_one_matching(os.path.join(DOWNLOAD_DIRECTORY, f'mys-{name}-*.tar.gz'),
                            archive_path)

    with Spinner(text=f"Extracting {archive}"):
        with tarfile.open(archive_path) as fin:
            fin.extractall(DOWNLOAD_DIRECTORY)

    if version == '*':
        rename_one_matching(os.path.join(DOWNLOAD_DIRECTORY, f'mys-{name}-*/'),
                            os.path.join(DOWNLOAD_DIRECTORY, f'mys-{name}-latest'))


def download_dependencies(config, verbose):
    packages = []

    for name, info in config['dependencies'].items():
        if isinstance(info, str):
            package = prepare_download_dependency_from_registry(name, info)

            if package is not None:
                packages.append(package)

    if not packages:
        return

    command = [
        sys.executable, '-m', 'pip', 'download',
        '-d', DOWNLOAD_DIRECTORY
    ]
    command += [package_specifier for _, _, package_specifier, _, _ in packages]
    run(command, f"Downloading dependencies", verbose)

    for name, version, _, archive, archive_path in packages:
        extract_dependency(verbose, name, version, archive, archive_path)

def read_package_configuration():
    try:
        with Spinner('Reading package configuration'):
            return Config()
    except FileNotFoundError:
        box_print([
            'Current directory does not contain a Mys package (package.toml does',
            'not exist).',
            '',
            'Please enter a Mys package directory, and try again.',
            '',
            f'You can create a new package with {cyan("mys new <name>")}.'],
                  BULB)

        raise Exception()


def find_package_sources(package_name, path, ignore_main=False):
    srcs = []
    oldpath = os.getcwd()
    os.chdir(os.path.join(path, 'src'))

    try:
        for src in glob.glob('**/*.mys', recursive=True):
            if ignore_main and src == 'main.mys':
                continue

            srcs.append((package_name, path, src, os.path.join(path, 'src', src)))
    finally:
        os.chdir(oldpath)

    return srcs


def dependency_path(dependency_name, config):
    for package_name, info in config['dependencies'].items():
        if package_name == dependency_name:
            if isinstance(info, str):
                if info == '*':
                    return f'build/dependencies/mys-{package_name}-latest/'
                else:
                    return f'build/dependencies/mys-{package_name}-{info}/'
            elif 'path' in info:
                return info['path']
            else:
                raise Exception('Bad dependency format.')

    raise Exception(f'Bad dependency {dependency_name}.')


def find_dependency_sources(config):
    srcs = []

    for package_name in config['dependencies']:
        path = dependency_path(package_name, config)
        srcs += find_package_sources(package_name, path, ignore_main=True)

    return srcs


def create_makefile(config, optimize, no_ccache):
    srcs = find_package_sources(config['package']['name'], '.')

    if not srcs:
        box_print(["'src/' is empty. Please create one or more .mys-files."], ERROR)

        raise Exception()

    srcs += find_dependency_sources(config)

    transpile_options = []
    transpile_srcs = []
    transpile_srcs_paths = []
    objs = []
    is_application = False
    transpiled_cpp = []

    for package_name, package_path, src, _path in srcs:
        flags = []

        if package_name != config['package']['name']:
            flags.append('-s yes')
        else:
            flags.append('-s no')

        if src == 'main.mys':
            is_application = True
            flags.append('-m yes')
        else:
            flags.append('-m no')

        flags = ' '.join(flags)

        module_path = f'build/transpiled/src/{package_name}/{src}'
        transpile_options.append(
            TRANSPILE_OPTIONS_FMT.format(package_name=package_name,
                                         package_path=package_path,
                                         flags=flags))

        transpile_srcs.append(src)
        transpile_srcs_paths.append(os.path.join(package_path, 'src', src))
        objs.append(f'OBJ += {module_path}.$(OBJ_SUFFIX)')
        transpiled_cpp.append(f'SRC += {module_path}.cpp')

    if is_application:
        all_deps = '$(EXE)'
    else:
        all_deps = '$(OBJ)'

    if not no_ccache and shutil.which('ccache'):
        ccache = 'ccache '
    else:
        ccache = ''

    with open('build/Makefile', 'w') as fout:
        fout.write(
            MAKEFILE_FMT.format(mys_dir=MYS_DIR,
                                ccache=ccache,
                                objs='\n'.join(objs),
                                optimize=OPTIMIZE[optimize],
                                transpile_options=' '.join(transpile_options),
                                transpile_srcs_paths=' '.join(transpile_srcs_paths),
                                transpile_srcs=' '.join(transpile_srcs),
                                all_deps=all_deps,
                                package_name=config['package']['name'],
                                transpiled_cpp='\n'.join(transpiled_cpp)))

    return is_application


def build_prepare(verbose, optimize, no_ccache):
    config = read_package_configuration()

    if not os.path.exists('build/Makefile'):
        setup_build()

    download_dependencies(config, verbose)

    return create_makefile(config, optimize, no_ccache), config


def build_app(debug, verbose, jobs, is_application):
    command = ['make', '-f', 'build/Makefile', '-j', str(jobs), 'all']

    if debug:
        command += ['TRANSPILE_DEBUG=--debug']

    if not verbose:
        command += ['-s']

    if is_application:
        command += ['APPLICATION=yes']

    run(command, 'Building', verbose)


def do_build(_parser, args):
    is_application, _ = build_prepare(args.verbose, args.optimize, args.no_ccache)
    build_app(args.debug, args.verbose, args.jobs, is_application)


def run_app(args, verbose):
    if verbose:
        print('./build/app')

    subprocess.run(['./build/app'] + args, check=True)


def style_source(code):
    return highlight(code,
                     PythonLexer(),
                     Terminal256Formatter(style='monokai')).rstrip()


def do_run(_parser, args):
    if build_prepare(args.verbose, args.optimize, args.no_ccache)[0]:
        build_app(args.debug, args.verbose, args.jobs, True)
        run_app(args.args, args.verbose)
    else:
        main_1 = style_source('def main():\n')
        main_2 = style_source("    print('Hello, world!')\n")
        func = style_source('main()')
        box_print([
            f"This package is not executable. Create '{cyan('src/main.mys')}' and",
            f"implement '{func}' to make the package executable.",
            '',
            main_1,
            main_2], BULB)

        raise Exception()


def do_test(_parser, args):
    build_prepare(args.verbose, args.optimize, args.no_ccache)
    command = [
        'make', '-f', 'build/Makefile', '-j', str(args.jobs), 'test', 'TEST=yes'
    ]

    if args.debug:
        command += ['TRANSPILE_DEBUG=--debug']

    run(command, 'Building tests', args.verbose)
    run(['./build/test'], 'Running tests', args.verbose)


def do_clean(_parser, args):
    read_package_configuration()

    with Spinner(text='Cleaning'):
        shutil.rmtree('build', ignore_errors=True)


def print_lint_message(message):
    location = f'{message["path"]}:{message["line"]}:{message["column"]}'
    level = message['type'].upper()
    symbol = message["symbol"]
    message = message["message"]

    if level == 'ERROR':
        level = red(level, style='bold')
    elif level == 'WARNING':
        level = yellow(level, style='bold')
    else:
        level = cyan(level, style='bold')

    print(f'{location} {level} {message} ({symbol})')


def do_lint(_parser, args):
    read_package_configuration()
    output = ''
    returncode = 1

    try:
        with Spinner('Linting'):
            proc = subprocess.run([sys.executable, '-m', 'pylint',
                                   '-j', str(args.jobs),
                                   '--output-format', 'json'
                                   ] + glob.glob('src/**/*.mys', recursive=True),
                                  stdout=subprocess.PIPE)
            output = proc.stdout.decode()
            returncode = proc.returncode
            proc.check_returncode()
    except Exception:
        pass

    for item in json.loads(output):
        print_lint_message(item)

    if returncode != 0:
        raise Exception()


def do_transpile(_parser, args):
    sources = []

    for i, mysfile in enumerate(args.mysfiles):
        mys_path = os.path.join(args.package_path[i], 'src', mysfile)
        module_hpp = os.path.join(args.package_name[i], mysfile + '.hpp')
        module = '.'.join(module_hpp[:-8].split('/'))
        hpp_path = os.path.join(args.outdir, 'include', module_hpp)
        cpp_path = os.path.join(args.outdir,
                                'src',
                                args.package_name[i],
                                mysfile + '.cpp')

        with open(mys_path, 'r') as fin:
            sources.append(Source(fin.read(),
                                  mysfile,
                                  module,
                                  mys_path,
                                  module_hpp,
                                  args.skip_tests[i] == 'yes',
                                  hpp_path,
                                  cpp_path,
                                  args.main[i] == 'yes'))

    generated = transpile(sources)

    for source, (hpp_code, cpp_code) in zip(sources, generated):
        os.makedirs(os.path.dirname(source.hpp_path), exist_ok=True)
        os.makedirs(os.path.dirname(source.cpp_path), exist_ok=True)

        with open(source.hpp_path, 'w') as fout:
            fout.write(hpp_code)

        with open(source.cpp_path, 'w') as fout:
            fout.write(cpp_code)


def publish_create_release_package(config, verbose, archive):
    with open('setup.py', 'w') as fout:
        fout.write(SETUP_PY_FMT.format(
            name=f"mys-{config['package']['name']}",
            version=config['package']['version'],
            description=config['package']['description'],
            author="'" + ', '.join(
                [author.name for author in config.authors]) + "'",
            author_email="'" + ', '.join(
                [author.email for author in config.authors]) + "'",
            dependencies='[]'))

    with open('MANIFEST.in', 'w') as fout:
        fout.write(MANIFEST_IN)

    shutil.copytree('../../src', 'src')
    shutil.copy('../../package.toml', 'package.toml')
    shutil.copy('../../README.rst', 'README.rst')
    run([sys.executable, 'setup.py', 'sdist'], f'Creating {archive}', verbose)


def publish_upload_release_package(verbose, username, password, archive):
    # Try to hide the password.
    env = os.environ.copy()

    if username is None:
        username = input('Username: ')

    if password is None:
        password = getpass.getpass()

    env['TWINE_USERNAME'] = username
    env['TWINE_PASSWORD'] = password
    command = [sys.executable, '-m', 'twine', 'upload']

    if verbose:
        command += ['--verbose']

    command += glob.glob('dist/*')

    run(command, f'Uploading {archive}', verbose, env=env)


def do_publish(_parser, args):
    config = read_package_configuration()

    box_print([
        "Mys is currently using Python's Package Index (PyPI). A PyPI",
        'account is required to publish your package.'], INFO)

    publish_dir = 'build/publish'
    shutil.rmtree(publish_dir, ignore_errors=True)
    os.makedirs(publish_dir)
    path = os.getcwd()
    os.chdir(publish_dir)

    try:
        name = config['package']['name']
        version = config['package']['version']
        archive = f"mys-{name}-{version}.tar.gz"
        publish_create_release_package(config, args.verbose, archive)
        publish_upload_release_package(args.verbose,
                                       args.username,
                                       args.password,
                                       archive)
    finally:
        os.chdir(path)


def install_clean():
    if not os.path.exists('package.toml'):
        raise Exception('not a package')

    with Spinner(text='Cleaning'):
        shutil.rmtree('build', ignore_errors=True)

def install_download(args):
    command = [
        sys.executable, '-m', 'pip', 'download', f'mys-{args.package}'
    ]
    run(command, f"Downloading package", args.verbose)


def install_extract():
    archive = glob.glob('mys-*.tar.gz')[0]

    with Spinner(text=f"Extracting package"):
        with tarfile.open(archive) as fin:
            fin.extractall()

    os.remove(archive)


def install_build(args):
    is_application, config = build_prepare(args.verbose, 'speed', args.no_ccache)

    if not is_application:
        raise Exception('not an application')

    build_app(args.debug, args.verbose, args.jobs, is_application)

    return config

def install_install(root, args, config):
    bin_dir = os.path.join(root, 'bin')
    src_file = 'build/app'
    dst_file = os.path.join(bin_dir, config['package']['name'])

    with Spinner(text=f"Copying binary to {bin_dir}"):
        os.makedirs(bin_dir, exist_ok=True)
        shutil.copyfile(src_file, dst_file)
        shutil.copymode(src_file, dst_file)


def install_from_current_dirctory(args, root):
    install_clean()
    config = install_build(args)
    install_install(root, args, config)


def install_from_registry(args, root):
    with TemporaryDirectory()as tmp_dir:
        os.chdir(tmp_dir)
        install_download(args)
        install_extract()
        os.chdir(glob.glob('mys-*')[0])
        config = install_build(args)
        install_install(root, args, config)


def do_install(parser, args):
    root = os.path.abspath(os.path.expanduser(args.root))

    if args.package is None:
        install_from_current_dirctory(args, root)
    else:
        install_from_registry(args, root)


def do_style(_parser, _args):
    read_package_configuration()

    box_print(['This subcommand is not yet implemented.'], ERROR)

    raise Exception()


def do_help(parser, _args):
    parser.print_help()


DESCRIPTION = f'''\
The Mys programming language package manager.

Available subcommands are:

    {cyan('new')}      Create a new package.
    {cyan('build')}    Build the appliaction.
    {cyan('run')}      Build and run the application.
    {cyan('test')}     Build and run tests
    {cyan('clean')}    Remove build output.
    {cyan('lint')}     Perform static code analysis.
    {cyan('publish')}  Publish a release.
    {cyan('install')}  Install an application from local package or registry.'
'''


def add_verbose_argument(subparser):
    subparser.add_argument('-v', '--verbose',
                           action='store_true',
                           help='Verbose output.')


def add_jobs_argument(subparser):
    subparser.add_argument(
        '-j', '--jobs',
        type=int,
        default=default_jobs(),
        help='Maximum number of parallel jobs (default: %(default)s).')


def add_optimize_argument(subparser, default):
    subparser.add_argument(
        '-o', '--optimize',
        default=default,
        choices=['speed', 'size', 'debug'],
        help='Optimize the build for given level (default: %(default)s).')


def add_no_ccache_argument(subparser):
    subparser.add_argument('-n', '--no-ccache',
                           action='store_true',
                           help='Do not use ccache.')


def main():
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('--version',
                        action='version',
                        version=__version__,
                        help='Print version information and exit.')

    subparsers = parser.add_subparsers(dest='subcommand',
                                       help='Subcommand to execute.',
                                       metavar='subcommand')

    # The new subparser.
    subparser = subparsers.add_parser(
        'new',
        description='Create a new package.')
    subparser.add_argument(
        '--author',
        dest='authors',
        action='append',
        help=("Package author as 'Mys Lang <mys.lang@example.com>'. May "
              "be given multiple times."))
    subparser.add_argument('path')
    subparser.set_defaults(func=do_new)

    # The build subparser.
    subparser = subparsers.add_parser(
        'build',
        description='Build the appliaction.')
    add_verbose_argument(subparser)
    add_jobs_argument(subparser)
    add_optimize_argument(subparser, 'speed')
    add_no_ccache_argument(subparser)
    subparser.set_defaults(func=do_build)

    # The run subparser.
    subparser = subparsers.add_parser(
        'run',
        description='Build and run the application.')
    add_verbose_argument(subparser)
    add_jobs_argument(subparser)
    add_optimize_argument(subparser, 'speed')
    add_no_ccache_argument(subparser)
    subparser.add_argument('args', nargs='*')
    subparser.set_defaults(func=do_run)

    # The test subparser.
    subparser = subparsers.add_parser(
        'test',
        description='Build and run tests.')
    add_verbose_argument(subparser)
    add_jobs_argument(subparser)
    add_optimize_argument(subparser, 'debug')
    add_no_ccache_argument(subparser)
    subparser.set_defaults(func=do_test)

    # The clean subparser.
    subparser = subparsers.add_parser(
        'clean',
        description='Remove build output.')
    subparser.set_defaults(func=do_clean)

    # The lint subparser.
    subparser = subparsers.add_parser(
        'lint',
        description='Perform static code analysis.')
    add_jobs_argument(subparser)
    subparser.set_defaults(func=do_lint)

    # The transpile subparser.
    subparser = subparsers.add_parser(
        'transpile',
        description='Transpile given Mys file(s) to C++ header and source files.')
    subparser.add_argument('-o', '--outdir',
                           default='.',
                           help='Output directory.')
    subparser.add_argument('-p', '--package-path',
                           required=True,
                           action='append',
                           help='Package path.')
    subparser.add_argument('-n', '--package-name',
                           required=True,
                           action='append',
                           help='Package name.')
    subparser.add_argument('-s', '--skip-tests',
                           action='append',
                           choices=['yes', 'no'],
                           help='Skip tests.')
    subparser.add_argument('-m', '--main',
                           action='append',
                           choices=['yes', 'no'],
                           help='Contains main().')
    subparser.add_argument('mysfiles', nargs='+')
    subparser.set_defaults(func=do_transpile)

    # The publish subparser.
    subparser = subparsers.add_parser(
        'publish',
        description='Publish a release.')
    add_verbose_argument(subparser)
    subparser.add_argument('-u', '--username',
                           help='Registry username.')
    subparser.add_argument('-p', '--password',
                           help='Registry password.')
    subparser.set_defaults(func=do_publish)

    # The install subparser.
    subparser = subparsers.add_parser(
        'install',
        description='Install an application from local package or registry.')
    add_verbose_argument(subparser)
    add_jobs_argument(subparser)
    add_no_ccache_argument(subparser)
    subparser.add_argument('--root',
                           default='~/.local',
                           help='Root folder to install into (default: %(default)s.')
    subparser.add_argument(
        'package',
        nargs='?',
        help=('Package to install application from. Installs current package if '
              'not given.'))
    subparser.set_defaults(func=do_install)

    # The style subparser.
    subparser = subparsers.add_parser(
        'style',
        description=(
            'Check that the package follows the Mys style guidelines. Automatically '
            'fixes trivial errors and prints the rest.'))
    subparser.set_defaults(func=do_style)

    # The help subparser.
    subparser = subparsers.add_parser(
        'help',
        description='Show this help.')
    subparser.set_defaults(func=do_help)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    try:
        args.func(parser, args)
    except Exception as e:
        if args.debug:
            print_exc()

        sys.exit(str(e))
    except KeyboardInterrupt:
        print()

        if args.debug:
            raise

        sys.exit(1)
