import os
import json


class RunAbort:

    gamemode_lookup = None
    abortreason_lookup = None

    def __init__(self, abort_after_sec, penalty_sec, gamemode_id, abortreason_id):
        self.abort_after_sec = abort_after_sec
        self.penalty_sec = penalty_sec
        self.reason = RunAbort.__abortreason_by_id(abortreason_id)
        self.metadata = {
            "gamemode": RunAbort.__gamemode_by_id(gamemode_id)
        }


    def __str__(self):
        return f"Abort after: {self.abort_after_sec}s ({self.reason})"
    

    def __gamemode_by_id(gamemode_id):
        RunAbort.__load_id_data()
        return RunAbort.gamemode_lookup.get(gamemode_id, "N/A")
    

    def __abortreason_by_id(abortreason_id):
        RunAbort.__load_id_data()
        return RunAbort.abortreason_lookup.get(abortreason_id, "N/A")
    

    def __load_id_data():
        if not RunAbort.gamemode_lookup or not RunAbort.abortreason_lookup:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ids_file = os.path.join(current_dir, "../", "ids.json")
            ids_data = json.load(open(ids_file))
            
            gamemodes = ids_data["game_mode"]
            abortreasons = ids_data["stage_result_status"]
            RunAbort.gamemode_lookup = {gamemode["id"]: gamemode["name"] for gamemode in gamemodes}
            RunAbort.abortreason_lookup = {abortreason["id"]: abortreason["name"] for abortreason in abortreasons}


    def sql_create():
        return """
        CREATE TABLE IF NOT EXISTS aborts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            abort_after REAL,
            penalty REAL,
            reason TEXT,
            metadata TEXT,
            aborted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            vehicle_id INTEGER,
            track_id INTEGER
        )
        """
    

    def sql_insert(self, vehicle_id, track_id):
        return (
            "INSERT INTO aborts (abort_after, penalty, reason, metadata, vehicle_id, track_id) VALUES (?, ?, ?, ?, ?, ?)",
            (self.abort_after_sec, self.penalty_sec, self.reason, json.dumps(self.metadata), vehicle_id, track_id)
        )