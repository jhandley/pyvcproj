#!/usr/bin/python

# List all source and include files for each project in a solution.

import vcproj
import os

solution_file = '../vcproj/tests/test_solution/test.sln'
solution = vcproj.solution.parse(solution_file)
for project_file in solution.project_files():
    print project_file
    project = vcproj.project.parse(os.path.join(os.path.dirname(solution_file), project_file))
    for source_file in project.source_files():
        print "\t" + source_file
    for include_file in project.include_files():
        print "\t" + include_file
