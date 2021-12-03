from msfs_project.object import MsfsObject


class MsfsShape(MsfsObject):
    dbf_file_name: str
    shp_file_name: str
    shx_file_name: str

    def __init__(self, path, name, definition_file, dbf_file_name, shp_file_name, shx_file_name):
        super().__init__(path, name, definition_file)
        self.dbf_file_name = dbf_file_name
        self.shp_file_name = shp_file_name
        self.shx_file_name = shx_file_name
