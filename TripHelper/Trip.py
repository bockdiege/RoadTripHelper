"""

This is the uppermost class in this project, only this one should be initiated.
It currently has the following objects:
- Graph Loader
- Scrapper

In the future it should also have these things:
- GUI Manager
"""
from TripHelper.Loader.GraphLoader import GraphLoader
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
        Generally not satisfied with the location of this algorithm, but it needs a graph and scrappers,
        which this class has.
        How does this algorithm work:
            First step:
                Get an array of all the waypoints from one point to another
        """

        # Make a list of requests that have to be made
        # Think of matrix with width and length of the number of points. Each row is a start point, each column an
        # endpoint, thus the requests have to be the upper (or lower) triangle of the matrix. This code does that
        requests= []
        for i in range(0, len(self.graph.get_points())):
            for j in range(i+1, len(self.graph.get_points())):
                requests.append((self.graph.get_points()[i].get_data().get_pos(), self.graph.get_points()[j].get_data().get_pos()))
        print(requests)
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