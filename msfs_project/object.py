from msfs_project.object_xml import MsfsObjectXml


class MsfsObject:
    name: str
    definition_file: str
    xml: MsfsObjectXml

    def __init__(self, path, name, definition_file):
        self.name = name
        self.definition_file = definition_file
        self.xml = MsfsObjectXml(path, definition_file)
