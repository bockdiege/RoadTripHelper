"""
Data Manager for the Graph.
It should be responsible for properly loading and saving data.
It also should be able to mine data with different apis

"""
from TripHelper.Loader.TypeManager import TypeManager
from TripHelper.Graph.Node import Point
from TripHelper.Graph.Graph import Graph


class GraphLoader:
    typeManager = TypeManager()

    def __int__(self):
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
        San Diego;32.7157,117.1611;City;Los Angeles,2|;Ugly,Shitty
        """
        arr = point_str.split(';')
        place_type = arr[2]

        new_place =  self.typeManager.string_to_type(place_type)(point_str)
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

        for i in arr[3].split('|'):
            name = i.split(',')[0]
            cost = float(i.split(',')[1])
            neighbour = graph.get_point_by_name(name)
            graph.add_connection(neighbour, start_point, cost)
        return

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

            # Get index of point in graph_arr
            index =graph.get_points().index(graph.get_point_by_name(start))
            neighbour_string = graph_arr[index].split(';')[3]

            # If already some neighbours are already specified the seperator must be added!
            if neighbour_string != "":
                neighbour_string += "|"
            neighbour_string += end + "," + cost

            new_point_str = graph_arr[index].split(';')
            new_point_str[3] = neighbour_string
            graph_arr[index] = ";".join(new_point_str)

        # Finally, write TripHelper into the specified path
        with open(path, 'w') as file:
            file.write("\n".join(graph_arr))
        return path

    def load_two_graphs(self, graph1: 'Graph', graph2: 'Graph'):
        """This function will take two graphs and will join them up
        general concept:
            graph1 is the one that will slowly glob up graph 2.
            How?
                -
        """
        #graph1.points = graph1.points + graph2.points
        #print(graph1.get_points()[-1].get_neighbours())
        #print(graph2.get_points()[-1].get_neighbours())
        point_strings = [data.get_point_without_neighbours_as_string() for data in graph2.get_points_data()]
        print("pointstrings", point_strings)
        # find all the matches:
        #matches = {}
        #for point1 in graph1.get_points():
        #    for point2 in graph2.get_points():
        #        if point1.get_data().get_pos() == point2.get_data().get_pos():
        #            print("Neighbours 1:", [vertex.get_end_point() for vertex in point1.get_neighbours()])
        #            print("Neighbours 2:", [vertex.get_end_point() for vertex in point2.get_neighbours()])
        #print(matches)
        pass
