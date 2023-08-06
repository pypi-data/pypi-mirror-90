import subprocess

class IGScrapper():
    """
    Use to scrape data from an instagram account
    """
    def __init__(self, scrapper, password):
        self.scrapper = scrapper
        self.password = password

    def scrape(self, username):
        """
        Scrapes data from an instagram user
        """
        cmd = f"instagram-scraper {username} -u {self.scrapper} -p {self.password} --media-metadata --latest"
        subprocess.run(cmd.split())