import os
import xml.etree.ElementTree as Et
from constants import *
from utils import pretty_print, line_prepender


class Xml:
    file_path: str
    file_name: str
    tree: object
    root: object

    def __init__(self, file_folder, file_name):
        self.file_path = os.path.join(file_folder, file_name)
        self.file_name = file_name
        self.tree = Et.parse(self.file_path)
        self.root = self.tree.getroot()

    def save(self):
        self.tree.write(self.file_path, encoding=ENCODING)
        pretty_print(element=self.root)
        line_prepender(self.file_path, XML_HEADER)