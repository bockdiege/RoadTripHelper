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
        name = arr[0]
        pos = (float(arr[1].split(',')[0]), float(arr[1].split(',')[1]))
        extra = arr[-1]

        new_place = self.typeManager.string_to_type(place_type)(name, pos, extra)
        new_point = Point(new_place)
        return new_point

    def __generate_vertexes_from_str(self, point_str: 'str', graph: 'Graph'):
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

        # This creates the points, but does not specify the neighbours
        for point_index in range(0, len(graph.get_points())):
            """Remember, String Format Sample:
            San Diego;32.7157,117.1611;City;Los Angeles,2;Ugly,Shitty
            """
            data = graph.get_points()[point_index].get_data()
            name = data.get_name()
            lat = str(data.get_pos()[0])
            long = str(data.get_pos()[1])
            latlong = ",".join([lat,long])
            extra = data.get_extra()
            #type_str = self.type_to_string(data)
            type_str = self.typeManager.type_to_string(data)

            # Build string, but without neighbours
            #point_string = name + ";" + lat+ "," + long + ";" + type_str + ";" + ";"
            point_string = ";".join([name, latlong, type_str, "", extra])
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
