"""

This is the uppermost class in this project, only this one should be initiated.
It currently has the following objects:
- Graph Loader
- Scrapper

In the future it should also have these things:
- GUI Manager
"""
from TripHelper.Graph.Graph import Graph
from TripHelper.Graph.Node import Point
from TripHelper.Loader.GraphLoader import GraphLoader
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Scrapers.Scrapper import Scrapper


class Trip:

    def __init__(self, path: 'str', keys: 'str'):
        self.path = path    # Technically unnecessary
        self.loader = GraphLoader()
        self.scrapper = Scrapper(keys)
        self.graph = self.load_graph(self.path)

    def get_nationalparks_by_state_code(self, state_code: 'str'):
        """
        Known state codes:
        California - ca
        Nevada - nv
        Utah - ut
        Nebraska - ne
        """
        parks = self.scrapper.nps.get_parks_by_state(state_code)
        for np in parks:
            self.loader.load_point(np, self.graph)
        return

    def search_path_between_two_points(self, start: 'str', end: 'str'):
        return self.graph.search(self.graph.get_point_by_name(start), self.graph.get_point_by_name(end))

    def build_road_network_of_points(self):
        """
        Builds the necessary road network for the graph.
        How does this algorithm work:
            First step:
                Get an array of requests that have to be made by the OSRM scrapper.
                req(n) = (n^2 - n)/2, with req(n) being the number of requests, and n the number of points in the graph.
                In the future this number of requests should be pruned further.
        """

        # Make a list of requests that have to be made
        # Think of matrix with width and length of the number of points. Each row is a start point, each column an
        # endpoint, thus the requests have to be the upper (or lower) triangle of the matrix. This code does that
        requests =  []
        for i in range(0, len(self.graph.get_points())):
            for j in range(i+1, len(self.graph.get_points())):
                requests.append((self.graph.get_points()[i].get_data().get_pos(), self.graph.get_points()[j].get_data().get_pos()))

        print("requests:", len(requests))
        print("predicted amount of requests: ", (len(self.graph.get_points())**2 - len(self.graph.get_points()))/2)

        road_positions = []
        for request in requests:
            pos0 = request[0]
            pos1 = request[1]
            road_path = self.scrapper.osrm.get_direction_between_two_points(pos0, pos1)
            road_positions.append(road_path)
        # This algorithm will need a graph merge function, but that should not be a problem to implement
        road_positions = [position for road_path in road_positions for position in road_path]   # Flatten the road network

        num_roads_old = len(road_positions)

        road_network = []
        for index, position in enumerate(road_positions):
            segment = RoadSegment(f"{index};{position}")
            road_network.append(Point(segment))

        road_graph = Graph([], [])
        road_graph.add_single_point(road_network[0])
        for index, road_segment in enumerate(road_network[1:-1]):
            road_graph.add_point(road_network[index + 1], road_segment, 0)
        num_roads_new = len(road_graph.get_points())
        print(f"{num_roads_old - num_roads_new} redundancies found in road network.")
        return road_graph.get_points_data()

    def get_path(self):
        return self.path

    def set_path(self, new_path):
        self.path = new_path
        return self.load_graph(self.path)

    def get_graph(self):
        return self.graph

    def load_graph(self, path):
        """
        Loads and then returns a graph from a given path.
        """
        if path != self.path:
            self.set_path(path)
        return self.loader.load_file(path)

    def dump_graph(self, path):
        """
        Dumps the path to a given location,
        returns the path
        """
        return self.loader.dump_graph(self.graph, path)


"""
Documentation 
http://project-osrm.org/docs/v5.24.0/api/#
"""