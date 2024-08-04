from threading import Thread
import socket
import struct


def listener(port, processor):
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("127.0.0.1", port))
    while True:
        data, addr = server.recvfrom(1024)
        processor(data)


def start_processor(raw_data):
    bool_shakedown = struct.unpack("?", raw_data[0:1])[0]
    uint8_gamemode = struct.unpack("B", raw_data[1:2])[0]
    uint16_vehicle = struct.unpack("H", raw_data[2:4])[0]
    uint16_vehicle_class = struct.unpack("H", raw_data[4:6])[0]
    uint16_vehicle_manufacturer = struct.unpack("H", raw_data[6:8])[0]
    uint16_location = struct.unpack("H", raw_data[8:10])[0]
    uint16_route = struct.unpack("H", raw_data[10:12])[0]
    print(f"location: {uint16_location}, route: {uint16_route}, vehicle: {uint16_vehicle}")


def update_processor(raw_data):
    float32_current_time = struct.unpack("f", raw_data[0:4])[0]
    print(f"time: {float32_current_time}")


def end_processor(raw_data):
    result_lookup = [
        "not_finished",
        "finished",
        "timed_out_stage",
        "terminally_damaged",
        "retired",
        "disqualified",
        "unknown"
    ]

    float32_result_time = struct.unpack("f", raw_data[0:4])[0]
    float32_result_penalty = struct.unpack("f", raw_data[4:8])[0]
    uint8_result_status = struct.unpack("B", raw_data[8:9])[0]
    print(f"status: {result_lookup[uint8_result_status]}, result: {float32_result_time}, penalty: {float32_result_penalty}")


thread_start_listener = Thread(target=listener, daemon=True, args=(20776, start_processor))
thread_update_listener = Thread(target=listener, daemon=True, args=(20777, update_processor))
thread_end_listener = Thread(target=listener, daemon=True, args=(20778, end_processor))
thread_start_listener.start()
thread_update_listener.start()
thread_end_listener.start()

while True:
    pass