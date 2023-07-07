"""Visual C++ project filters file."""

import xml.etree.ElementTree as ET
import re, string
import os
from bigtree import list_to_tree, print_tree, dict_to_tree

__all__ = ['Project', 'parse']

_MS_BUILD_NAMESPACE = "http://schemas.microsoft.com/developer/msbuild/2003"

try:
    _register_namespace = ET.register_namespace
except AttributeError:
    def _register_namespace(prefix, uri):
        ET._namespace_map[uri] = prefix

class Project(object):
    """Visual C++ project file (.vcxproj)."""

    def __init__(self, filename):
        """Create a Project instance for project file *filename*."""
        _register_namespace('', _MS_BUILD_NAMESPACE)
        self.filename = filename
        self.xml = ET.parse(filename)
        # FIXME: consider using the project file and get RootNamespace instead
        self.root_namespace = os.path.basename(self.filename).split(".")[0]

    def convert_seperator(self, token):
        """Convert seperator from Windows to OS"""
        return token.replace("\\", str(os.sep))

    def get_type(self, tag):
        """Get Type, basically remove the _MS_BUILD_NAMESPACE."""
        return str(tag).replace("{" + _MS_BUILD_NAMESPACE + "}", "")

    def get_tree(self):
        """Get project filter tree."""
        path_dict = {}
        myroot = self.xml.getroot()
        for y in myroot[0:]:
            for x in y:
                    type = self.get_type(x.tag)
                    if not "Filter" == type:
                        folder=""
                        filename=""
                        realpath=""
                        if len(x) == 1:
                            folder = self.convert_seperator(x[0].text)
                            if folder:
                                realpath = self.convert_seperator(x.attrib['Include'])
                                filename = "/" + os.path.basename(realpath)
                        else:
                            realpath = self.convert_seperator(x.attrib['Include'])
                            filename = x.attrib['Include']
                        filter_path = self.root_namespace + "/" + str(folder) + str(filename)
                        path_dict[filter_path] = {"realpath": realpath, "Type": type}
                    else:
                        filter_path = self.root_namespace + "/" + self.convert_seperator(x.attrib['Include'])
                        path_dict[filter_path] = {"realpath": "", "UniqueIdentifier": x[0].text, "Type": type}

        return dict_to_tree(path_dict)

    def list_tree(self, attr_list=[]):
        """List project filter tree."""
        print_tree(self.get_tree(), attr_list=attr_list)

def parse(filename):
    """Parse project file filename and return Project instance."""
    return Project(filename)
