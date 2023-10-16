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
from TripHelper.Scrapers.ScrapperState import ScrapperState


class NationalPark(PlaceInterface):
    state = ScrapperState.LIBERAL

    def __init__(self, name, pos, extra):
        self.pos = pos
        self.name = name
        self.extra = extra

    def __str__(self):
        return f"{self.name}"
        # return f"The City of {self.name}, which is located at: {self.pos}"

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos

    def get_extra(self):
        return self.extra
