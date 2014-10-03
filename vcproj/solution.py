import re

class Solution(object):
    """Visual C++ solution file (.sln)."""

    __REGEX_PROJECT_FILE = re.compile(r"""Project\("\{[A-Za-z0-9-]+\}"\) = "\w+", "(((\w+)\\)*(\w+)\.vcxproj)", \"{[A-Za-z0-9-]+}\"""")

    def __init__(self, filename):
        """Create a Solution instance for solution file *name*."""
        self.filename = filename
        with open(self.filename) as f:
            self.lines = f.readlines()        

    def projects(self):
        """List project files (.vcxproj.) in solution."""
        for line in self.lines:
            match = self.__REGEX_PROJECT_FILE.match(line)
            if match:
                yield match.group(1)

def parse(filename):
    """Parse solution file *filename* and return Solution instance."""
    return Solution(filename)
