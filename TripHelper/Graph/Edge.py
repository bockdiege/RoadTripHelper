#from Trips.TripHelper.Node import Point
#that causes a circular input


class Edge:
    def __init__(self, point1: 'Point', point2: 'Point', cost, extra: 'str'):
        self.cost = cost
        self.point1 = point1
        self.point2 = point2
        self.extra = extra
        return

    def __repr__(self):
        return f"O: {self.get_start_point()}, N:{self.get_end_point()}, C: {self.get_cost()}, E: {self.extra}"

    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost
        return self.cost

    def get_end_point(self):
        return self.point2

    def get_extra(self):
        return self.extra

    def set_extra(self, extra: 'str'):
        self.extra = extra
        return self.extra

    def get_start_point(self):
        return self.point1
