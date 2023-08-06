import cv2
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from . import constants

class Graphics():
    """
    Use to process and generate graphics
    """

    def __init__(self):
        self.output_dir = os.getcwd()+f"/{constants.OUTPUT_FOLDER}/"
        os.mkdir(self.output_dir)

    def crop_center(self, pil_img, crop_width, crop_height):
        """
        Crops image with inputs relative to center
        """
        img_width, img_height = pil_img.size
        return pil_img.crop(((img_width - crop_width) // 2,
                            (img_height - crop_height) // 2,
                            (img_width + crop_width) // 2,
                            (img_height + crop_height) // 2))

    def crop_max_square(self, image_filename):
        """
        Crops max square from image 
        """
        pil_img = Image.open(image_filename)
        cropped_image = self.crop_center(pil_img, min(pil_img.size), min(pil_img.size))
        cropped_image.save(image_filename, quality=95)

    def graph_trendline(self, username, ts_list, like_list, ts_peak, like_peak):
        """
        Creates a trendline image with the identified 9 peaks
        """
        plt.plot(ts_list, like_list)
        plt.scatter(ts_peak, like_peak, color='red')
        plt.savefig(self.output_dir+username.replace(".",""))
        plt.close()

    def generate_image_matrix(self, username, filename_peak):
        """
        Generates image matrix based on list of image filenames
        """
        image_list = []
        for jpg in filename_peak:
            self.crop_max_square(jpg)
            image = cv2.imread(jpg)
            image_list.append(cv2.resize(image,(800,800)))

        hor1 = (np.hstack([image_list[0],image_list[1],image_list[2]]))
        hor2 = (np.hstack([image_list[3],image_list[4],image_list[5]]))
        hor3 = (np.hstack([image_list[6],image_list[7],image_list[8]]))

        image_matrix=np.vstack([hor1,hor2,hor3])

        cv2.imwrite(self.output_dir+username.replace(".","")+".jpg", image_matrix)

