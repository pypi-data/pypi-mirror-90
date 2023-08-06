import cv2
import os
import numpy as np
from PIL import Image
import time
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime
from . import constants

class Graphics():
    """
    Use to process and generate graphics
    """

    def __init__(self):
        self.output_dir = os.getcwd()+f"/{constants.OUTPUT_FOLDER}/"
        if not os.path.exists(self.output_dir):
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

    def graph_trendline(self, username, ts_list, like_list, ts_peak, like_peak, title, lower_ts, upper_ts):
        """
        Creates a trendline image with the identified 9 peaks
        """
        str_dates = pd.date_range(lower_ts, upper_ts).tolist()
        year_dates = [date.to_pydatetime() for date in str_dates]
        year_y_vals = [-100]*len(year_dates)

        fig = plt.figure(figsize=(8, 6), dpi=300)
        sid = 60*60*24
        xmin, xmax = xlim = time.mktime(lower_ts.timetuple())/sid, time.mktime(upper_ts.timetuple())/sid
        ymin, ymax = ylim = 0, max(like_list)*1.2
        ax = fig.add_subplot(111, xlim=xlim, ylim=ylim,
                            autoscale_on=False)
        X = [[0, 0], [0.1, 0.1]]
        ax.imshow(X, interpolation='bicubic', cmap=cm.gnuplot2,
                extent=(xmin, xmax, ymin-1100, ymax+1200), alpha=1)
        
        ax.plot_date(year_dates, year_y_vals)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax.plot_date(ts_list, like_list, ls='--', color='white')
        ax.plot_date(ts_peak, like_peak, color='red')
        
        ax.set_title(str(title))
        # ax.grid(ls='dotted', color='blue')
        ax.set_aspect('auto')
        fig.savefig(self.output_dir+username.replace(".",""))
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

