#  #
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#  #
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#  #
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#  #
#
#  <pep8 compliant>
import os.path
import shutil

from constants import TEXTURE_FOLDER
from utils import load_json_file, save_json_file, insert_key_value


class MsfsGltf:
    file_path: str
    data: str

    NODES_TAG = "nodes"
    BUFFERS_TAG = "buffers"
    IMAGES_TAG = "images"
    MATERIALS_TAG = "materials"
    MIME_TYPE_TAG = "mimeType"
    URI_TAG = "uri"
    DOUBLESIDED_TAG = "doubleSided"
    ASSET_TAG = "asset"
    SCENE_TAG = "scene"
    TAGS_TAG = "tags"
    GENERATOR_TAG = "generator"
    EXTENSIONS_TAG = "extensions"
    EXTENSIONS_USED_TAG = "extensionsUsed"
    ASOBO_TAGS_TAG = "ASOBO_tags"
    MESHES_TAG = "meshes"
    NAME_TAG = "name"
    ROAD_TAG = "Road"
    COLLISION_TAG = "Collision"
    ENABLED_TAG = "enabled"
    ASOBO_MATERIAL_DAY_NIGHT_SWITCH_TAG = "ASOBO_material_day_night_switch"
    ASOBO_MATERIAL_FAKE_TERRAIN_TAG = "ASOBO_material_fake_terrain"
    ASOBO_MATERIAL_INVISIBLE_TAG = "ASOBO_material_invisible"
    ASOBO_NORMAL_MAP_CONVENTION_TAG = "ASOBO_normal_map_convention"
    ASOBO_ASSETS_OPTIMIZED_TAG = "ASOBO_asset_optimized"
    TANGENT_SPACE_CONVENTION_TAG = "tangent_space_convention"

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = load_json_file(self.file_path)

    def update_image(self, idx, uri, mime_type):
        if not self.data: return

        if not self.data[self.IMAGES_TAG][idx]: return

        image = self.data[self.IMAGES_TAG][idx]
        image[self.URI_TAG] = uri
        image[self.MIME_TYPE_TAG] = mime_type
        self.dump()

    def add_optimization_tag(self):
        if not self.data: return

        self.data[self.ASSET_TAG][self.GENERATOR_TAG] = "Scenery optimized Khronos glTF Blender I/O v1.2.75"

    def add_cleaned_tag(self):
        if not self.data: return

        self.data[self.ASSET_TAG][self.GENERATOR_TAG] = "Scenery optimized and cleaned Khronos glTF Blender I/O v1.2.75"

    def remove_texture_path(self, lod_name):
        if not self.data: return
        if not self.IMAGES_TAG in self.data.keys(): return

        for image in self.data[self.IMAGES_TAG]:
            image[self.URI_TAG] = image[self.URI_TAG].replace(lod_name + "/", str())
            image[self.URI_TAG] = image[self.URI_TAG].replace(TEXTURE_FOLDER + "/", str())

    def rename_texture(self, texture_name, new_texture_name):
        if not self.data: return
        if not self.IMAGES_TAG in self.data.keys(): return

        for image in self.data[self.IMAGES_TAG]:
            texture_name = texture_name.split(".")[0]
            if image[self.NAME_TAG] == texture_name:
                image[self.NAME_TAG] = new_texture_name.split(".")[0]
                image[self.URI_TAG] = new_texture_name
                return

    def add_texture_path(self):
        if not self.data: return
        if not self.IMAGES_TAG in self.data.keys(): return

        for image in self.data[self.IMAGES_TAG]:
            image[self.URI_TAG] = TEXTURE_FOLDER + "/" + image[self.URI_TAG]

    def fix_doublesided(self):
        if not self.data: return
        if not self.MATERIALS_TAG in self.data.keys(): return

        for material in self.data[self.MATERIALS_TAG]:
            material[self.DOUBLESIDED_TAG] = False

    def add_asobo_extensions(self):
        if not self.data: return

        map_convention_data = {
            self.ASOBO_NORMAL_MAP_CONVENTION_TAG: {
                self.TANGENT_SPACE_CONVENTION_TAG: "DirectX"
            }
        }

        self.data[self.ASSET_TAG][self.EXTENSIONS_TAG] = map_convention_data

        extensions_used_data = [
            self.ASOBO_NORMAL_MAP_CONVENTION_TAG,
            self.ASOBO_TAGS_TAG,
            self.ASOBO_MATERIAL_FAKE_TERRAIN_TAG,
            self.ASOBO_MATERIAL_DAY_NIGHT_SWITCH_TAG,
            self.ASOBO_ASSETS_OPTIMIZED_TAG
        ]

        self.data = insert_key_value(self.data, self.EXTENSIONS_USED_TAG, self.SCENE_TAG, extensions_used_data)

        material_extensions_data = {
            self.ASOBO_TAGS_TAG: {
                self.TAGS_TAG: [self.ROAD_TAG, self.COLLISION_TAG]
            },
            self.ASOBO_MATERIAL_DAY_NIGHT_SWITCH_TAG: {
                self.ENABLED_TAG: True
            },
            self.ASOBO_MATERIAL_FAKE_TERRAIN_TAG: {
                self.ENABLED_TAG: True
            }
        }

        if not self.MATERIALS_TAG in self.data.keys(): return

        try:
            for material in self.data[self.MATERIALS_TAG]:
                material[self.EXTENSIONS_TAG] = material_extensions_data
        except:
            pass

    def add_extension_tag(self, extension_tag):
        if not self.data: return

        self.data[self.EXTENSIONS_USED_TAG].append(extension_tag)

        if not self.MATERIALS_TAG in self.data.keys(): return

        try:
            for material in self.data[self.MATERIALS_TAG]:
                material[self.EXTENSIONS_TAG][extension_tag] = {
                    self.ENABLED_TAG: True
                }
        except:
            pass

    def remove_asobo_tag(self, asobo_tag_name):
        if not self.data: return

        if not self.MATERIALS_TAG in self.data.keys(): return

        other_tag_exists = False

        for material in self.data[self.MATERIALS_TAG]:
            if not self.EXTENSIONS_TAG in material.keys(): continue
            if not self.ASOBO_TAGS_TAG in material[self.EXTENSIONS_TAG].keys(): continue
            if not self.TAGS_TAG in material[self.EXTENSIONS_TAG][self.ASOBO_TAGS_TAG].keys(): continue

            if asobo_tag_name in material[self.EXTENSIONS_TAG][self.ASOBO_TAGS_TAG][self.TAGS_TAG]:
                material[self.EXTENSIONS_TAG][self.ASOBO_TAGS_TAG][self.TAGS_TAG].remove(asobo_tag_name)

            if len(material[self.EXTENSIONS_TAG][self.ASOBO_TAGS_TAG][self.TAGS_TAG]):
                other_tag_exists = True
            else:
                material[self.EXTENSIONS_TAG][self.ASOBO_TAGS_TAG].pop(self.TAGS_TAG)
                material[self.EXTENSIONS_TAG].pop(self.ASOBO_TAGS_TAG)

        if self.EXTENSIONS_USED_TAG in self.data.keys():
            if self.ASOBO_TAGS_TAG in self.data[self.EXTENSIONS_USED_TAG] and not other_tag_exists:
                self.data[self.EXTENSIONS_USED_TAG].remove(self.ASOBO_TAGS_TAG)

    def remove_asobo_extension(self, extension_name):
        if not self.data: return

        if not self.MATERIALS_TAG in self.data.keys(): return

        for material in self.data[self.MATERIALS_TAG]:
            if not self.EXTENSIONS_TAG in material.keys(): continue

            if extension_name in material[self.EXTENSIONS_TAG]:
                material[self.EXTENSIONS_TAG].pop(extension_name)

        if self.EXTENSIONS_USED_TAG in self.data.keys():
            if extension_name in self.data[self.EXTENSIONS_USED_TAG]:
                self.data[self.EXTENSIONS_USED_TAG].remove(extension_name)

    def get_subtiles(self):
        result = []

        if not self.data:
            return result

        if self.MESHES_TAG in self.data.keys():
            for mesh in self.data[self.MESHES_TAG]:
                if self.NAME_TAG in mesh.keys():
                    result.append(mesh[self.NAME_TAG].split("_", 1)[0])

        return result

    def is_valid(self):
        return self.BUFFERS_TAG in self.data.keys()

    def dump(self):
        save_json_file(self.file_path, self.data)