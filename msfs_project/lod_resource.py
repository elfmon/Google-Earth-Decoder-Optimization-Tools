import os

from utils import backup_file


class MsfsLodResource:
    folder: str
    file: str

    def __init__(self, folder, file):
        self.folder = folder
        self.file = file

    def backup_file(self, backup_path, dry_mode=False, pbar=None):
        backup_file(backup_path, self.folder, self.file, dry_mode=dry_mode, pbar=pbar)

    def remove_file(self):
        file_path = os.path.join(self.folder, self.file)
        if os.path.isfile(file_path):
            os.remove(os.path.join(file_path))
            print(self.file, "removed")