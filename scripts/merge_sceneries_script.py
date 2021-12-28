from utils import Settings, get_sources_path, reload_modules, print_title, isolated_print

settings = Settings(get_sources_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import os

from pathlib import Path
from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject


def merge_sceneries(settings):
    try:
        # instantiate the msfsProject and create the necessary resources if it does not exist
        msfs_project = MsfsProject(settings.projects_path, settings.project_name, settings.author_name, settings.sources_path)
        msfs_project_to_merge = MsfsProject(settings.projects_path, settings.project_name_to_merge, settings.author_name, settings.sources_path)

        check_configuration(settings, msfs_project)
        check_configuration(settings, msfs_project_to_merge)

        if settings.backup_enabled:
            msfs_project.backup(Path(os.path.abspath(__file__)).stem)

        msfs_project.merge(msfs_project_to_merge)

        if settings.build_package_enabled:
            build_package(msfs_project, settings)

        pr_bg_green("Script correctly applied" + CEND)

    except ScriptError as ex:
        error_report = "".join(ex.value)
        isolated_print(constants.EOL + error_report)
        pr_bg_red("Script aborted" + CEND)
    except RuntimeError as ex:
        isolated_print(constants.EOL + str(ex))
        pr_bg_red("Script aborted" + CEND)
    finally:
        os.chdir(os.path.dirname(__file__))


##################################################################
#                        Main process
##################################################################

merge_sceneries(settings)
