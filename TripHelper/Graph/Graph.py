from TripHelper.Graph.Vertex import Vertex
from TripHelper.Graph.Node import Point


class Graph:
    points = []

    def __init__(self, points: list[Point], vertexes: list[Vertex]):
        self.points = points
        self.vertexes = vertexes
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
        neighbours = [vertex.get_end_point() for vertex in point.get_neighbours()]
        vertexes_to_be_deleted = point.get_neighbours()
        for neighbour in neighbours:
            for vertex in neighbour.get_neighbours():
                if vertex.get_end_point() == point:
                    # delete the vertex of the neighbouring point:
                    neighbour.neighbours.remove(vertex)
                    vertexes_to_be_deleted.append(vertex)
            pass
        for vertex in vertexes_to_be_deleted:
            self.vertexes.remove(vertex)
            pass
        self.get_points().remove(point)

        return

    def add_connection(self, point1: 'Point', point2: 'Point', cost, extra: 'str'):
        vertex1 = Vertex(point1, point2, cost, extra)
        point1.add_neighbour(vertex1)
        self.add_vertex(vertex1)

        vertex2 = Vertex(point2, point1, cost, extra)
        point2.add_neighbour(vertex2)
        self.add_vertex(vertex2)
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

    def get_vertexes(self) -> list[Vertex]:
        return self.vertexes

    def get_single_vertexes(self):
        return self.vertexes[::2]

    def add_vertex(self, vertex: 'Vertex'):
        self.vertexes.append(vertex)
        return vertex

    def search(self, start: 'Point', end: 'Point'):
        def recursive_search(start: 'Point', end: 'Point', tree, path):
            path.insert(0,end)
            if start == end:
                return path
            new_end = tree[end]
            return recursive_search(start, new_end, tree, path)

        tree, cost_arr = self.dijkstra_search(start)
        # Get Trip

        test = recursive_search(start, end, tree, [])
        cost = cost_arr[self.get_points().index(end)]
        return test, cost

    def dijkstra_search(self, start: 'Point'):
        #graph_points = self.get_points()
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

    """
    Following idea for searching for a path that finds the shortest path between multiple poitns, i.e.
    start, point_i, end
    
    dijkstra search the shit out of every single path and store that information. Proceed from there
    That should be a lot less computationally heavy than for looping every single point for every single
    possibility slay
    """
