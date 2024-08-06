import os
import json


class Vehicle:
    
    group_lookup = None
    manufacturer_lookup = None
    name_lookup = None

    def __init__(self, group_id, manufacturer_id, name_id):
        self.group_name = Vehicle.__group_name_by_id(group_id)
        self.manufacturer = Vehicle.__manufacturer_by_id(manufacturer_id)
        self.name = Vehicle.__name_by_id(name_id)
        

    def __str__(self):
        return f'{self.name} [{self.group_name}]'
    

    def create_table():
        return """CREATE TABLE IF NOT EXISTS vehicles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_name TEXT,
                    manufacturer TEXT,
                    name TEXT
                )"""
    

    def __group_name_by_id(group_id):
        Vehicle.__load_id_data()
        return Vehicle.group_lookup.get(group_id, "N/A")
    

    def __manufacturer_by_id(manufacturer_id):
        Vehicle.__load_id_data()
        return Vehicle.manufacturer_lookup.get(manufacturer_id, "N/A")
    

    def __name_by_id(name_id):
        Vehicle.__load_id_data()
        return Vehicle.name_lookup.get(name_id, "N/A")
    

    def __load_id_data():
        if not Vehicle.group_lookup or not Vehicle.manufacturer_lookup or not Vehicle.name_lookup:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ids_file = os.path.join(current_dir, "../", "ids.json")
            ids_data = json.load(open(ids_file))
            
            groups = ids_data["vehicle_classes"]
            Vehicle.group_lookup = {group["id"]: group["name"] for group in groups}
            manufacturers = ids_data["vehicle_manufacturers"]
            Vehicle.manufacturer_lookup = {manufacturer["id"]: manufacturer["name"] for manufacturer in manufacturers}
            names = ids_data["vehicles"]
            Vehicle.name_lookup = {name["id"]: name["name"] for name in names}