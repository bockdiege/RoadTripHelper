from TripHelper.Graph.Node import Point
from TripHelper.Places.NationalParks import NationalPark
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Trip import Trip
import matplotlib.pyplot as plt

road_testing_path = "TripHelper/data/road_testing.txt"
test_data_path = "TripHelper/data/test_data.txt"
path_new = "TripHelper/data/test_data_new.txt"
key_path = "TripHelper/Scrapers/keys.txt"

trip = Trip(path_new, key_path)

#trip.graph.delete_point(trip.graph.get_point_by_name("San Diego"))
#print(trip.graph.get_point_by_name("Napa").get_neighbours())
#print(trip.graph.get_single_vertexes())
#trip.dump_graph("delete_testing.txt")
trip.loader.compress_roads(trip.graph)
trip.dump_graph("compressed?")


#trip1.loader.load_two_graphs(trip1.graph, trip2.graph)
#trip.build_road_network_of_points()
#trip.loader.compress_roads(trip.graph)

#print(trip.search_path_between_two_points("San Francisco", "Sacramento"))
#trip.dump_graph(path_new)


#trip.scrapper.nps.get_park_by_code("yose")

#trip = Trip(path_new, key_path)
#print(trip.search_path_between_two_points("San Francisco", "Sacramento"))
#trip.get_nationalparks_by_state_code("ca")
#trip.get_nationalparks_by_state_code("ut")
#road_graph = trip.build_road_network_of_points()
#trip.graph = road_graph2w3
#trip.dump_graph("TripHelper/data/roads.txt")


#road_data = road_graph.get_points_data()
#number_of_neighbours = [len(point.get_neighbours()) for point in road_graph.get_points()]
#print("Number of neighbours", number_of_neighbours)

#test = "qwertyuiop["
#x = test.replace("qwert", "a")
#print(x)
"""
x = []
y = []
for data in road_data:
    x.append(data.get_pos()[0])
    y.append(data.get_pos()[1])
#print(x)
#print(y)
x_1 = []
y_1 = []
for data in trip.graph.get_points_data():
    x_1.append(data.get_pos()[0])
    y_1.append(data.get_pos()[1])

plt.plot(y,x)
plt.errorbar(y_1, x_1, fmt="x")
plt.savefig("pesto")

trip.graph = road_graph
trip.dump_graph(path_new)

"""
