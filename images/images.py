import os
import sys
from time import strftime, gmtime
from PIL import Image, ImageEnhance

parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)
from file.files import FileHandling
sys.path.remove(parent_dir)

class ImageManipulation(FileHandling):
    def __init__(self, image, save_path):
        self.__image = image
        self.__file = ""
        self.__path = save_path
        super().__init__(self.__path)
        self.__save_location = self.save_location()
        self.__image_file = Image.open(self.__image)

    def __check_if_other_operations_done(self, text):
        if self.__file == "":
            self.__file += text
        else:
            self.__file += f"&{text}"

    def black_and_white(self):
        self.__image_file = self.__image_file.convert('1')
        self.__check_if_other_operations_done("b&w")

    def upside_down(self):
        self.__image_file = self.__image_file.transpose(Image.FLIP_TOP_BOTTOM)
        self.__check_if_other_operations_done("upside_down")

    def sixteen_bit(self):
        self.__image_file = self.__image_file.quantize(16)
        self.__check_if_other_operations_done("16_bit")

    def contrast(self):
        self.__image_file = ImageEnhance.Contrast(self.__image_file).enhance(2.0)
        self.__check_if_other_operations_done("contrast")

    def brightness(self):
        self.__image_file = ImageEnhance.Brightness(self.__image_file).enhance(2.0)
        self.__check_if_other_operations_done("brightness")

    def save_image(self):
        if self.__file == "":
            self.__file = "test.png"
        else:
            self.__file += ".png"
        self.__image_file.save(os.path.join(self.__save_location, self.__file))
    
    def return_image(self):
        return self.__image_file


def main():
    image = ImageManipulation(os.path.join(os.getcwd(), "insects_dataset", "Elmis sp", "CPH-Elmis sp.-503-t.png"))
    image.black_and_white()
    image.save_image()

if __name__ == "__main__":
    main()

