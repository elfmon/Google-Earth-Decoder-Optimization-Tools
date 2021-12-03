# constants
CEND = "\033[0m"
BOLD = "\033[01m"
CRED = "\033[31m"
CGREEN = "\033[32m"
CORANGE = "\033[38;5;214m"
CREDBG = "\033[41m"
CGREENBG = "\033[6;30;42m"
OK = "OK"
KO = "KO"
EOL = "\n"
NODE_JS_SCRIPT="retrievepos.js"
MSFS_BUILD_EXE="fspackagetool.exe"
EARTH_RADIUS = 6371010

POS_FILE_EXT = ".pos"
XML_FILE_EXT = ".xml"
GLTF_FILE_EXT = ".gltf"
BIN_FILE_EXT = ".bin"
DBF_FILE_EXT = ".dbf"
SHP_FILE_EXT = ".shp"
SHX_FILE_EXT = ".shx"

POS_FILE_PATTERN = "*" + POS_FILE_EXT
XML_FILE_PATTERN = "*" + XML_FILE_EXT
GLTF_FILE_PATTERN = "*" + GLTF_FILE_EXT
BIN_FILE_PATTERN = "*" + BIN_FILE_EXT
DBF_FILE_PATTERN = "*" + DBF_FILE_EXT
SHP_FILE_PATTERN = "*" + SHP_FILE_EXT
SHX_FILE_PATTERN = "*" + SHX_FILE_EXT

ENCODING = "utf-8"

XML_HEADER = '<?xml version="1.0"?>'

CLEAR_CONSOLE_CMD = "cls"

PYTHON_COMPIL_OPTION = "exec"

RESOURCE_FOLDER = "resource"
TEMPLATES_FOLDER = RESOURCE_FOLDER + "\\" + "templates"
THUMBNAIL_FOLDER = RESOURCE_FOLDER + "\\" + "thumbnail"

BUSINESS_JSON_TEMPLATE = "Business.json"
PACKAGE_DEFINITIONS_TEMPLATE = "package-definition.xml"
PROJECT_DEFINITION_TEMPLATE = "project-definition.xml"
THUMBNAIL_PICTURE_TEMPLATE = "Thumbnail.jpg"

PROJECT_DEFINITION_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + PROJECT_DEFINITION_TEMPLATE
BUSINESS_JSON_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + BUSINESS_JSON_TEMPLATE
PACKAGE_DEFINITIONS_TEMPLATE_PATH = TEMPLATES_FOLDER + "\\" + PACKAGE_DEFINITIONS_TEMPLATE
THUMBNAIL_PICTURE_TEMPLATE_PATH = THUMBNAIL_FOLDER + "\\" + THUMBNAIL_PICTURE_TEMPLATE

