import logging
import math
from itertools import permutations
from TripHelper.Graph.Edge import Edge
from TripHelper.Graph.Node import Point


class Graph:
    points = []

    def __init__(self, points: list[Point], edges: list[Edge]):
        self.points = points
        self.edges = edges
        pass

    def add_single_point(self, point):
        positions = [position.get_pos() for position in self.get_points_data()]
        if point.get_data().get_pos() in positions:
            #print("Attempted to add point whose position was already in the graph.")
            return
        self.points.append(point)
        return point

    def add_point(self, point_added, point_origin, cost, extra: 'str'):
        """Preferred method of adding points"""
        if point_added == point_origin:  # This is to prevent shot circuits
            if point_added not in self.points:
                self.add_single_point(point_added)      # add the point
            return
        self.add_single_point(point_added)      # add the point
        self.add_connection(point_added, point_origin, cost, extra)
        return

    def delete_point(self, point: 'Point'):
        neighbours = [edge.get_end_point() for edge in point.get_neighbours()]
        edges_to_be_deleted = point.get_neighbours()
        for neighbour in neighbours:
            for edge in neighbour.get_neighbours():
                if edge.get_end_point() == point:
                    # delete the edge of the neighbouring point:
                    neighbour.neighbours.remove(edge)
                    edges_to_be_deleted.append(edge)
            pass
        for edge in edges_to_be_deleted:
            self.edges.remove(edge)
            pass
        self.get_points().remove(point)

        return

    def add_connection(self, point1: 'Point', point2: 'Point', cost, extra: 'str'):
        for edge in self.edges:
            if edge.get_end_point() == point1 or edge.get_end_point() == point2:
                if edge.get_start_point() == point1 or edge.get_start_point() == point2:
                    #logging.critical(f"Connection between {point1} and {point2} already exists.")
                    return

        edge1 = Edge(point1, point2, cost, extra)
        point1.add_neighbour(edge1)
        self.add_edge(edge1)

        edge2 = Edge(point2, point1, cost, extra)
        point2.add_neighbour(edge2)
        self.add_edge(edge2)
        return

    def get_points_data(self):
        data = []
        for i in self.points:
            data.append(i.get_data())
        return data

    def get_points_name(self):
        names = []
        for i in self.points:
            names.append(i.get_data().get_name())
        return names

    def get_point_by_name(self, name) -> 'Point':
        """Returns the Point that has the input name"""
        index = self.get_points_name().index(name)
        return self.points[index]

    def get_points(self) -> list[Point]:
        return self.points

    def get_edges(self) -> list[Edge]:
        return self.edges

    def get_single_edges(self):
        return self.edges[::2]

    def add_edge(self, edge: 'Edge'):
        self.edges.append(edge)
        return edge

    def search(self, start: 'Point', end: 'Point') -> tuple[list, float]:
        def recursive_search(start: 'Point', end: 'Point', tree, path):
            path.insert(0, end)
            if start == end:
                return path
            new_end = tree[end]
            return recursive_search(start, new_end, tree, path)
        tree, cost_arr = self.dijkstra_search(start)
        # Get Trip
        result = recursive_search(start, end, tree, [])
        cost = cost_arr[self.get_points().index(end)]
        return result, cost

    def dijkstra_search(self, start: 'Point'):
        dist = [1e8] * len(self.get_points())  # Set the distance of other points to basically infinity
        dist[self.get_points().index(start)] = 0  # Set the distance of the start to 0

        previous_nodes = {}
        unvisited_nodes = list(self.get_points())

        while unvisited_nodes:
            # Get current node
            # This could be written a bit more clearly, but cant be bothered rn

            smallest_node_index = None
            for node in unvisited_nodes:
                index = self.get_points().index(node)
                if smallest_node_index == None:
                    smallest_node_index = index
                elif dist[index] < dist[smallest_node_index]:
                    smallest_node_index = index
            current_node = self.get_points()[smallest_node_index]

            # Vist current node's neighbours
            for neighbour in current_node.get_neighbours():
                # Update cost
                #print(type(neighbour.get_cost()))
                new_cost = dist[smallest_node_index] + neighbour.get_cost()
                #print("Graph Points", self.get_points(), "Neighbour", neighbour.get_end_point())
                #print(len(self.get_points()))
                if dist[self.get_points().index(neighbour.get_end_point())] > new_cost:
                    dist[self.get_points().index(neighbour.get_end_point())] = new_cost
                    previous_nodes[neighbour.get_end_point()] = current_node
            unvisited_nodes.remove(current_node)
        return previous_nodes, dist

    def get_shortest_path_between_points(self, start: 'Point', end: 'Point', legs: list[Point]):
        route_points = [start, end] + legs

        # Cant do dict comprehensions here (rather would take twice the time) :(
        tree_dict_path = {}
        tree_dict_cost = {}
        for point in route_points:
            tree_dict_path[point], tree_dict_cost[point] = self.dijkstra_search(point)

        # index_dict = {point: index for index, point in enumerate(route_points)}

        # Creat adjacency matrix
        cost_matrix = [[math.floor(tree_dict_cost[other_point][self.get_points().index(point)])
                       for other_point in route_points]
                       for point in route_points]

        # paths that will be searched
        paths = [[start] + perm + [end] for perm in list(map(list, permutations(legs)))]

        # create index dictionary for faster look up
        index_dict = {point: index for index, point in enumerate(route_points)}

        cost_of_paths = [sum([cost_matrix[index_dict[point]][index_dict[path[index + 1]]]
                         for index, point in enumerate(path[:-1])])
                         for path in paths]

        best_path = paths[cost_of_paths.index(min(cost_of_paths))]

        route = [point
                 for index, leg in enumerate(best_path[:-1])
                 for point in self.__recursive_search(leg,  best_path[index + 1], tree_dict_path[leg], [])[1:]]
        route.insert(0, best_path[0])

        return route, min(cost_of_paths)

    def __recursive_search(self, start_point: 'Point', end_point: 'Point', tree, path):
        path.insert(0, end_point)
        if start_point == end_point:
            return path
        new_end = tree[end_point]
        return self.__recursive_search(start_point, new_end, tree, path)

    def check_if_graph_has_double_edges(self, extra_message: 'str'):
        edges_seen = {}
        for edge in self.get_edges():
            start_end = (edge.get_start_point(), edge.get_end_point())
            end_start = (edge.get_end_point(), edge.get_start_point())

            edges_seen[start_end] = edges_seen.get(start_end, 0) + 1
            edges_seen[end_start] = edges_seen.get(end_start, 0) + 1
            if edges_seen.get(start_end) > 2:
                logging.critical(f"Graph has double edge at: {start_end}, {extra_message}")
            if edges_seen.get(end_start) > 2:
                logging.critical(f"Graph has double edge at: {end_start}, {extra_message}")

