import os
from os import walk
import adnar_scraper.settings as settings
import zipfile
import re
from adnar_scraper.utility.data_loader import DataLoader

class ZipUncompresser:
    def __init__(self):
        self.db_name = "/home/discoverious/Downloads/backgrounds/"
        self.zip_files = self.get_zip_files()

    def get_zip_files(self):
        f = []
        for (dirpath, dirnames, filenames) in walk(self.db_name):
            f.extend(filenames)
            break

        return f

    def uncompress(self):
        for zip_file in self.zip_files:
            path = self.db_name + zip_file

            save_path = settings.IMAGE_DATA_DATABASE_PATH + 'background_image/'
            file_name = re.sub(pattern='\.zip', repl='', string=zip_file)

            #DataLoader.create_if_folder_not_exists(path=save_path + file_name)

            zipfile.ZipFile(path).extractall(save_path + file_name)

if __name__ == "__main__":
    uncompresser = ZipUncompresser()

    file_names = uncompresser.get_zip_files()
    uncompresser.uncompress()