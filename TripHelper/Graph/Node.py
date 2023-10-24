class Point:
      # Stores the Vertexes, that way costs and points are in one place

    def __init__(self, data):
        self.data = data
        self.neighbours = []

    def __repr__(self):
        return self.data.get_name()

    def get_data(self):
        return self.data

    def add_neighbour(self, neighbour_vertex):
        self.neighbours.append(neighbour_vertex)
        return True

    def get_neighbours(self):
        """ Returns the array, where the Vertexes are, that connect the points, are stored"""
        return self.neighbours

    def set_neighbours(self, neighbours):
        """
        Only use this if you know what you are doing!
        """
        self.neighbours = neighbours

    # def __str__(self): PLS IMPLEMENT THIS
    #    return f"Point with position at {self.data.get_}"





