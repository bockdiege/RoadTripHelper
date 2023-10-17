"""
This Scrapper gets data from the OSRM api
"""
import urllib.request, json
import polyline

from TripHelper.Scrapers.ScrapperState import ScrapperState


class OSRMScrapper:

    def __init__(self):
        self.state = ScrapperState.LIBERAL
        print("OSRM Scrapper initialised")
        return

    def get_direction_between_two_points(self, latlong1, latlong2):
        url = f"http://router.project-osrm.org/route/v1/driving/{latlong1[1]},{latlong1[0]};{latlong2[1]},{latlong2[0]}"
        #url = "http://router.project-osrm.org/route/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219"
        data_raw = self.execute_call(url)
        data = data_raw["routes"][0]
        geometry_encoded = data["geometry"]
        geometry_decoded = polyline.decode(geometry_encoded)
        return geometry_decoded

    def execute_call(self, url):
        req = urllib.request.Request(url)
        response_raw = urllib.request.urlopen(req)
        response = response_raw.read()
        data = json.loads(response.decode('utf-8'))
        return data