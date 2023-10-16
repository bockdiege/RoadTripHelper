from TripHelper.Interfaces.Place import PlaceInterface


class City(PlaceInterface):
    def __init__(self, name, pos, extra):
        self.pos = pos
        self.name = name
        self.extra = extra

    def __str__(self):
        return f"{self.name}"
        #return f"The City of {self.name}, which is located at: {self.pos}"

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def get_extra(self):
        return self.extra
