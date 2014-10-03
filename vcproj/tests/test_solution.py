import vcproj.solution

def test_projects():
    s = vcproj.solution.parse('vcproj/tests/test_solution/test.sln')
    assert list(s.projects()) == ['test\\test.vcxproj', 'lib1\\lib1.vcxproj', 'lib2\\lib2.vcxproj']
    

