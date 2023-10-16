"""
This class is supposed to make adding new types of data points easy.

Its task is twofold, firstly, to return the string Identifier of an object,
and if possible return the object
"""
from TripHelper.Places.Cities import City
from TripHelper.Places.NationalParks import NationalPark


class TypeManager:

    def __int__(self):
        pass

    def type_to_string(self, obj: 'object') -> 'str':
        if isinstance(obj, City):
            return "City"
        elif isinstance(obj, NationalPark):
            return "NP"
        return "NoType"

    def string_to_type(self, string: 'str') -> 'object':
        if string == "City":
            return City
        if string == "NP":
            return NationalPark
        pass

