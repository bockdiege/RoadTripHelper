import math
import sys

from TripHelper.GUI.Plotter import Plotter
from TripHelper.Graph.Node import Point
from TripHelper.Places.NationalParks import NationalPark
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Trip import Trip

road_testing_path = "TripHelper/data/road_testing.txt"
test_data_path = "TripHelper/data/test_data.txt"
path_new = "TripHelper/data/test_data_new.txt"
key_path = "TripHelper/Scrapers/keys.txt"
minimum = "TripHelper/data/minimum.txt"
utah = "TripHelper/data/utah.txt"

trip = Trip(utah, key_path)
#trip.get_nationalparks_by_state_code("ut")
#trip.init_road_network_of_points()
#trip.dump_graph(utah)

# print("Number of points in Graph:", len(trip.graph.get_points()))
#sf = trip.graph.get_point_by_name("San Francisco")
#napa = trip.graph.get_point_by_name("Napa")
#sacra = trip.graph.get_point_by_name("Sacramento")
#tahoe = trip.graph.get_point_by_name("Tahoe City")
#la = trip.graph.get_point_by_name("Los Angeles")
#path, cost = trip.graph.get_shortest_path_between_points(sf, tahoe, [napa, sacra, la])
#print("San Francisco to San Francisco", trip.search_path_between_two_points("San Francisco", "San Francisco"))

#path, cost = trip.search_path_between_two_points("Fresno", "Tahoe City")
# arches, capitol reef, bryce, natural bridges, rainbow bridge, und dann wieder zion
zion = trip.graph.get_point_by_name("Zion")
capitol_reef = trip.graph.get_point_by_name("Capitol Reef")
bryce = trip.graph.get_point_by_name("Bryce Canyon")
natural_bridge = trip.graph.get_point_by_name("Natural Bridges")
rainbow_bridge = trip.graph.get_point_by_name("Rainbow Bridge")
salt = trip.graph.get_point_by_name("Salt Lake City")
road = trip.graph.get_point_by_name("152-24")

path, cost = trip.graph.get_shortest_path_between_points(zion, road, [])

plotter = Plotter()

#print("Number of Points in path", len(path))
print(cost)
#plotter.plot_points([zion, bryce])
#plotter.plot_route(path)
print(path)
for point in path:
    plotter.plot_point_and_edges(point)
#plotter.plot_points(trip.loader.get_points_by_type(trip.graph, ["Road"], True))
#for edge in trip.graph.get_single_edges():
#    plotter.plot_extra_of_edge(edge)

#for edge in trip.graph.get_single_edges():
#    plotter.plot_extra_of_edge(edge)
plotter.finalise_plot("utah", False)

