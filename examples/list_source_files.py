#!/usr/bin/env python

# List all source and include files for each project in a solution.

import sys
from pathlib import Path

import vcproj.project
import vcproj.solution


def main(argv):
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <solution file>")
        sys.exit(2)
    solution_path = argv[1]

    solution_path = Path(solution_path)
    solution_dir = solution_path.parent

    solution = vcproj.solution.parse(solution_path)
    for project_file in solution.project_files():
        print(project_file)
        project = vcproj.project.parse(solution_dir / project_file)
        for source_file in project.source_files():
            print(f"\t{source_file}")
        for include_file in project.include_files():
            print(f"\t{include_file}")


if __name__ == '__main__':
    # main(sys.argv)
    main(['', '../vcproj/tests/test_solution/test.sln'])
