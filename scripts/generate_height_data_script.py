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

from utils import GlobalSettings, get_global_path, reload_modules, print_title, isolated_print

settings = GlobalSettings(get_global_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import warnings
from shapely.errors import ShapelyDeprecationWarning

warnings.simplefilter(action="ignore", category=UserWarning, append=True)
warnings.simplefilter(action="ignore", category=FutureWarning, append=True)
warnings.simplefilter(action="ignore", category=DeprecationWarning, append=True)
warnings.simplefilter(action="ignore", category=ShapelyDeprecationWarning, append=True)

import os
from pathlib import Path
from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject


def generate_height_data(global_settings):
    try:
        # instantiate the msfsProject and create the necessary resources if it does not exist
        msfs_project = MsfsProject(global_settings.projects_path, global_settings.project_name, global_settings.definition_file, global_settings.path)

        check_configuration(global_settings, msfs_project)

        if msfs_project.settings.backup_enabled:
            msfs_project.backup(Path(os.path.abspath(__file__)).stem.replace(SCRIPT_PREFIX, str()), all_files=False)

        isolated_print(EOL)
        print_title("GENERATE HEIGHT DATA")

        msfs_project.settings.exclude_ground = True
        msfs_project.settings.exclude_nature_reserve = True
        msfs_project.settings.exclude_parks = True
        msfs_project.settings.keep_constructions = True
        msfs_project.settings.keep_roads = True
        msfs_project.settings.keep_residential_and_industrial = False
        msfs_project.settings.disable_terraform = True
        if not msfs_project.settings.isolate_3d_data:
            msfs_project.settings.building_margin = 8.0
        msfs_project.settings.save()
        msfs_project.prepare_3d_data(global_settings, generate_height_data=True, process_3d_data=False, create_polygons=False, process_all=True)

        if msfs_project.settings.build_package_enabled:
            build_package(global_settings, msfs_project)

        pr_bg_green("Script correctly applied" + constants.CEND)

    except ScriptError as ex:
        error_report = "".join(ex.value)
        isolated_print(constants.EOL + error_report)
        pr_bg_red("Script aborted" + constants.CEND)
    except RuntimeError as ex:
        isolated_print(constants.EOL + str(ex))
        pr_bg_red("Script aborted" + constants.CEND)


##################################################################
#                        Main process
##################################################################


if __name__ == "__main__":
    generate_height_data(settings)
