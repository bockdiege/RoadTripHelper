from TripHelper.Graph.Node import Point
from TripHelper.Places.NationalParks import NationalPark
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Trip import Trip
import matplotlib.pyplot as plt

road_testing_path = "TripHelper/data/road_testing.txt"
test_data_path = "TripHelper/data/test_data.txt"
path_new = "TripHelper/data/test_data_new.txt"
key_path = "TripHelper/Scrapers/keys.txt"

trip1 = Trip(road_testing_path, key_path)
trip2 = Trip(test_data_path, key_path)

trip1.loader.load_two_graphs(trip1.graph, trip2.graph)
#trip.build_road_network_of_points()
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
