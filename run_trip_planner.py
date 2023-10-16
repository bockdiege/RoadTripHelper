from TripHelper.Graph.Node import Point
from TripHelper.Places.NationalParks import NationalPark
from TripHelper.Places.RoadSegment import RoadSegment
from TripHelper.Trip import Trip


path_existing = "TripHelper/data/test_data.txt"
path_new = "TripHelper/data/test_data_new.txt"

trip = Trip(path_existing)

start = "Tahoe City"
destination = "San Diego"

print(trip.search_path_between_two_points(start, destination))

trip.get_nationalparks_by_state_code("ut")

sf = "San Francisco"
sacra = "Sacramento"

pos_sf = trip.get_graph().get_point_by_name(sf).get_data().get_pos()
pos_scara = trip.get_graph().get_point_by_name(sacra).get_data().get_pos()


trip.dump_graph(path_new)