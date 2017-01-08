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


def display_log(learning_log):

    root = Tk()
    root.title("Learning Log Viewer")
    root.geometry("830x600")
    root.resizable(height=False, width=False)
    tree = ttk.Treeview(root, height=560)

    tree["columns"]=("learning_intention", "success", "lesson_achievement", "next steps")
    tree.column("learning_intention", width=200)
    tree.column("success", width=20)
    tree.column("lesson_achievement", width=200)
    tree.column("next steps", width=200)
    tree.heading("learning_intention", text="Learning Intention")
    tree.heading("success", text="Succsessful lesson?")
    tree.heading("lesson_achievement", text="Lesson Achievement")
    tree.heading("next steps", text="Next Steps")
    dates = list(learning_log.keys())
    dates.remove("file_name")
    dates.sort()
    dates.reverse()
    for each in dates:
        tree.insert("", END, text=each, values=(learning_log[each][0],learning_log[each][1], learning_log[each][2], learning_log[each][3]))

    tree.grid(column=0, row=0, sticky="NSEW")

    root.mainloop()
