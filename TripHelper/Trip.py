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

    def __init__(self, path, keys):
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

    def get_path(self):
        return self.path

    def set_path(self, new_path):
        self.path = new_path
        return self.load_graph(self.path)

    def get_graph(self):
        return self.graph

    def load_graph(self, path):
        if path != self.path:
            self.set_path(path)
        return self.loader.load_file(path)

    def dump_graph(self, path):
        """
        Dumps the path to a given location,
        returns the path
        """
        return self.loader.dump_graph(self.graph, path)
