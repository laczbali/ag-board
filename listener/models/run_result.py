import os
import json


class RunResult:

    gamemode_lookup = None

    def __init__(self, result_sec, penalty_sec, gamemode_id):
        self.result_sec = result_sec
        self.penalty_sec = penalty_sec
        self.gamemode = RunResult.__gamemode_by_id(gamemode_id)
        

    def __str__(self):
        return f"Result: {self.result_sec}s, Penalty: {self.penalty_sec}s"
    

    def __gamemode_by_id(gamemode_id):
        RunResult.__load_id_data()
        return RunResult.gamemode_lookup.get(gamemode_id, "N/A")
    

    def __load_id_data():
        if not RunResult.gamemode_lookup:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            ids_file = os.path.join(current_dir, "../", "ids.json")
            ids_data = json.load(open(ids_file))
            
            gamemodes = ids_data["game_mode"]
            RunResult.gamemode_lookup = {gamemode["id"]: gamemode["name"] for gamemode in gamemodes}