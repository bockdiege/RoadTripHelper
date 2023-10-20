from TripHelper.Graph.Node import Point
from TripHelper.Places.NationalParks import NationalPark
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Trip import Trip
import matplotlib.pyplot as plt

road_testing_path = "TripHelper/data/test_data.txt"
path_new = "TripHelper/data/test_data_new.txt"
key_path = "TripHelper/Scrapers/keys.txt"

trip = Trip(road_testing_path, key_path)
#trip.build_road_network_of_points()
#trip.get_nationalparks_by_state_code("ca")
#trip.get_nationalparks_by_state_code("ut")
road_data = trip.build_road_network_of_points()

x = []
y = []
for data in road_data:
    x.append(data.get_pos()[0])
    y.append(data.get_pos()[1])
print(x)
print(y)
x_1 = []
y_1 = []
for data in trip.graph.get_points_data():
    x_1.append(data.get_pos()[0])
    y_1.append(data.get_pos()[1])

plt.errorbar(y,x, fmt=".")
plt.errorbar(y_1, x_1, fmt = "x")
plt.savefig("pesto")

#trip.dump_graph(path_new)
