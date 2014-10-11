import vcproj.solution
import tempfile, filecmp

def test_project_names():
    s = vcproj.solution.parse('vcproj/tests/test_solution/test.sln')
    assert list(s.project_names()) == ['test', 'lib1', 'lib2']

def test_project_files():
    s = vcproj.solution.parse('vcproj/tests/test_solution/test.sln')
    assert list(s.project_files()) == ['test\\test.vcxproj', 'lib1\\lib1.vcxproj', 'lib2\\lib2.vcxproj']
    
def test_dependencies():
    s = vcproj.solution.parse('vcproj/tests/test_solution/test.sln')
    assert list(s.dependencies('test')) == ['lib1', 'lib2']
    
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
    
    
