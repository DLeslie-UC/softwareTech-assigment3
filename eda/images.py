import os
from math import sqrt
import cv2
import pandas as pd

class edaData():

    def __init__(self, species: list[str]):
        self.species = species
        # NOTE: likely need to change to a third party class available top level that sets it automatically
        self.__dataset_path = f"{os.getcwd()}/insects_dataset"

    # NOTE: Could probably extract this to its own library
    def __folder_check(self, species: str) -> tuple[list[str], str] | FileNotFoundError:
        try:
            path = f"{self.__dataset_path}/{species}"
            image_list = os.listdir(path)
        except FileNotFoundError:
            # NOTE: Likely need to change to a return to allow the gui to show it
            raise FileNotFoundError(f"The Species, {species},  doesn't exist in the dataset path")
        return image_list, path

    def number_of_image(self, species: str, image_list: list[str] = []) -> int:
        ''' Gets the number of images for the species or the image_list passed to it '''
        # Done this way to prevent recalculating it when doing stuff in mean_height_width func
        if image_list == []:
            image_list, _ = self.__folder_check(species)
        image_count = len(image_list)
        return image_count

    def mean_height_width(self, species: str) -> tuple[float, float]:
        ''' Calculates the mean width and height for the species passed '''
        image_list, path = self.__folder_check(species)
        height_total = 0
        width_total = 0
        image_count = self.number_of_image(species, image_list)
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

    def standard_deviation(self, species: str) -> tuple[float, float]:
        ''' Calculates the standard deviation of the width and height for the species passed '''
        image_list, path = self.__folder_check(species)
        height_mean, width_mean = self.mean_height_width(species)
        image_count = self.number_of_image(species, image_list)
        height_sum_squared_diff = 0
        width_sum_squared_diff = 0

        for image in image_list:
            image_path = f"{path}/{image}"
            # (height, width)
            result = cv2.imread(image_path).shape[:2]
            height_sum_squared_diff += (result[0] - height_mean)**2
            width_sum_squared_diff += (result[1] - width_mean)**2

        height_std = round(sqrt(height_sum_squared_diff/image_count), 2)
        width_std = round(sqrt(width_sum_squared_diff/image_count), 2)

        return height_std, width_std

    def representative_images(self, species: str) -> list[str]: 
        ''' Gets a representative set of images for the species by checking if the images for it are within +-1 standard deviation for the species images set '''
        image_list, path = self.__folder_check(species)
        height_mean, width_mean = self.mean_height_width(species)
        height_std, width_std = self.standard_deviation(species)
        height_lower_bound = height_mean - height_std
        height_upper_bound = height_mean + height_std
        width_lower_bound = width_mean - width_std
        width_upper_bound = width_mean + width_std
        representative_list = []
        for image in image_list:
            image_path = f"{path}/{image}"
            result = cv2.imread(image_path).shape[:2]
            height = result[0]
            width = result[1]
            height_check = height_lower_bound <= height <= height_upper_bound
            width_check = width_lower_bound <= width <= width_upper_bound
            if (height_check) and (width_check):
                representative_list.append(image)
            # NOTE: Can change len req if need more images
            # Done to check if have enough images already
            if len(representative_list) > 9:
                break
        return representative_list

def main():
    eg = edaData(['Limnius sp', 'Asellus sp'])
    # eg = edaData(['Limnius sp'])
    for species in eg.species:
        # print(f"Species: {species} has {eg.number_of_image(species)} number of images")
        # height_mean, width_mean = eg.mean_height_width(species)
        # print(f"Species: {species} has height mean: {height_mean} and width mean: {width_mean}")
        # height_std, width_std = eg.standard_deviation(species)
        # print(f"Species: {species} has height std: {height_std} and width std: {width_std}")
        # height_iqr, width_iqr = eg.iqr(species)
        # print(f"Species: {species} has height iqr: {height_iqr} and width iqr: {width_iqr}")
        representative_list = eg.representative_images(species)
        print(f"Species: {species} has representative images: {representative_list}")


if __name__ == "__main__":
    main()
