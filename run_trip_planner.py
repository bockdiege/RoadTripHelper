import sys

from TripHelper.GUI.Plotter import Plotter
from TripHelper.Graph.Node import Point
from TripHelper.Places.NationalParks import NationalPark
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Trip import Trip
import matplotlib.pyplot as plt

road_testing_path = "TripHelper/data/road_testing.txt"
test_data_path = "TripHelper/data/test_data.txt"
path_new = "TripHelper/data/test_data_new.txt"
key_path = "TripHelper/Scrapers/keys.txt"

trip = Trip("TripHelper/data/california.txt", key_path)

#trip.get_nationalparks_by_state_code("ca")
#trip.init_road_network_of_points()

#trip.dump_graph("TripHelper/data/california.txt")
print("Number of points in Graph:", len(trip.graph.get_points()))
print("Size of Trip", sys.getsizeof(trip.graph.get_points()))
#print(trip.search_path_between_two_points("San Francisco", "Mojave"))
#print(trip.search_path_between_two_points("San Francisco", "Sacramento"))
#print(trip.search_path_between_two_points("Los Angeles", "Joshua Tree"))
#print(trip.search_path_between_two_points("Death Valley", "Yosemite"))

search_result, cost = trip.search_path_between_two_points("San Francisco", "San Diego")

#trip.loader.get_polyline(search_result)
#print(search_result)
#trip.dump_graph(path_new)

poly = trip.loader.get_polyline(search_result)
print(poly)
plotter = Plotter()

plotter.plot_points_and_polyline(trip.loader.get_points_by_type(trip.graph, ["Road"], True), poly)
