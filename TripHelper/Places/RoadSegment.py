"""
Class for National Parks.

Following information should be decoded in the extra string:
    - park code
    - description
    - weather info
    - costs
        - cost of entering per vehicle
        - cost of entering per foot
"""

from TripHelper.Interfaces.Place import PlaceInterface


class RoadSegment(PlaceInterface):

    def __init__(self, string: 'str'):
        arr = string.split(';')
        self.name = arr[0]
        self.pos = (float(arr[1].split(',')[0]), float(arr[1].split(',')[1]))
        #self.extra = arr[-1]
        self.point_without_neighbours_as_string = string

    def __repr__(self):
        return str(self.pos)

    def __str__(self):
        return f"{self.name}"
        # return f"The City of {self.name}, which is located at: {self.pos}"

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    #def get_extra(self):
    #    return self.extra

    def get_point_without_neighbours_as_string(self):
        new_point_str = self.point_without_neighbours_as_string.split(';')
        new_point_str[3] = ""
        self.point_without_neighbours_as_string = ";".join(new_point_str)
        return self.point_without_neighbours_as_string
