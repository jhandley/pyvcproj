#!/usr/bin/python

# List filter structure project in a solution.

import vcproj.solution
import vcproj.project
import vcproj.filters

import os

solution_file = '../vcproj/tests/test_solution/test.sln'
solution = vcproj.solution.parse(solution_file)

# FIXME: add a helpers file
def convert_seperator(token):
    return token.replace("\\", str(os.sep))

# FIXME: add solution.project_filters()
for project_file in solution.project_files():
    filter_file = os.path.join(os.path.dirname(solution_file), convert_seperator(project_file) + ".filters")
    filters = vcproj.filters.parse(filter_file)
    filters.list_tree()

for project_file in solution.project_files():
    filter_file = os.path.join(os.path.dirname(solution_file), convert_seperator(project_file) + ".filters")
    filters = vcproj.filters.parse(filter_file)
    filters.list_tree(attr_list=["realpath", "UniqueIdentifier", "Type"])
