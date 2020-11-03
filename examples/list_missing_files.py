#!/usr/bin/env python

# List all missing files being referenced in a solution/project

import sys
from pathlib import Path

import vcproj.project
import vcproj.solution


def main(argv):
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <solution file>")
        sys.exit(2)

    solution_path = Path(argv[1])
    solution_dir = solution_path.parent

    solution = vcproj.solution.parse(solution_path)
    for project_file in solution.project_files():
        printed_name = False
        project_path = solution_dir / project_file
        project_dir = project_path.parent

        project = vcproj.project.parse(project_path)

        files = [
            *project.source_files(),
            *project.include_files(),
            *project.generic_files('None'),
            *project.generic_files('Text'),
            *project.generic_files('Image'),
            *project.generic_files('CustomBuild'),
            *project.generic_files('ResourceCompile'),
            *project.generic_files('ProjectReference'),
        ]

        for file in files:
            filepath = project_dir / file
            if not filepath.exists():
                if not printed_name:
                    printed_name = True
                    print(project_file)
                print(f"\t{file}")


if __name__ == '__main__':
    main(sys.argv)
