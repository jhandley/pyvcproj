import vcproj.solution
import tempfile, filecmp
import pytest

@pytest.fixture(scope="session")
def test_sol():
    return vcproj.solution.parse('vcproj/tests/test_solution/vc15sol/vc15sol.sln')


def test_all_projects(test_sol):
    projects = test_sol.project_names()
    len(list(projects)) == 59


def test_project_names(test_sol):
    projects = test_sol.project_names()
    assert 'Helper' in projects
    assert 'MDraw' in projects


def test_project_files(test_sol):

    proj_files = list(test_sol.project_files())

    assert 'PrivateLib\\PrivateLib.vcxproj' in proj_files
    assert 'Helper\\Helper.vcxproj' in proj_files
    assert 'Resource\\Resource.vcxproj' in proj_files


def test_dependencies(test_sol):

    deps = list(test_sol.dependencies('DXHHTest'))

    assert deps == ['Public', 'MDraw']
    
def test_set_dependencies():
    s = vcproj.solution.parse('vcproj/tests/test_solution/test.sln')
    s.set_dependencies('lib1', ['lib2'])
    assert list(s.dependencies('lib1')) == ['lib2']

def test_write():
    s = vcproj.solution.parse('vcproj/tests/test_solution/test.sln')
    temp = tempfile.NamedTemporaryFile()
    temp.close()
    s.write(temp.name)
    assert filecmp.cmp('vcproj/tests/test_solution/test.sln', temp.name)
    
    
