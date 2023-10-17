from TripHelper.Graph.Node import Point
from TripHelper.Places.NationalParks import NationalPark
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Trip import Trip

import matplotlib.pyplot as plt
road_testing_path = "TripHelper/data/road_testing.txt"
key_path = "TripHelper/Scrapers/keys.txt"

trip = Trip(road_testing_path, key_path)

print(trip.search_path_between_two_points("San Francisco", "Tahoe City"))

#trip.dump_graph(path_new)
