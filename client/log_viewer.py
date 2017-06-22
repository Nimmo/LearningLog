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
import datetime


def display_log(learning_log):

    root = Tk()
    root.title("Learning Log Viewer")
    root.geometry("950x400")
    root.resizable(height=False, width=False)
    tree = ttk.Treeview(root)

    tree["columns"]=("learning_intention", "success", "lesson_achievement", "next steps")
    tree.column("learning_intention", width=250)
    tree.column("success", width=40)
    tree.column("lesson_achievement", width=300)
    tree.column("next steps", width=300)
    tree.heading("learning_intention", text="Learning Intention")
    tree.heading("success", text="Success?")
    tree.heading("lesson_achievement", text="Lesson Achievement")
    tree.heading("next steps", text="Next Steps")

    v_scroll = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
    h_scroll = ttk.Scrollbar(root, orient=HORIZONTAL, command=tree.xview)

    tree["yscrollcommand"] = v_scroll.set
    tree["xscrollcommand"] = h_scroll.set

    tree.grid(column=0, row=0, sticky="N,W,E,S")
    v_scroll.grid(column=1, row=0, sticky="SN")
    h_scroll.grid(column=0, row=1, sticky="EW")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    dates = list(learning_log.keys())
    dates.remove("file_name")
    dates = sorted(dates, key=lambda x: datetime.datetime.strptime(x, "%d/%m/%y"))
    dates.reverse()
    for each in dates:
        if learning_log[each][1] == "Y":
            success = "Yes"
        elif learning_log[each][1] == "P":
            success = "Partially"
        else:
            success = "No"

        tree.insert("", END, text=each, values=(learning_log[each][0],success, learning_log[each][2], learning_log[each][3]))

    root.mainloop()
