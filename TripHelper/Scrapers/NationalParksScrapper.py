"""
Scraps data from the National Parks API
"""
import urllib.request, json
import logging

from TripHelper.Scrapers.ScrapperState import ScrapperState


class NationalParkScrapper:
    key = ""
    base_endcode = "https://developer.nps.gov/api/v1/parks"
    default_requests = 1000


    def __init__(self, key: 'str'):
        self.key = key
        self.HEADERS = {"X-Api-Key": key}
        self.remaining_requests = self.default_requests
        self.state = ScrapperState.LIBERAL
        self.request_limit = 10
        pass

    def __repr__(self):
        return "Scrapper for the National Park Service"

    def get_key(self):
        return self.key

    def get_park_by_code(self, code):
        endpoint = "?".join([self.base_endcode, f"parkCode={code}"])
        data = self.__make_call(endpoint)
        data_str = self.__create_string_from_nps_data(data["data"])[0]
        return data_str

    def get_parks_by_state(self, state_code: 'str'):
        endpoint ="?".join([self.base_endcode, f"StateCode={state_code}"])
        data = self.__make_call(endpoint)
        data_str = self.__create_string_from_nps_data(data["data"])
        return data_str

    def __create_string_from_nps_data(self, data):
        """ Sample
        Yosemite;32.7157,117.1611;NP;;Very Nice
        Things that are wanted from the data point:
        Name, code, lat, long, Activities?, description
        directions
        entrance fee
        weatherInto
        """
        parks_str_arr = []
        for data_point in data:
            name = data_point["name"]
            lat = data_point["latitude"]
            long = data_point["longitude"]
            latlong = ",".join([lat, long])
            weather_info = data_point["weatherInfo"]
            description = data_point["description"]
            park_code = data_point["parkCode"]
            entrance_fees = data_point["entranceFees"]
            #print("private vehicle: ", entrance_fees[0])
            #print("cost on foot", entrance_fees[2])
            #cost_private_vehicle = entrance_fees[0]["cost"]
            #cost_on_foot = entrance_fees[2]["cost"]
            #costs = ",".join([cost_private_vehicle, cost_on_foot])
            extra_data = "|".join([park_code, description, weather_info])
            park_string = ";".join([name, latlong, "NP", "", extra_data])
            parks_str_arr.append(park_string)
        return parks_str_arr

    def __make_call(self, endpoint):
        if self.state == ScrapperState.LOCKED:
            logging.warning("National Park Scrapper is currently locked, only a single call that will update the state "
                            "will go through")
            return self.__execute_call("https://developer.nps.gov/api/v1/parks?limit=1")
        if self.state == ScrapperState.FILL:
            logging.info("National Park Scrapper is currently in FILL mode, so your call will not go through,"
                         " as this mode is not used with this scrapper, thus something must have gone wrong")
            return self.__execute_call("https://developer.nps.gov/api/v1/parks?limit=1")

        return self.__execute_call(endpoint)

    def __execute_call(self, endpoint):
        """
        Never call this function, ever. For making calls to the NPS API call __make_call()
        """
        req = urllib.request.Request(endpoint, headers=self.HEADERS)
        response_raw = urllib.request.urlopen(req)
        self.remaining_requests = int(response_raw.getheader('X-Ratelimit-Remaining'))
        response = response_raw.read()
        data = json.loads(response.decode('utf-8'))
        self.update_state()
        # print(r.getheaders()) Important code!
        return data

    def update_state(self):
        """
        Updates the state, based on how many requests are remaining.
        Locks the Scrapper if less than 20 requests are remaining, these are meant as a buffer
         incase the state should be changed again, which requires a call
        """
        logging.info(f"Remaining requests: {self.remaining_requests}")
        print(f"Remaining requests: {self.remaining_requests}")
        if self.remaining_requests <= 20:
            self.state = ScrapperState.LOCKED
        pass

    def set_state(self, state):
        self.state = state
        return state

# Configure API request
# endpoint = "https://developer.nps.gov/api/v1/parks?stateCode=me"
# HEADERS = {"X-Api-Key":"INSERT_API_KEY_HERE"}
# req = urllib.request.Request(endpoint,headers=HEADERS)
# Additional code would follow
