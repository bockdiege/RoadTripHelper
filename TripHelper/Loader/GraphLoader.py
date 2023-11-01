"""
Data Manager for the Graph.
It should be responsible for properly loading and saving data.
It also should be able to mine data with different apis

"""
from polyline import polyline

from TripHelper.Loader.TypeManager import TypeManager
from TripHelper.Graph.Node import Point
from TripHelper.Graph.Graph import Graph
from TripHelper.Places.RoadSegment import RoadSegment


class GraphLoader:

    def __init__(self):
        self.typeManager = TypeManager()
        pass

    def load_file(self, path: 'str') -> 'Graph':
        """
        Loads and returns a Graph from given file path.
        """

        with open(path) as file:
            list_of_points_in_file = file.read().split('\n')
            list_of_points = []
            for point in list_of_points_in_file:
                list_of_points.append(self.__generate_point_from_str(point))
            # Create Graph
            graph = Graph(list_of_points, [])

            # Connect all the points to each other
            for point in list_of_points_in_file:
                self.__generate_vertexes_from_str(point, graph)
        return graph

    def __generate_point_from_str(self, point_str: 'str') -> 'Point':
        """
        Returns a point with all its bits and bobs from a string.
        Format of string must be:
        Name; long lat; Type; (Neighbour_i, cost_i); (Tags); Description
        Description is the extra data that each type
        Sample string:
        San Diego;32.7157,117.1611;City;Los Angeles,2/;Ugly,Shitty
        """
        arr = point_str.split(';')
        place_type = arr[2]

        new_place = self.typeManager.string_to_type(place_type)(point_str)
        new_point = Point(new_place)
        return new_point

    def __generate_vertexes_from_str(self, point_str: 'str', graph: 'Graph'):
        """
        Takes a point string and a graph. Figures out what the neighbours of the point are and then
        actually creates such connections in the Graph
        """
        arr = point_str.split(';')
        start_point = graph.get_point_by_name(name=arr[0])

        if arr[3] == "":
            return

        for i in arr[3].split('/'):
            name = i.split(',')[0]
            cost = float(i.split(',')[1])
            extra = i.split(',')[2]

            neighbour = graph.get_point_by_name(name)
            graph.add_connection(neighbour, start_point, cost, extra)
        return

    def compress_roads(self, graph):
        # Points that should be compressed:
        # Roads that only neighbour two other roads

        roads_in_graph = self.get_points_by_type(graph, ["Road"], False)

        # print([len(point.get_neighbours()) for point in roads_in_graph])
        for road_point in roads_in_graph:
            # Filter out those road points that only have two neigbours that are roads
            neighbours = [vertex.get_end_point() for vertex in road_point.get_neighbours()]
            if len(neighbours) == 2:
                if isinstance(neighbours[0].get_data(), RoadSegment):
                    if isinstance(neighbours[1].get_data(), RoadSegment):
                        graph.delete_point(road_point)
                        graph.add_connection(neighbours[0], neighbours[1], 0, "")
                pass
            else:
                continue

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
            # Case 1: Position of point is not in the graph.
            if point_to_be_added.get_data().get_pos() not in positions:
                graph.add_point(point_to_be_added, point, 0, "")
            else:
                # Case 2: Position of Point is in the Graph, but connection does not exist
                index_actual = positions.index(point_to_be_added.get_data().get_pos())
                point_to_be_added_actual = graph.get_points()[index_actual]

                neighbours = [vertex.get_end_point() for vertex in point.get_neighbours()]

                if point_to_be_added_actual not in neighbours:
                    graph.add_connection(point_to_be_added_actual, point, 0, "")
        return graph

    def load_point(self, point_str: 'str', graph: 'Graph'):
        """
        Loads a point with all its bits and bobs from a string.
        Format of string must be:
        Name; long lat; Type; (Neighbour_i, cost_i); (Tags); Description
        Description is optional but highly encouraged
        Sample string:
        San Diego;32.7157,117.1611;City;Los Angeles,2;Ugly,Shitty
        """
        new_point = self.__generate_point_from_str(point_str)
        graph.add_single_point(new_point)
        self.__generate_vertexes_from_str(point_str, graph)
        return graph

    def dump_graph(self, graph, path):
        """
        Writes the given TripHelper into a file at the given path.
        """
        graph_arr = [[]] * (len(graph.get_points()))

        for point_index, point in enumerate(graph.get_points()):
            data = point.get_data()
            point_string = data.get_point_without_neighbours_as_string()
            graph_arr[point_index] = point_string

        # Specify the neighbours:
        for vertex in graph.get_single_vertexes():
            start = vertex.get_start_point().get_data().get_name()
            end = vertex.get_end_point().get_data().get_name()
            cost = str(vertex.get_cost())
            extra = vertex.get_extra()

            # Get index of point in graph_arr
            index = graph.get_points().index(graph.get_point_by_name(start))
            neighbour_string = graph_arr[index].split(';')[3]

            # If already some neighbours are already specified the seperator must be added!
            if neighbour_string != "":
                neighbour_string += "/"
            neighbour_string += ",".join([end, cost, extra])

            new_point_str = graph_arr[index].split(';')
            new_point_str[3] = neighbour_string
            graph_arr[index] = ";".join(new_point_str)

        # Finally, write TripHelper into the specified path
        with open(path, 'w') as file:
            file.write("\n".join(graph_arr))
        return path

    def get_points_by_type(self, graph, point_type_arr: list[str], complement: 'bool') -> list[Point]:
        """
        :param graph:
        :param point_type_arr: List of types that should be filtered
        :param complement: If true points named in type array will be returned,
                if false then those that are not of the type will be returned
        :return: array of points
        """
        # I am sure this code could be formatted better...
        if complement:
            arr = [point for point in graph.get_points() if
                   self.typeManager.type_to_string(point.get_data()) not in point_type_arr]
        else:
            arr = [point for point in graph.get_points() if
                   self.typeManager.type_to_string(point.get_data()) in point_type_arr]
        return arr

    def get_polyline(self, points: 'list[Point]'):
        geom = []
        for index, point in enumerate(points[:-1]):
            for vertex in point.get_neighbours():
                if vertex.get_end_point() == points[index + 1]:
                    extra = vertex.get_extra()
                    geometry_decoded = polyline.decode(extra)
                    geom += geometry_decoded
        line = polyline.encode(geom)
        return line
