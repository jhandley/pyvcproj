#!/usr/bin/env python

# Fixes the following warning:
#   warning MSB8012: TargetPath does not match the Linker's OutputFile
#   property value. This may cause your project to build incorrectly. To
#   correct this, please make sure that $(OutDir), $(TargetName) and
#   $(TargetExt) property values match the value specified in
#   %(Link.OutputFile).
# Pass in path to solution file, a desired output directory for exe
# and dll files and a desired library for lib files. Desired output
# directory for both is usually "$(SolutionDir)$(Configuration)" but you can
# use any paths. The script will modify the $OutDir variable for each project
# to point to the exe/dll output directory for exe/dll projects and to the
# lib directory for static library projects.
# It will then make the OutputFile property use the $OutDir variable to
# appease the warning.

import os
import sys

import vcproj.project
import vcproj.solution


def main(argv):
    if len(argv) < 4:
        print("Usage: " + argv[0] + " <solution file> <bin directory> <lib directory>")
        sys.exit(2)
    solution_path = argv[1]
    solution_dir = os.path.dirname(solution_path)
    bin_dir = argv[2]
    lib_dir = argv[3]
    solution = vcproj.solution.parse(solution_path)
    for project_file in solution.project_files():
        project = vcproj.project.parse(os.path.join(solution_dir, project_file))
        if project.configuration_type() == 'StaticLibrary':
            project.set_output_directory('All Configurations', 'All Configurations', lib_dir)
        else:
            project.set_output_directory('All Configurations', 'All Configurations', bin_dir)
            # use default value for pdb file, should end up in OutDir
            project.set_program_database_file('All Configurations', 'All Configurations', None)

        # set output file to got to OutDir
        project.set_output_file('All Configurations', 'All Configurations', '$(OutDir)$(TargetName)$(TargetExt)')
        project.write()


if __name__ == '__main__':
    main(sys.argv)
