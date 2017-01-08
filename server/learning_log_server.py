import socket
import json
import os
import time
import server.class_management as class_manager
from lib.nimmo_library import yes_no_confirmation


def init():
    if os.path.isfile("server_settings.json"):
        server_settings = json.load(open("server_settings.json"))
        log_dir = server_settings["log_dir"]
        ip = server_settings["ip"]
        port = server_settings["port"]
    else:
        print("Settings file not found, assuming this is the first run.")
        ip = "0.0.0.0"
        port = 5005
        home_dir = os.path.expanduser("~")
        file_directory = "Learning Log - Pupils"
        log_dir = os.path.join(home_dir, file_directory)
        print("By default the pupil's learning logs will be stored to: ", log_dir)
        override_defaults = yes_no_confirmation("Would you like to choose a different location?")
        if override_defaults:
            created = False
            while not created:
                log_dir = input("Please enter the path to where you'd like to store your pupil's logs: ")
                if not os.path.isdir(log_dir):
                    try:
                        os.makedirs(log_dir, exist_ok=True)
                        created = True
                    except:
                        print("there was a problem creating that path, please provide the path again")
        server_settings = {"ip": ip, "port": port, "log_dir": log_dir}
        json.dump(server_settings, open("server_settings.json", "w"))
    return ip, port, log_dir


def store_log(received_log):
    file_path = class_manager.get_file_path(log_directory, received_log["file_name"], class_list)
    if os.path.isfile(file_path):
        existing_log = json.load(open(file_path))
    else:
        existing_log = {}
    existing_log.update(received_log)
    json.dump(existing_log, open(file_path, 'w'))
    print("Wrote", str(len(list(received_log.keys()))-1), "log entries to:", file_path)


def get_time():
    hours = int(time.strftime("%H"))
    minutes = int(time.strftime("%M"))
    seconds = int(time.strftime("%S"))
    return "%d:%d:%d" % (hours, minutes, seconds)


if __name__ == '__main__':
    UDP_IP, UDP_PORT, log_directory = init()
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP

    sock.bind((UDP_IP, UDP_PORT))
    class_list = class_manager.load_class_list()
    print("Loaded", len(list(class_list.keys())), "classes.")

    while True:
        data, addr = sock.recvfrom(2048)  # buffer size is 1024 bytes
        received_data = eval(data.decode())

        store_log(received_data)
