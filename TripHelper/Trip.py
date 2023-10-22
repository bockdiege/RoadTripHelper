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
            2:
                Execute the requests and get the points that map out the road.
            3:
                Create a graph of these roads
                The graph will automatically filter out redundancies in points
        """
        roads = self.scrapper.osrm.get_roads_from_points(self.graph.get_points())
        road_graph = Graph([], [])

        for road in roads:
            self.add_road(road, road_graph)
        return road_graph

    def add_road(self, road_point_arr, graph: 'Graph'):
        # Add the first point of the road manually. It is still important to check if the points already exists.
        positions = [data.get_pos() for data in graph.get_points_data()]

        if road_point_arr[0].get_data().get_pos() in positions:
            index = positions.index(road_point_arr[0].get_data().get_pos())
            road_point_arr[0] = graph.get_points()[index]
        else:
            graph.add_single_point(road_point_arr[0])

        # Now add the road to the graph.
        for index, point in enumerate(road_point_arr[:-1]):
            positions = [data.get_pos() for data in graph.get_points_data()]

            point_to_be_added = road_point_arr[index + 1]
            # Point position might already be in the graph. In this case the point that is already there should be used.
            if point.get_data().get_pos() in positions:
                index_point_actual = positions.index(point.get_data().get_pos())
                point = graph.get_points()[index_point_actual]

            if point_to_be_added.get_data().get_pos() not in positions:
                graph.add_point(point_to_be_added, point, 0)
            else:
                # Point position is in the Graph. Get the point that already is in the graph with the same position.
                index_actual = positions.index(point_to_be_added.get_data().get_pos())
                point_to_be_added_actual = graph.get_points()[index_actual]

                neighbours = [vertex.get_end_point() for vertex in point.get_neighbours()]
                if point_to_be_added_actual not in neighbours:
                    graph.add_connection(point_to_be_added_actual, point, 0)
        return graph

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