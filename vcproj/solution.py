"""Visual Studio Solution File."""

__all__ = ['Solution', 'parse']

import codecs
import re
from collections import namedtuple

_Project = namedtuple('_Project', 'type_guid,name,path,guid,dependencies')
_GUID = r'\{[\w-]+\}'
_REGEX_PROJECT_FILE = re.compile(rf'''
    Project\("({_GUID})"\)  # type_guid
    [\s=]+
    "([^"]+)",\s            # name
    "(.+proj)",\s+          # path
    "({_GUID})"             # guid
''', re.X)
_REGEX_END_PROJECT = re.compile(r'\s*EndProject')
_REGEX_PROJECT_DEPENDENCIES_SECTION = re.compile(r'\s*ProjectSection\((\w+)\) = postProject')
_REGEX_END_PROJECT_SECTION = re.compile(r'\s*EndProjectSection')
_REGEX_DEPENDENCY = re.compile(rf'\s*({_GUID})\s*=\s*({_GUID})')


def parse(filename):
    """Parse solution file filename and return Solution instance."""
    return Solution(filename)


class SolutionFileError(Exception):
    pass


class Solution(object):
    """Visual C++ solution file (.sln)."""

    def __init__(self, filename):
        """Create a Solution instance for solution file *name*."""
        self.filename = filename
        self.projects = []
        with open(self.filename, encoding='utf-8-sig') as f:
            line = f.readline()
            while line:
                line = f.readline()
                if line.startswith('Project'):
                    match = _REGEX_PROJECT_FILE.match(line)
                    if match:
                        self.projects.append(Solution.__read_project(match.groups(), f))
                    else:
                        print(f'No MATCH: {line}')
                elif line.startswith('Global'):
                    self.globals = Solution.__read_global(f)

    @staticmethod
    def __read_project(project, f):
        dependencies = []
        while True:
            line = f.readline()
            if line is None:
                raise SolutionFileError("Missing end project")
            if _REGEX_END_PROJECT.match(line):
                break
            if _REGEX_PROJECT_DEPENDENCIES_SECTION.match(line):
                dependencies = Solution.__read_dependencies(f)
        return _Project(*project, dependencies)

    @staticmethod
    def __read_dependencies(f):
        dependencies = []
        while True:
            line = f.readline()
            if line is None:
                raise SolutionFileError("Missing end dependencies section")
            if _REGEX_END_PROJECT_SECTION.match(line):
                break
            match = _REGEX_DEPENDENCY.match(line)
            if match:
                dependencies.append(match.group(1))
        return dependencies

    @staticmethod
    def __read_global(f):
        globals = []
        while True:
            line = f.readline()
            if line is None:
                raise SolutionFileError("Missing end global")
            if line.startswith('EndGlobal'):
                break
            globals.append(line.rstrip())
        return globals

    def project_files(self):
        """List project files (.vcxproj.) in solution."""
        return map(lambda p: p.path, self.projects)

    def project_names(self):
        """List project files (.vcxproj.) in solution."""
        return map(lambda p: p.name, self.projects)

    def dependencies(self, project_name):
        """List names of projects dependent on project *project_name*"""
        project = self.__project_from_name(project_name)
        if not project:
            raise SolutionFileError(f"Can't find project with name {project_name}")
        return map(lambda d: self.__project_from_id(d)[1], project.dependencies)

    def set_dependencies(self, project_name, dependencies):
        """Set names of projects dependent on project *project_name* to *dependencies*"""
        project = self.__project_from_name(project_name)
        if not project:
            raise SolutionFileError(f"Can't find project with name {project_name}")
        index = self.projects.index(project)
        self.projects[index] = _Project(*project[0:4], map(lambda d: self.__project_from_name(d)[3], dependencies))

    def __project_from_name(self, project_name):
        return next((p for p in self.projects if p.name == project_name), None)

    def __project_from_id(self, project_id):
        return next(filter(lambda p: p.guid == project_id, self.projects))

    def write(self, filename=None):
        """Save solution file."""
        filename = filename or self.filename
        with codecs.open(filename, 'wb', 'utf-8-sig') as f:
            f.write('\r\nMicrosoft Visual Studio Solution File, Format Version 11.00\r\n')
            f.write('# Visual Studio 2010\r\n')
            for p in self.projects:
                f.write(f'Project("{p[0]}") = "{p[1]}", "{p[2]}", "{p[3]}"\r\n')
                dependencies = p[4]
                if dependencies:
                    f.write('\tProjectSection(ProjectDependencies) = postProject\r\n')
                    for d in dependencies:
                        f.write(f'\t\t{d} = {d}\r\n')
                    f.write('\tEndProjectSection\r\n')
                f.write('EndProject\r\n')
            f.write('Global\r\n')
            for g in self.globals:
                f.write(f'{g}\r\n')
            f.write('EndGlobal\r\n')
