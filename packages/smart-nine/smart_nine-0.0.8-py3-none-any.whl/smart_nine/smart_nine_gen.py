import os
import json
import time
from datetime import datetime
from pytz import timezone
import pytz
from . import scrapper, graphics
from . import metrics_analytics as ma

class SmartNineGen():
    """
    Use to generate a good instagram top nine
    """
    def __init__(self, usernames, scrapper_user, password, tz, year):
        self.usernames = self.handle_usernames(usernames)
        self.tz = timezone(tz)
        self.scrapper = scrapper.IGScrapper(scrapper_user, password)
        self.metrics = ma.MetricsAnalytics()
        self.year = year

        if self.year == "All":
            self.upper_ts = datetime.now(self.tz)
            self.lower_ts = datetime.strptime(f"2000-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
        else:
            self.upper_ts = datetime.strptime(f"{year+1}-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
            self.lower_ts = datetime.strptime(f"{year}-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S")
            self.upper_ts = self.tz.localize(self.upper_ts)
            self.lower_ts = self.tz.localize(self.lower_ts)
        self.graphics = graphics.Graphics()

    def handle_usernames(self, usernames):
        """
        Forces usernames to be of type list
        """
        if isinstance(usernames, list):
            return usernames
        else:
            usernames = [usernames]
            return usernames

    def extract_jpg(self, url):
        """
        Returns jpg filename from URL
        """
        jpg = url.split("?")[0].split("/")[-1]
        return jpg

    def smart_nine_gen(self, scrape_flag = True):
        """
        Generates a smart instagram top nine image
        """
        for username in self.usernames:
            if scrape_flag:
                self.scrapper.scrape(username)
            print(f"Processing Instagram account: @{username}")
            ts_list, like_list, filename_list = self.filter_content(username, self.year)
            ts_peak, like_peak, filename_peak = self.metrics.find_top_nine_peaks(ts_list, 
                                                                                 like_list,
                                                                                 filename_list,
                                                                                 username,
                                                                                 self.year)
            
            self.graphics.graph_trendline(username+f"_{self.year}",
                                          ts_list,
                                          like_list,
                                          ts_peak,
                                          like_peak,
                                          self.year,
                                          self.lower_ts,
                                          self.upper_ts)
            self.graphics.generate_image_matrix(username+f"_{self.year}", filename_peak)

    def filter_content(self, username, year):
        """
        Filters content by year
        """
        user_data_path = str(os.getcwd()) +f"/{username}/"
        meta_data_path = str(os.getcwd()) +f"/{username}/{username}.json"

        if os.path.isfile(meta_data_path):
            config_dict = json.load(open(meta_data_path, encoding="utf-8"))
        else:
            raise ValueError(f"Unable to find metadata for Intagram user: @{username}. Enable scrapping.")

        ts_list = []
        like_list = []
        filename_list = []
        upper_ts = time.mktime(self.upper_ts.timetuple())
        lower_ts = time.mktime(self.lower_ts.timetuple())

        print(f"Began filtering for year: {year}...")
        for post in config_dict["GraphImages"]:
            ts = datetime.fromtimestamp(post['taken_at_timestamp'], self.tz) #.isoformat()

            if post['taken_at_timestamp'] > upper_ts:
                continue

            if post['taken_at_timestamp'] < lower_ts:
                print(f"Finished filtering.")
                break

            filename = user_data_path+self.extract_jpg(post["urls"][0])
            if ".mp4" in filename:
                continue

            likes = post['edge_media_preview_like']['count']
            ts_list.append(ts)
            like_list.append(likes)
            filename_list.append(filename)

        if self.year == "All":
            self.lower_ts = ts
    
        return ts_list, like_list, filename_list
        
