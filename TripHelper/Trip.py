"""

This is the uppermost class in this project, only this one should be initiated.
It currently has the following objects:
- Graph Loader
- Scrapper

In the future it should also have these things:
- GUI Manager
"""
import logging

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
        try:
            return self.graph.search(self.graph.get_point_by_name(start), self.graph.get_point_by_name(end))
        except KeyError:
            logging.critical(f"No connection between {start} and {end} found")

    def init_road_network_of_points(self):
        """
        Builds the necessary road network for the graph.
        """
        # TODO: if a graph already has points, these should now be included!
        # TODO: for that a method that returns only points of a certain type.
        roads = self.scrapper.osrm.get_roads_from_points(self.graph.get_points())

        # This connects the actual points to the Road Points
        n = len(self.graph.get_points())
        indexes = [int(n*i - i*(i+1)/2) for i, p in enumerate(self.graph.get_points())]

        self.graph.add_point(roads[-1][-1], self.graph.get_points()[-1], 0, "")     # this connects the last road
        # This connects the other points.
        for index, point in enumerate(self.graph.get_points()[:-2]):
            road = roads[indexes[index]]
            self.graph.add_point(road[0], point, 0, "")

        for road in roads:
            self.loader.add_road(road, self.graph)
        self.loader.compress_roads(self.graph)
        self.finalize_road_network()
        return self.graph

    def finalize_road_network(self):
        """
        Get the actual driving distance between the road points, as well as the polylines that show the
        """
        for vertex in self.graph.get_vertexes():
            geo, cost = self.scrapper.osrm.get_dir_and_cost_between_two_points(
                vertex.get_end_point().get_data().get_pos(),
                vertex.get_start_point().get_data().get_pos())
            vertex.set_cost(cost)
            vertex.set_extra(geo)
            pass
        pass

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