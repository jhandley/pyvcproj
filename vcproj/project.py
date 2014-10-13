import xml.etree.ElementTree as ET
import re

__all__ = ['Project', 'parse']

_MS_BUILD_NAMESPACE = "http://schemas.microsoft.com/developer/msbuild/2003"
_REGEX_CONFIG_CONDITION = re.compile(r"""'\$\(Configuration\)\|\$\(Platform\)'=='(\w+)\|(\w+)'""")

def _parse_config_condition(condition):
    return _REGEX_CONFIG_CONDITION.match(condition).groups()

def _matches_platform_configuration(item_group, platform, configuration):
    (p, c) = _parse_config_condition(item_group.attrib['Condition'])
    return (p == "All Configurations" or p == platform) and (c == "All Configurations" or c == configuration)

# ET.register_namespace doesn't exist before python 2.7
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

    def source_files(self):
        """List source files in project."""
        return [c.attrib['Include'] for c in self.xml.findall(".//{" + _MS_BUILD_NAMESPACE + "}ClCompile") if 'Include' in c.attrib]

    def include_files(self):
        """List include files in project."""
        return [c.attrib['Include'] for c in self.xml.findall(".//{" + _MS_BUILD_NAMESPACE + "}ClInclude") if 'Include' in c.attrib]
    
    def __item_groups_for_config(self, platform, configuration):
        groups = self.xml.findall("./{" + _MS_BUILD_NAMESPACE + "}ItemDefinitionGroup")
        return filter(lambda g: _matches_platform_configuration(g, platform, configuration), groups)

    def __item_group_item_for_config(self, platform, configuration, subgroup_name, item_name):
        groups = self.__item_groups_for_config(platform, configuration)
        if len(groups) == 0:
            return []
        item = groups[0].find("{" + _MS_BUILD_NAMESPACE + "}" + subgroup_name + "/{" + _MS_BUILD_NAMESPACE + "}" + item_name)
        if item is None:
            return []
        return item.text.split(';')
        
    def additional_link_dependencies(self, platform, configuration):
        return self.__item_group_item_for_config(platform, configuration, "Link", "AdditionalDependencies")
        
    def additional_include_directories(self, platform, configuration):
        return self.__item_group_item_for_config(platform, configuration, "ClCompile", "AdditionalIncludeDirectories")

    def set_additional_include_directories(self, additional_includes):
        include_nodes = self.xml.findall("./{" + self.__MS_BUILD_NAMESPACE + "}ItemDefinitionGroup/{" +
                                         self.__MS_BUILD_NAMESPACE + "}ClCompile/{" +
                                         self.__MS_BUILD_NAMESPACE + "}AdditionalIncludeDirectories")
        for n in include_nodes:
          n.text = additional_includes

    def write(self, filename = None):
        """Save project file."""
        filename = filename or self.filename
        self.xml.write(filename, xml_declaration=True, encoding='utf-8', method="xml")
        
def parse(filename):
    """Parse project file *filename* and return Project instance."""
    return Project(filename)
