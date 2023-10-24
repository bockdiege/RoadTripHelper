"""
This class manages all individual scrappers, so that these do not need to be called one by one.
Class also reads different keys from a selected path, and parses said keys into the respective scrappers
"""
from TripHelper.Scrapers.NationalParksScrapper import NationalParkScrapper
from TripHelper.Scrapers.OSRMScrapper import OSRMScrapper


class Scrapper:

    def __init__(self, keys_path: 'str'):
        self.keys_path = keys_path

        # read the keys and initialize the individual scrappers

        with open(self.keys_path) as file:
            for key_info in file.read().split('\n'):
                name = key_info.split(",")[0]
                key = key_info.split(",")[1]

                if name == "USGOV":
                    # Initialise every scrapper that uses USGOV api
                    self.nps = NationalParkScrapper(key)
                    continue
                if name == "OSRM":
                    self.osrm = OSRMScrapper()   # This scrapper does not need a key
                    continue

    def print_nps_scrapper(self):
        print(self.nps)

