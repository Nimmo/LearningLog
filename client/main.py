# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tkinter import *
from tkinter import ttk
import getpass
import time
import json
import os.path
import log_viewer
import socket

file_path = ""
learning_log = {}


def display_entry_screen(root):
    # Root Frame
    frame_main.grid(column=0, row=0, sticky=(N, W, E, S))
    frame_main.rowconfigure(0, weight=1)

    # LI Frame
    frame_learning_intention.grid(column=0, row=0, sticky="NWE")
    label_learning_intention.grid(column=0, row=0, sticky="W")
    entry_learning_intention.grid(column=0, row=1, sticky="WE")

    # Lesson Success Frame
    frame_lesson_success.grid(column=0, row=1, sticky = "WE")
    label_lesson_success.grid(column=0, row=0)
    radio_yes.grid(column=0, row=1, sticky="WE")
    radio_partially.grid(column=1, row=1, sticky="WE")
    radio_no.grid(column=2, row=1, sticky="WE")

    # Lesson Achievement Frame
    frame_lesson_achievement.grid(column=0, row=2, sticky="WE")
    label_lesson_achievement.grid(column=0, row=0, sticky="WE")
    entry_lesson_achievement.grid(column=0, row=1, sticky="WE")

    # Next Steps Frame
    frame_next_steps.grid(column=0, row=3, sticky="WE")
    label_next_steps.grid(column=0, row=0, sticky="WE")
    entry_next_steps.grid(column=0, row=1, sticky="WE")


def details_to_server(log):
    if os.path.isfile("server_settings.txt"):
        settings_file = open("server_settings.txt", "r")
        settings_data = settings_file.read()
        settings = settings_data.split(",")
        UDP_IP = settings[0]
        UDP_PORT = int(settings[1])
    else:
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005
    to_send = json.dumps(log)
    print("Sending our log to the server")
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.settimeout(2.0)
    sock.sendto(to_send.encode(), (UDP_IP, UDP_PORT))
    print("Send attempt complete")


def add_entry():
    date = time.strftime("%d/%m/%y")

    lesson_details = [entry_learning_intention.get(), success.get(), lesson_achievement.get(), next_steps.get()]

    learning_log[date] = lesson_details

    json.dump(learning_log, open(file_path, "w"))
    print("Wrote learning log to", file_path)
    details_to_server(learning_log)


def view_log():
    log_viewer.display_log(learning_log)


def get_session():
    month = int(time.strftime("%m"))
    year = int(time.strftime("%y"))
    if month > 8:
        return str(year) + "-" + str(year + 1)
    else:
        return str(year - 1) + "-" + str(year)


def get_file_path(file_name):
    file_directory = "Learning Log"
    migration_check = False
    if os.path.isfile("client_settings.txt"):
        try:
            client_settings_file = open("client_settings.txt", "r")
            home_dir = client_settings_file.readline()
            migration_check = True
        except Exception as ex:
            home_dir = os.path.expanduser("~")
            print("Threw an exception:", ex)

    else:
            home_dir = os.path.expanduser("~")
    # print(home_dir)

    file_path = os.path.join(home_dir, file_directory, file_name)
    try:
        if migration_check:
            old_home = os.path.expanduser("~")
            if old_home[0] != home_dir[0]:
                print("Initating migration check")
                old_path = os.path.join(old_home, file_directory, file_name)
                if os.path.isfile(old_path):
                    print("Migrating from old log file location")
                    old_log = json.load(old_path)
                    new_log = json.load(file_path)
                    print("Adding", len(list(old_log.keys()))-1, "to list of", len(list(new_log.keys()))-1, "entries in new file.")
                    new_log.update(old_log)
                    json.dump(new_log, open(file_path, "w"))
                    print("Deleting old file:", old_log)
                    os.remove(old_log)
    except Exception as ex:
        print("Encountered an exception: " + ex)

    return file_path

if __name__ == '__main__':

    # Generate the UI
    root = Tk()
    root.title("Learning Log - Entry Screen")
    root.geometry("800x300")
    root.resizable(height=False, width=False)
    learning_intention = StringVar()
    success = StringVar()
    lesson_achievement = StringVar()
    next_steps = StringVar()

    xpad = 3
    ypad = 12
    frame_main = ttk.Frame(root, padding="%d %d %d %d" %(xpad, xpad, ypad, ypad))
    frame_main.columnconfigure(0, weight=1)
    frame_main.rowconfigure(0, weight=1)

    # Learning intention block
    frame_learning_intention = ttk.Frame(frame_main,
                                         width=root.winfo_width())
    frame_learning_intention.columnconfigure(0,weight=1)
    label_learning_intention = ttk.Label(frame_learning_intention,
                                         text="Learning intention:")

    entry_learning_intention = ttk.Entry(frame_learning_intention, 
                                         width=97, 
                                         textvariable=learning_intention)

    # Lesson Success Block
    frame_lesson_success = ttk.Frame(frame_main)
    label_lesson_success = ttk.Label(frame_lesson_success,
                                     text="Did you achieve the learning intention?")

    radio_yes = ttk.Radiobutton(frame_lesson_success,
                                text="Yes",
                                value="Y",
                                variable=success)

    radio_partially = ttk.Radiobutton(frame_lesson_success,
                                      text="Partially",
                                      value="P",
                                      variable=success)

    radio_no = ttk.Radiobutton(frame_lesson_success,
                               text="No",
                               value="N",
                               variable=success)

    # Lesson Achievement Block
    frame_lesson_achievement = ttk.Frame(frame_main)
    label_lesson_achievement = ttk.Label(frame_lesson_achievement,
                                         text="What was your greatest achievement during this lesson?")

    entry_lesson_achievement = ttk.Entry(frame_lesson_achievement,
                                         textvariable=lesson_achievement,
                                         width=97)

    # Next Steps Block
    frame_next_steps = ttk.Frame(frame_main)
    label_next_steps = ttk.Label(frame_next_steps,
                                 text="What are your next steps?")

    entry_next_steps = ttk.Entry(frame_next_steps,
                                 textvariable=next_steps,
                                 width=97)

    # Button controls
    frame_buttons = ttk.Frame(frame_main)
    frame_buttons.grid(column=0,
                       row=4,
                       sticky="WE")

    button_add_entry = ttk.Button(frame_buttons,
                                  text="Add Entry",
                                  command=add_entry)

    button_add_entry.grid(column=0,
                          row=0)

    button_view_log = ttk.Button(frame_buttons,
                                 text="View Log",
                                 command=view_log)

    button_view_log.grid(column=1,
                         row=0)

    for child in frame_main.winfo_children():
        child.grid_configure(padx=5, pady=10)
    
    username = getpass.getuser()
    session = get_session()
    file_name = username + " " + session + " learning log.json"

    file_path = get_file_path(file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        # Attempt to open an existing learning log
        learning_log = json.load(open(file_path))
        print("Loaded learning log from: " + file_path)
    except FileNotFoundError:
        print("No existing learning log found, preparing to create a new one.")
        # If there is no existing learning log, prepare for it to be created
        learning_log["file_name"] = file_name

    display_entry_screen(root)
    root.mainloop()
