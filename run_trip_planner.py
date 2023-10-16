from TripHelper.Trip import Trip


path_existing = "TripHelper/data/test_data.txt"
path_new = "TripHelper/data/test_data_new.txt"

trip = Trip(path_existing)

start = "Tahoe City"
destination = "San Diego"

print(trip.search_path_between_two_points(start, destination))

trip.get_nationalparks_by_state_code("ut")

#sf = "San Francisco"
#sacra = "Sacramento"

#pos_sf = trip.get_graph().get_point_by_name(sf).get_data().get_pos()
#pos_scara = trip.get_graph().get_point_by_name(sacra).get_data().get_pos()

#print(pos_sf[0])
#print(pos_scara)
#print(trip.scrapper.testscrapper.request(pos_sf, pos_scara))

url = "http://router.project-osrm.org/route/v1/driving/13.388860,52.517037;13.397634,52.529407;13.428555,52.523219"
print(trip.scrapper.osrm.execute_call(url))
trip.dump_graph(path_new)





#data_loader = GraphLoader()
#path_existing = "/Users/pablo/PycharmProjects/pythonProject/Trips/TripHelper/data/test_data.txt"
#path_new = "/Users/pablo/PycharmProjects/pythonProject/Trips/TripHelper/data/test_data_new.txt"

#start = "San Francisco"
#destination = "San Diego"

#scrapper = Scrapper("Trips/TripHelper/Scrapers/keys.txt")

#test_graph = data_loader.load_file(path_existing)
#print(test_graph.search(test_graph.get_point_by_name(start), test_graph.get_point_by_name(destination)))

#yose_string = scrapper.nps.get_park_by_code("yose")
#print(yose_string)
#data_loader.load_point(yose_string, test_graph)
#california_nps = scrapper.nps.get_parks_by_state("nv")
#for np in california_nps:
#    data_loader.load_point(np, test_graph)

#data_loader.dump_graph(test_graph, path_new)
#test_graph = data_loader.load_file(path_new)
#print(test_graph.search(test_graph.get_point_by_name(start), test_graph.get_point_by_name(destination)))


# Scrapping baby

#print(scrapper.nps.get_parks_by_state("ca"))



