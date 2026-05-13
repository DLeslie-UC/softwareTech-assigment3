import os
from time import strftime, gmtime
class FileHandling():
    def __init__(self, path):
        self.__save_folder = os.path.join(os.getcwd(), "results", strftime("%Y-%m-%d", gmtime()), path)

    def __check_exists(self):
        if not os.path.exists(self.__save_folder):
            os.makedirs(self.__save_folder)
    def save_location(self):
        self.__check_exists()
        return self.__save_folder
