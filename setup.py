#!/usr/bin/env python

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='vcproj',
    version='0.1.0',
    description='Manipulate Visual C++ Project Files',
    author='Josh Handley',
    author_email='josh@teleyah.com',
    tests_require=['pytest'],
    url='http://github.com/jhandley/pyvcproj',
    py_modules=['vcproj'],
    packages=['vcproj'],
    cmdclass={'test': PyTest},
    python_requires='>=3.6',
)
