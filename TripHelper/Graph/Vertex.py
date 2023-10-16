#from Trips.TripHelper.Node import Point
#that causes a circular input


class Vertex:
    def __init__(self, point1: 'Point', point2: 'Point', cost):
        self.cost = cost
        self.point1 = point1
        self.point2 = point2
        return

    def __repr__(self):
        return f"O: {self.get_start_point()}, N:{self.get_end_point()}, C: {self.get_cost()}"

    def get_cost(self):
        return self.cost

    def get_end_point(self):
        return self.point2

    def get_start_point(self):
        return self.point1
