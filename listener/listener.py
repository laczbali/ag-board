from threading import Thread
import socket
import struct

from listener.models.run_result import RunResult
from listener.models.track import Track
from listener.models.vehicle import Vehicle
from listener.storage_handler import StorageHandler


class Listener:

    def __init__(self):
        self.__track = None
        self.__vehicle = None
        self.__game_mode = None
        self.__run_results = None
        self.__storage_handler = StorageHandler()


    def __listen(self, port, processor):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(("127.0.0.1", port))
        while True:
            data, addr = server.recvfrom(1024)
            processor(data)


    def __process_start(self, raw_data):
        bool_shakedown = struct.unpack("?", raw_data[0:1])[0]
        uint8_gamemode = struct.unpack("B", raw_data[1:2])[0]
        uint16_vehicle = struct.unpack("H", raw_data[2:4])[0]
        uint16_vehicle_class = struct.unpack("H", raw_data[4:6])[0]
        uint16_vehicle_manufacturer = struct.unpack("H", raw_data[6:8])[0]
        uint16_location = struct.unpack("H", raw_data[8:10])[0]
        uint16_route = struct.unpack("H", raw_data[10:12])[0]

        if bool_shakedown:
            return

        self.__track = Track(uint16_location, uint16_route)
        self.__vehicle = Vehicle(uint16_vehicle_class, uint16_vehicle_manufacturer, uint16_vehicle)
        self.__game_mode = uint8_gamemode
        print(f"Run starting: {self.__track} - {self.__vehicle}")


    def __process_update(self, raw_data):
        float32_current_time = struct.unpack("f", raw_data[0:4])[0]


    def __process_end(self, raw_data):
        float32_result_time = struct.unpack("f", raw_data[0:4])[0]
        float32_result_penalty = struct.unpack("f", raw_data[4:8])[0]
        uint8_result_status = struct.unpack("B", raw_data[8:9])[0]
        
        if uint8_result_status != 1:
            print(f"Run aborted")
            return
        
        self.__run_results = RunResult(float32_result_time, float32_result_penalty, self.__game_mode)
        self.__storage_handler.store_run(self.__run_results, self.__vehicle, self.__track)
        print(f"Run saved {self.__run_results}")


    def start(self):
        Thread(target=Listener.__listen, daemon=True, args=(self, 20776, self.__process_start)).start()
        Thread(target=Listener.__listen, daemon=True, args=(self, 20777, self.__process_update)).start()
        Thread(target=Listener.__listen, daemon=True, args=(self, 20778, self.__process_end)).start()