import xml.etree.ElementTree as ET

class Project(object):
    """Visual C++ project file (.vcxproj)."""

    __MS_BUILD_NAMESPACE = "http://schemas.microsoft.com/developer/msbuild/2003"

    def __init__(self, filename):
        """Create a Project instance for project file *filename*."""
        ET.register_namespace('', self.__MS_BUILD_NAMESPACE)
        self.filename = filename
        self.xml = ET.parse(filename)

    def source_files(self):
        """List source files in project."""
        return [c.attrib['Include'] for c in self.xml.findall(".//{" + self.__MS_BUILD_NAMESPACE + "}ClCompile[@Include]")]

    def include_files(self):
        """List include files in project."""
        return [c.attrib['Include'] for c in self.xml.findall(".//{" + self.__MS_BUILD_NAMESPACE + "}ClInclude[@Include]")]

    def set_additional_include_directories(self, additional_includes):
        include_nodes = self.xml.findall("./{" + self.__MS_BUILD_NAMESPACE + "}ItemDefinitionGroup/{" + self.__MS_BUILD_NAMESPACE + "}ClCompile/{" + __MS_BUILD_NAMESPACE + "}AdditionalIncludeDirectories")
        for n in include_nodes:
          n.text = additional_includes

    def write(self, filename = None):
        """Save project file."""
        filename = filename or self.filename
        self.xml.write(filename, xml_declaration=True, encoding='utf-8', method="xml")
        
def parse(filename):
    """Parse project file *filename* and return Project instance."""
    return Project(filename)
