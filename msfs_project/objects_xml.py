from utils import Xml


class ObjectsXml(Xml):
    GUID_TAG = "name"
    LIBRARY_OBJECTS_SEARCH_PATTERN = "./SceneryObject/LibraryObject"
    SCENERY_OBJECT_SEARCH_PATTERN = "./SceneryObject/LibraryObject[@name='"
    SCENERY_OBJECT_GROUP_SEARCH_PATTERN = "./Group/SceneryObject/LibraryObject[@name='"

    def __init__(self, file_folder, file_name):
        super().__init__(file_folder, file_name)

    def update_objects_position(self, msfs_project, settings):
        self.__update_tiles_pos(msfs_project, settings)
        self.__update_colliders_pos(msfs_project, settings)
        self.save()

    def __retrieve_library_objects(self):
        return self.root.findall(self.LIBRARY_OBJECTS_SEARCH_PATTERN)

    def __find_scenery_objects(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def __find_scenery_objects_in_group(self, guid):
        return self.root.findall(self.SCENERY_OBJECT_GROUP_SEARCH_PATTERN + guid.upper() + self.PARENT_PATTERN_SUFFIX)

    def __update_tiles_pos(self, msfs_project, settings):
        for guid, tile in msfs_project.tiles.items():
            print("-------------------------------------------------------------------------------")
            print("xml tile: ", tile.name)

            self.__update_scenery_object_pos(tile, self.__find_scenery_objects(guid.upper()), settings)
            self.__update_scenery_object_pos(tile, self.__find_scenery_objects_in_group(guid.upper()), settings)

    def __update_colliders_pos(self, msfs_project, settings):
        for guid, collider in msfs_project.colliders.items():
            print("-------------------------------------------------------------------------------")
            print("xml collider: ", collider.name)

            self.__update_scenery_object_pos(collider, self.__find_scenery_objects(guid.upper()), settings)
            self.__update_scenery_object_pos(collider, self.__find_scenery_objects_in_group(guid.upper()), settings)

    @staticmethod
    def __update_scenery_object_pos(tile, found_scenery_objects, settings):
        for scenery_object in found_scenery_objects:
            new_lat = tile.pos.lat + settings.lat_correction
            new_lon = tile.pos.lon + settings.lon_correction
            print("new lat: ", new_lat)
            print("new lon: ", new_lon)
            scenery_object.set("lat", str(new_lat))
            scenery_object.set("lon", str(new_lon))
