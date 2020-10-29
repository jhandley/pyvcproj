import filecmp
import tempfile

import pytest

import vcproj.solution


@pytest.fixture(scope='session')
def test_sol():
    return vcproj.solution.parse('vcproj/tests/test_solution/test.sln')


def test_project_files(test_sol):
    assert list(test_sol.project_files()) == ['test\\test.vcxproj', 'lib1\\lib1.vcxproj', 'lib2\\lib2.vcxproj']


def test_dependencies(test_sol):
    assert list(test_sol.dependencies('test')) == ['lib1', 'lib2']


def test_project_names(test_sol):
    assert list(test_sol.project_names()) == ['test', 'lib1', 'lib2']


def test_set_dependencies(test_sol):
    test_sol.set_dependencies('lib1', ['lib2'])
    assert list(test_sol.dependencies('lib1')) == ['lib2']


def test_write():
    s = vcproj.solution.parse('vcproj/tests/test_solution/test.sln')
    temp = tempfile.NamedTemporaryFile()
    temp.close()
    s.write(temp.name)
    assert filecmp.cmp('vcproj/tests/test_solution/test.sln', temp.name)
