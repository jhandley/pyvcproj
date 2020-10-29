import vcproj.project


def test_source_files():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (list(p.source_files()) == ['stdafx.cpp', 'test.cpp'])


def test_include_files():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (list(p.include_files()) == ['Resource.h', 'stdafx.h', 'targetver.h', 'test.h'])


def test_configurations():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (list(p.configurations()) == [('Debug', 'Win32'), ('Release', 'Win32')])


def test_configuration_type():
    test = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (test.configuration_type() == 'Application')

    lib1 = vcproj.project.parse('vcproj/tests/test_solution/lib1/lib1.vcxproj')
    assert (lib1.configuration_type() == 'DynamicLibrary')

    lib2 = vcproj.project.parse('vcproj/tests/test_solution/lib2/lib2.vcxproj')
    assert (lib2.configuration_type() == 'StaticLibrary')


def test_additional_link_dependencies():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (p.additional_link_dependencies('Debug', 'Win32') ==
            ['somethingextra.lib', 'kernel32.lib', 'user32.lib', 'gdi32.lib', 'winspool.lib', 'comdlg32.lib', 'advapi32.lib', 'shell32.lib', 'ole32.lib', 'oleaut32.lib', 'uuid.lib', 'odbc32.lib', 'odbccp32.lib', '%(AdditionalDependencies)'])
    assert (p.additional_link_dependencies('Release', 'Win32') ==
            ['somethingextra.lib', 'somethingelse.lib', 'kernel32.lib', 'user32.lib', 'gdi32.lib', 'winspool.lib', 'comdlg32.lib', 'advapi32.lib', 'shell32.lib', 'ole32.lib', 'oleaut32.lib', 'uuid.lib', 'odbc32.lib', 'odbccp32.lib', '%(AdditionalDependencies)'])
    assert (p.additional_link_dependencies('Foo', 'Win32') is None)


def test_additional_include_directories():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (p.additional_include_directories('Debug', 'Win32') == ['..', 'foo/bar'])
    assert (p.additional_include_directories('Release', 'Win32') is None)
    assert (p.additional_include_directories('Foo', 'Win32') is None)


def test_set_additional_include_directories():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    p.set_additional_include_directories('Debug', 'Win32', ['foo', 'bar'])
    assert (p.additional_include_directories('Debug', 'Win32') == ['foo', 'bar'])

    p.set_additional_include_directories('All Configurations', 'All Configurations', ['blaa', 'blaaa'])
    assert (p.additional_include_directories('Release', 'Win32') == ['blaa', 'blaaa'])

    p.set_additional_include_directories('Release', 'Win32', None)
    assert (p.additional_include_directories('Release', 'Win32') is None)


def test_output_file():
    test = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (test.output_file('Debug', 'Win32') == '$(OutDir)test.exe')

    lib2 = vcproj.project.parse('vcproj/tests/test_solution/lib2/lib2.vcxproj')
    assert (lib2.output_file('Debug', 'Win32') == '$(OutDir)$(TargetName)$(TargetExt)')


def test_set_output_file():
    test = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    test.set_output_file('All Configurations', 'All Configurations', 'blaaaaa.exe')
    assert (test.output_file('Debug', 'Win32') == 'blaaaaa.exe')

    lib2 = vcproj.project.parse('vcproj/tests/test_solution/lib2/lib2.vcxproj')
    lib2.set_output_file('Debug', 'Win32', 'ughughugh.lib')
    assert (lib2.output_file('Debug', 'Win32') == 'ughughugh.lib')


def test_output_directory():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (p.output_directory('Debug', 'Win32') == '$(SolutionDir)$(Configuration)\\bin')
    assert (p.output_directory('Release', 'Win32') is None)


def test_set_output_directory():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    p.set_output_directory('Debug', 'Win32', 'C:\\foo\\bar')
    assert (p.output_directory('Debug', 'Win32') == 'C:\\foo\\bar')

    p.set_output_directory('Debug', 'Win32', None)
    assert (p.output_directory('Debug', 'Win32') is None)

    p.set_output_directory('All Configurations', 'All Configurations', 'C:\\foo\\bar')
    assert (p.output_directory('Debug', 'Win32') == 'C:\\foo\\bar')
    assert (p.output_directory('Release', 'Win32') == 'C:\\foo\\bar')


def test_program_database_file():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (p.program_database_file('Debug', 'Win32') == '$(TargetDir)test.pdb')
    assert (p.program_database_file('Release', 'Win32') is None)


def test_set_program_database_file():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    p.set_program_database_file('Debug', 'Win32', 'foobar')
    assert (p.program_database_file('Debug', 'Win32') == 'foobar')

    p.set_program_database_file('All Configurations', 'All Configurations', 'blaablaa')
    assert (p.program_database_file('Release', 'Win32') == 'blaablaa')

    p.set_program_database_file('Debug', 'Win32', None)
    assert (p.program_database_file('Debug', 'Win32') is None)


def test_debug_information_format():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (p.debug_information_format('Debug', 'Win32') == 'EditAndContinue')
    assert (p.debug_information_format('Release', 'Win32') is None)


def test_set_debug_information_format():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    p.set_debug_information_format('All Configurations', 'All Configurations', 'ProgramDatabase')
    assert (p.debug_information_format('Debug', 'Win32') == 'ProgramDatabase')
    assert (p.debug_information_format('Release', 'Win32') == 'ProgramDatabase')


def test_enable_incremental_linking():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    assert (p.enable_incremental_linking('Debug', 'Win32') is True)
    assert (p.enable_incremental_linking('Release', 'Win32') is False)


def test_set_enable_incremental_link():
    p = vcproj.project.parse('vcproj/tests/test_solution/test/test.vcxproj')
    p.set_enable_incremental_linking('Debug', 'Win32', False)
    assert (p.enable_incremental_linking('Debug', 'Win32') is False)

    p.set_enable_incremental_linking('Release', 'Win32', None)
    assert (p.enable_incremental_linking('Release', 'Win32') is None)
