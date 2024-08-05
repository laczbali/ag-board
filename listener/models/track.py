import json
import os


class Track:

    location_lookup = None
    route_lookup = None

    def __init__(self, location_id, route_id):
        self.location = Track.__location_by_id(location_id)
        self.route = Track.__route_by_id(route_id)


    def __str__(self):
        return f'{self.route}, {self.location}'


    def __location_by_id(location_id):
        Track.__load_id_data()
        return Track.location_lookup.get(location_id, "N/A")


    def __route_by_id(route_id):
        Track.__load_id_data()
        return Track.route_lookup.get(route_id, "N/A")


    def __load_id_data():
        if not Track.location_lookup or not Track.route_lookup:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ids_file = os.path.join(current_dir, "../", "ids.json")
            ids_data = json.load(open(ids_file))
            
            locations = ids_data["locations"]
            Track.location_lookup = {location["id"]: location["name"] for location in locations}
            routes = ids_data["routes"]
            Track.route_lookup = {route["id"]: route["name"] for route in routes}
            