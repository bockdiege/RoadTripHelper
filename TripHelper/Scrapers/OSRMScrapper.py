"""
This Scrapper gets data from the OSRM api
"""
import urllib.request, json

from TripHelper.Scrapers.ScrapperState import ScrapperState


class OSRMScrapper:

    def __init__(self):
        self.state = ScrapperState.LIBERAL
        print("OSRM Scrapper initialised")
        return

    def execute_call(self, url):
        req = urllib.request.Request(url)
        response_raw = urllib.request.urlopen(req)
        response = response_raw.read()
        data = json.loads(response.decode('utf-8'))
        return data

    def get_waypoint_by_hint(self, hint: 'str'):
        """
        E.g. you can use the hint value obtained by the nearest query as hint values for route inputs.
        """
        url = "http://router.project-osrm.org/nearest/v1/driving/13.388860,52.517037?number=3"
        return