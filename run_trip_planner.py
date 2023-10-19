from TripHelper.Graph.Node import Point
from TripHelper.Places.NationalParks import NationalPark
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Trip import Trip

import matplotlib.pyplot as plt
road_testing_path = "TripHelper/data/road_testing.txt"
path_new = "TripHelper/data/test_data_new.txt"
key_path = "TripHelper/Scrapers/keys.txt"

trip = Trip(road_testing_path, key_path)

trip.get_nationalparks_by_state_code("ut")


trip.dump_graph(path_new)
