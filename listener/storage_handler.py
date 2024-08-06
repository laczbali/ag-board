import sqlite3
import os

class StorageHandler:

    def __init__(self):
        self.__db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.db")
        self.__create_tables()


    def store_run(self, run_result, vehicle, track):
        vehicle_id = self.get_vehicle_id(vehicle)
        track_id = self.get_track_id(track)
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO runs (result, penalty, metadata, vehicle_id, track_id) VALUES (?, ?, ?, ?, ?)",
            (run_result.result_sec, run_result.penalty_sec, str(run_result.metadata), vehicle_id, track_id)
        )
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
        
        cursor.execute(
            "INSERT INTO vehicles (group_name, manufacturer, name) VALUES (?, ?, ?)",
            (vehicle.group_name, vehicle.manufacturer, vehicle.name)
        )
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
        
        cursor.execute(
            "INSERT INTO tracks (location, route) VALUES (?, ?)",
            (track.location, track.route)
        )
        conn.commit()
        conn.close()
        return cursor.lastrowid


    def __create_tables(self):
        vehicle_table = """
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_name TEXT,
            manufacturer TEXT,
            name TEXT
        )
        """
        track_table = """
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            route TEXT
        )
        """
        run_table = """
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            result REAL,
            penalty REAL,
            metadata TEXT,
            finished_at TEXT DEFAULT CURRENT_TIMESTAMP,
            vehicle_id INTEGER,
            track_id INTEGER
        )
        """
        conn = sqlite3.connect(self.__db_path)
        cursor = conn.cursor()
        cursor.execute(vehicle_table)
        cursor.execute(track_table)
        cursor.execute(run_table)
        conn.commit()
        conn.close()
