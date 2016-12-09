import socket
import json
import os
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 5000

def load_class_lists():
    if os.path.isfile("class_lists.json"):
        return json.load(open("class_lists.json"))            
    else:
        return {}

def find_class(file_name, class_list):
    user_name = file_name.split(" ")[0].lower()
    if class_list != {}:
        for item in list(class_list.keys()):
            if user_name in class_list[item]:
                return item
        return "unknown"
    else:
        return "unknown"

def get_file_path(file_name, class_list):
    if os.path.isfile("client settings.txt"):
        client_settings_file = open("client settings.txt", "r")
        home_dir = client_settings_file.readline()
    else:
        home_dir = os.path.expanduser("~")
    file_directory = "Learning Log - Pupils"
    class_directory = find_class(file_name, class_list)
    file_path = os.path.join(home_dir, file_directory, class_directory, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path

def read_file(file_name):
    file_path = get_file_path(file_name)
    if os.path.isfile(file_path):
        return json.load(open(file_path))
    else:
        return {"file_name": ""}


def request_dates(sender, required_dates):
    pass


def check_dates(received_data):
    # Prepare a list of dates we're going to request.
    # Start by assuming we want all of them

    requested_dates = list(received_data.keys())
    file_name = received_data["file_name"]
    requested_dates.remove("file_name")

    # Get the list of dates we've already received
    sender_log = read_file(file_name)
    synced_dates = list(sender_log.keys())
    synced_dates.remove("file_name")

    # Trying to trap the case where we're syncing for the first time
    if len(synced_dates) > 0:
        for entry in synced_dates:
            # If I've already got an entry for this date drop it from our list of requests
            if entry in requested_dates:
                requested_dates.remove(entry)
    
    return requested_dates


def store_log(received_data, class_list):
    file_name = received_data["file_name"]
    file_path = get_file_path(file_name, class_list)
    if os.path.isfile(file_path):
        existing_log = json.load(open(file_path))
    else:
        existing_log = {}
    existing_log.update(received_data)
    json.dump(existing_log, open(file_path, 'w'))
    print("Wrote", str(len(list(received_data.keys()))-1), "log entries to:", file_path )


def get_time():
    hours = int(time.strftime("%H"))
    minutes = int(time.strftime("%M"))
    seconds = int(time.strftime("%S"))
    return "%d:%d:%d" %(hours, minutes, seconds)


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

    sock.bind((UDP_IP, UDP_PORT))
    class_list = load_class_lists()
    print("Loaded", len(list(class_list.keys())), "classes.")
    while True:

        
        
        data, addr = sock.recvfrom(2048)  # buffer size is 1024 bytes
        received_data = eval(data.decode())
        current_time = get_time()
        #print("Received a log from", received_data["file_name"], "at", current_time)
        store_log(received_data, class_list)
        # needed_dates = check_dates(received_data)

        #sock.sendto("ack".encode(), addr)
