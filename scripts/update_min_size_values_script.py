from utils import Settings, get_sources_path, reload_modules, print_title, isolated_print

settings = Settings(get_sources_path())

# reload modules if the option is enabled in the optimization_tools.ini file
reload_modules(settings)

import os

from pathlib import Path
from constants import *
from utils import check_configuration, ScriptError, build_package, pr_bg_green, pr_bg_red
from msfs_project import MsfsProject


def update_min_size_values(script_settings):
    try:
        # instantiate the msfsProject and create the necessary resources if it does not exist
        msfs_project = MsfsProject(script_settings.projects_path, script_settings.project_name, script_settings.author_name, script_settings.sources_path)

        check_configuration(script_settings, msfs_project)

        if script_settings.backup_enabled:
            msfs_project.backup(Path(os.path.abspath(__file__)).stem.replace(SCRIPT_PREFIX, str()))

        isolated_print(EOL)
        print_title("UPDATE MIN SIZE VALUES")

        msfs_project.update_min_size_values(script_settings)

        if script_settings.build_package_enabled:
            build_package(msfs_project, script_settings)

        pr_bg_green("Script correctly applied" + constants.CEND)

    except ScriptError as ex:
        error_report = "".join(ex.value)
        isolated_print(constants.EOL + error_report)
        pr_bg_red("Script aborted" + constants.CEND)
    except RuntimeError as ex:
        isolated_print(constants.EOL + ex)
        pr_bg_red("Script aborted" + constants.CEND)


##################################################################
#                        Main process
##################################################################

if __name__ == "__main__":
    update_min_size_values(settings)
