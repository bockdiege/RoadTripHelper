from TripHelper.Interfaces.Place import PlaceInterface


class City(PlaceInterface):
    def __init__(self, string: 'str'):
        arr = string.split(';')
        self.name = arr[0]
        self.pos = (float(arr[1].split(',')[0]), float(arr[1].split(',')[1]))
        self.extra = arr[-1]
        self.point_without_neighbours_as_string = string

    def __str__(self):
        return f"{self.name}"
        # return f"The City of {self.name}, which is located at: {self.pos}"

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def get_extra(self):
        return self.extra

    def set_pos(self, pos):
        self.pos = pos

    def get_point_without_neighbours_as_string(self):
        new_point_str = self.point_without_neighbours_as_string.split(';')
        new_point_str[3] = ""
        self.point_without_neighbours_as_string = ";".join(new_point_str)
        return self.point_without_neighbours_as_string
