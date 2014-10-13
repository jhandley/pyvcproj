"""Parse and manipulate Visual Studio project and solution files.

Provides the following modules:

    solution: Visual Studio file (.sln).

    project: Visual Studio project file (.vcxproj).

Use the parse functions provided by the above modules to read in the file.
The following example prints the source files for each project
in the solution::

    import vcproj
    import os

    solution_file = '../vcproj/tests/test_solution/test.sln'
    solution = vcproj.solution.parse(solution_file)
    for project_file in solution.project_files():
        print project_file
        project = vcproj.project.parse(os.path.join(os.path.dirname(solution_file), project_file))
        for source_file in project.source_files():
            print "\t" + source_file

"""


import solution, project

__all__ = ['solution', 'project']

