"""
This Scrapper gets data from the OSRM api
"""
import urllib.request, json
import polyline

from TripHelper.Graph.Node import Point
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Scrapers.ScrapperState import ScrapperState


class OSRMScrapper:

    def __init__(self):
        self.state = ScrapperState.LIBERAL
        print("OSRM Scrapper initialised")
        return

    def get_direction_between_two_points(self, pos1, pos2):
        url = f"http://router.project-osrm.org/route/v1/driving/{pos1[1]},{pos1[0]};{pos2[1]},{pos2[0]}"
        data_raw = self.__execute_call(url)
        #print(data_raw)
        data = data_raw["routes"][0]
        geometry_encoded = data["geometry"]
        geometry_decoded = polyline.decode(geometry_encoded)
        geometry_decoded = [f"{point[0]},{point[1]}" for point in geometry_decoded]
        return geometry_decoded

    def get_dir_and_cost_between_two_points(self, pos1, pos2) -> tuple[str, float]:
        url = f"http://router.project-osrm.org/route/v1/driving/{pos1[1]},{pos1[0]};{pos2[1]},{pos2[0]}"
        data_raw = self.__execute_call(url)
        data = data_raw["routes"][0]
        geometry_encoded = data["geometry"]
        duration = float(data["duration"])
        return geometry_encoded, duration

    def get_nearest_street(self, pos1):
        url = f"http://router.project-osrm.org/nearest/v1/driving/{pos1[1]},{pos1[0]}?number=1"
        data_raw = self.__execute_call(url)
        waypoint = data_raw["waypoints"][0]
        name = waypoint["name"]
        position = waypoint["location"]
        #print(position)
        return position

    def get_roads_from_points(self, points):

        # Make a list of requests that have to be made
        # Think of matrix with width and length of the number of points. Each row is a start point, each column an
        # endpoint, thus the requests have to be the upper (or lower) triangle of the matrix. This code does that
        requests = []
        for i in range(0, len(points)):
            for j in range(i+1, len(points)):
                requests.append((points[i].get_data().get_pos(), points[j].get_data().get_pos()))

        print("requests:", len(requests))
        print("predicted amount of requests: ", (len(points)**2 - len(points))/2)
        # Execute the requests
        roads = []
        for i, request in enumerate(requests):
            pos0 = request[0]
            pos1 = request[1]
            road_path = self.get_direction_between_two_points(pos0, pos1)
            arr = []
            for j, position in enumerate(road_path):
                road_segment = RoadSegment(f"{i}-{j};{position};Road;;")
                arr.append(Point(road_segment))
            roads.append(arr)
        return roads

    def __execute_call(self, url):
        print(f"Requested Data from following URL: {url}")
        req = urllib.request.Request(url)
        response_raw = urllib.request.urlopen(req)
        response = response_raw.read()
        data = json.loads(response.decode('utf-8'))
        return data