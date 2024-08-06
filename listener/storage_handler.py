import sqlite3
import os

from listener.models.run_result import RunResult
from listener.models.track import Track
from listener.models.vehicle import Vehicle

class StorageHandler:

    def __init__(self):
        self.__db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")
        self.__create_tables()


    def store_run(self, run_result, vehicle, track):
        vehicle_id = self.get_vehicle_id(vehicle)
        track_id = self.get_track_id(track)
        route_insert = run_result.sql_insert(vehicle_id, track_id)

        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(route_insert[0], route_insert[1])
        conn.commit()
        conn.close()


    def get_vehicle_id(self, vehicle):
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        results = cursor.execute(
            "SELECT id FROM vehicles WHERE group_name = ? AND manufacturer = ? AND name = ?",
            (vehicle.group_name, vehicle.manufacturer, vehicle.name)
        )
        vehicle_id = results.fetchone()
        if vehicle_id:
            conn.close()
            return vehicle_id[0]
        
        vehicle_insert = vehicle.sql_insert()
        cursor.execute(vehicle_insert[0], vehicle_insert[1])
        conn.commit()
        conn.close()
        return cursor.lastrowid
    

    def get_track_id(self, track):
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        results = cursor.execute(
            "SELECT id FROM tracks WHERE location = ? AND route = ?",
            (track.location, track.route)
        )
        track_id = results.fetchone()
        if track_id:
            conn.close()
            return track_id[0]
        
        track_insert = track.sql_insert()
        cursor.execute(track_insert[0], track_insert[1])
        conn.commit()
        conn.close()
        return cursor.lastrowid


    def __create_tables(self):
        vehicle_table = Vehicle.sql_create()
        track_table = Track.sql_create()
        run_table = RunResult.sql_create()

        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(vehicle_table)
        cursor.execute(track_table)
        cursor.execute(run_table)
        conn.commit()
        conn.close()
