import socket
import json
import os
import getpass

UDP_IP = "0.0.0.0"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind((UDP_IP, UDP_PORT))


def read_file(file_name):
    home_dir = os.path.expanduser("~")
    file_directory = "Learning Log"
    file_path = os.path.join(home_dir, file_directory, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if os.path.isfile(file_path):
        return json.load(open(file_path))
    else:
        return {}


def request_dates(sender, required_data):
    pass


def check_dates(sender, received_data):
    dates = list(received_data.keys())
    file_name = received_data["file_name"]
    dates.remove("file_name")
    sender_log = read_file(file_name)
    received_dates = list(sender_log.keys())
    


if __name__ == '__main__':

    while True:

        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        received_data = json.load(data.decode())
        print("received data:", received_data)
        print("Message arrived from:", addr)
        check_dates(addr, received_data)

        sock.sendto("ack".encode(), addr)