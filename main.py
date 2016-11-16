from tkinter import *
from tkinter import ttk
import getpass
import time
import json
import os.path
import log_viewer

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

file_path = ""
learning_log = {}

def display_entry_screen(root):
    #Root Frame
    frame_main.grid(column=0, row=0, sticky=(N, W, E, S))
    frame_main.rowconfigure(0, weight=1)

    #LI Frame
    frame_learning_intention.grid(column=0, row=0, sticky="NWE")
    label_learning_intention.grid(column=0, row=0, sticky="W")
    entry_learning_intention.grid(column=0, row=1, sticky="WE")

    #Lesson Success Frame
    frame_lesson_success.grid(column=0, row=1, sticky = "WE")
    label_lesson_success.grid(column=0, row=0)
    radio_yes.grid(column = 0, row = 1, sticky="WE")
    radio_partially.grid(column = 1, row = 1, sticky="WE")
    radio_no.grid(column = 2, row = 1, sticky="WE")

    #Lesson Achievement Frame
    frame_lesson_achievement.grid(column = 0, row = 2, sticky="WE")
    label_lesson_achievement.grid(column=0, row=0, sticky="WE")
    entry_lesson_achievement.grid(column=0, row=1, sticky="WE")

    #Next Steps Frame
    frame_next_steps.grid(column = 0, row = 3, sticky="WE")
    label_next_steps.grid(column=0, row=0, sticky="WE")
    entry_next_steps.grid(column=0, row=1, sticky="WE")


def add_entry():
    date = time.strftime("%d/%m/%y")

    lesson_details = []
    lesson_details.append(entry_learning_intention.get())
    lesson_details.append(success.get())
    lesson_details.append(lesson_achievement.get())
    lesson_details.append(next_steps.get())


    learning_log[date] = lesson_details

    json.dump(learning_log, open(file_path, "w"))

def view_log():
    log_viewer.display_log(learning_log)

def get_session():
    month = int(time.strftime("%m"))
    year = int(time.strftime("%y"))
    if month > 8:
        session = str(year) + "-" + str(year + 1)
    else:
        session = str(year - 1) + "-" + str(year)
    return session

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
                                variable = success)

    radio_partially = ttk.Radiobutton(frame_lesson_success,
                                      text="Partially",
                                      value="P",
                                      variable = success)

    radio_no = ttk.Radiobutton(frame_lesson_success,
                               text="No",
                               value="N",
                               variable = success)


    # Lesson Achievement Block
    frame_lesson_achievement = ttk.Frame(frame_main)
    label_lesson_achievement = ttk.Label(frame_lesson_achievement,
                                         text="What was your greatest achievement during this lesson?")

    entry_lesson_achievement = ttk.Entry(frame_lesson_achievement,
                                         textvariable=lesson_achievement,
                                         width = 97)


    # Next Steps Block
    frame_next_steps = ttk.Frame(frame_main)
    label_next_steps = ttk.Label(frame_next_steps,
                                 text="What are your next steps?")

    entry_next_steps = ttk.Entry(frame_next_steps,
                                 textvariable=next_steps,
                                 width = 97)


    # Button controls
    frame_buttons = ttk.Frame(frame_main)
    frame_buttons.grid(column = 0,
                       row = 4,
                       sticky="WE")

    button_add_entry = ttk.Button(frame_buttons,
                                  text = "Add Entry",
                                  command = add_entry)

    button_add_entry.grid(column = 0,
                          row = 0)

    button_view_log = ttk.Button(frame_buttons,
                                 text = "View Log",
                                 command = view_log)

    button_view_log.grid(column = 1,
                         row = 0)


    for child in frame_main.winfo_children():
        child.grid_configure(padx=5, pady=10)
    
    username = getpass.getuser()
    session = get_session()
    home_dir = os.path.expanduser("~")
    file_name = username + " " + session + " learning log.json"
    file_directory = "Learning Log"
    home_dir_parts = home_dir.split('\\')
    file_path = os.path.join(home_dir, file_directory, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    if os.path.isfile(file_path):
        learning_log = json.load(open(file_path))

    display_entry_screen(root)
    root.mainloop()
