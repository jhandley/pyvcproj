import vcproj.project

def test_source_files():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert(list(p.source_files()) == ['stdafx.cpp', 'test.cpp'])

def test_include_files():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert(list(p.include_files()) == ['Resource.h', 'stdafx.h', 'targetver.h', 'test.h'])

def test_additional_link_dependencies():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert(p.additional_link_dependencies('Debug', 'Win32') ==
           ['somethingextra.lib', 'kernel32.lib', 'user32.lib', 'gdi32.lib', 'winspool.lib', 'comdlg32.lib', 'advapi32.lib', 'shell32.lib', 'ole32.lib', 'oleaut32.lib', 'uuid.lib', 'odbc32.lib', 'odbccp32.lib', '%(AdditionalDependencies)'])
    assert(p.additional_link_dependencies('Release', 'Win32') ==
           ['somethingextra.lib', 'somethingelse.lib', 'kernel32.lib', 'user32.lib', 'gdi32.lib', 'winspool.lib', 'comdlg32.lib', 'advapi32.lib', 'shell32.lib', 'ole32.lib', 'oleaut32.lib', 'uuid.lib', 'odbc32.lib', 'odbccp32.lib', '%(AdditionalDependencies)'])
    assert(p.additional_link_dependencies('Foo', 'Win32') == [])

def test_additional_include_directories():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert(p.additional_include_directories('Debug', 'Win32') == ['..', 'foo/bar'])
    assert(p.additional_include_directories('Release', 'Win32') == [])
    assert(p.additional_include_directories('Foo', 'Win32') == [])
