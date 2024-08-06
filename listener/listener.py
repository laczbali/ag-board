from threading import Thread
import socket
import struct

from listener.models.run_result import RunResult
from listener.models.track import Track
from listener.models.vehicle import Vehicle
from listener.storage_handler import StorageHandler


class Listener:

    def __init__(self):
        self.__storage_handler = StorageHandler()


    def __listen(self, port, processor):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(("127.0.0.1", port))
        print(f"Listener started on port {port}")
        while True:
            data, addr = server.recvfrom(1024)
            processor(data)

    def __process_end(self, raw_data):
        bool_shakedown = struct.unpack("?", raw_data[0:1])[0]
        uint8_gamemode = struct.unpack("B", raw_data[1:2])[0]
        uint16_vehicle = struct.unpack("H", raw_data[2:4])[0]
        uint16_vehicle_class = struct.unpack("H", raw_data[4:6])[0]
        uint16_vehicle_manufacturer = struct.unpack("H", raw_data[6:8])[0]
        uint16_location = struct.unpack("H", raw_data[8:10])[0]
        uint16_route = struct.unpack("H", raw_data[10:12])[0]
        float32_result_time = struct.unpack("f", raw_data[12:16])[0]
        float32_result_penalty = struct.unpack("f", raw_data[16:20])[0]
        uint8_result_status = struct.unpack("B", raw_data[20:21])[0]
        
        if bool_shakedown:
            print(f"Run was a shakedown (ignored)")
            return

        if uint8_result_status != 1:
            print(f"Run aborted")
            return
        
        track = Track(uint16_location, uint16_route)
        vehicle = Vehicle(uint16_vehicle_class, uint16_vehicle_manufacturer, uint16_vehicle)
        run_results = RunResult(float32_result_time, float32_result_penalty, uint8_gamemode)
        self.__storage_handler.store_run(run_results, vehicle, track)
        print(f"Run saved {run_results}, {track}, {vehicle}")


    def start(self):
        Thread(target=Listener.__listen, daemon=True, args=(self, 20778, self.__process_end)).start()
