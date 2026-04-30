import os
import cv2
import pandas as pd

# TODO: Add documentation notes about what each function does and the whole class too
class edaData():

    def __init__(self):
        self.species = ['Limnius sp', 'Asellus sp']
        # NOTE: likely need to change to a third party class available top level that sets it automatically
        self.dataset_path = f"{os.getcwd()}/insects_dataset"

    # NOTE: Could probably extract this to its own library
    def folder_check(self, species: str) -> tuple[list[str], str] | FileNotFoundError:
        try:
            path = f"{self.dataset_path}/{species}"
            image_list = os.listdir(path)
        except FileNotFoundError:
            # NOTE: Likely need to change to a return to allow the gui to show it
            raise FileNotFoundError(f"The Species, {species},  doesn't exist in the dataset path")
        return image_list, path

    def number_of_image(self, species: str) -> int:
        image_list, _ = self.folder_check(species)
        image_count = len(image_list)
        return image_count

    def statistical_distributions(self, species: str) -> tuple[float, float]:
        image_list, path = self.folder_check(species)
        height_total = 0
        width_total = 0
        image_count = self.number_of_image(species)
        for image in image_list:
            image_path = f"{path}/{image}"
            # (height, width)
            result = cv2.imread(image_path).shape[:2]
            # print(result)
            height_total += result[0]
            width_total += result[1]
        height_mean = round(height_total / image_count, 2)
        width_mean = round(width_total / image_count, 2)

        return height_mean, width_mean

def main():
    eg = edaData()
    for species in eg.species:
        print(f"Species: {species} has {eg.number_of_image(species)} number of images")
        height_mean, width_mean = eg.statistical_distributions(species)
        print(f"Species: {species} has height mean: {height_mean} and width mean: {width_mean}")


if __name__ == "__main__":
    main()
