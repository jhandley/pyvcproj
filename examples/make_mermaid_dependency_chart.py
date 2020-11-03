#!/usr/bin/env python

# Print mermaid syntax to create chart

import sys
from pathlib import Path

import vcproj.solution


def main(argv):
    if len(argv) < 2:
        print(f"Usage: {argv[0]} <solution file>")
        sys.exit(2)

    solution_path = Path(argv[1])

    solution = vcproj.solution.parse(solution_path)
    no_deps = []
    print('graph TD;')
    for p in solution.projects:
        if not p.dependencies:
            no_deps.append(p.name)

        for d in solution.dependencies(p.name):
            print(f'    {d}-->{p.name};')


if __name__ == '__main__':
    main(sys.argv)
