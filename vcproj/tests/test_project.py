import vcproj.project

def test_source_files():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert(list(p.source_files()) == ['stdafx.cpp', 'test.cpp'])

def test_include_files():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert(list(p.include_files()) == ['Resource.h', 'stdafx.h', 'targetver.h', 'test.h'])
