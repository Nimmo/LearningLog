from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import getpass
import time
import json
import os.path

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
learning_log = []


class LearningLog(FloatLayout):
    learning_intention = ObjectProperty()
    success_yes = ObjectProperty()
    success_part = ObjectProperty()
    success_no = ObjectProperty()
    lesson_success = ObjectProperty()
    next_steps = ObjectProperty()
    #comments = ObjectProperty()

    def add_record(self):
        learning_record = {}
        learning_record["date"] = time.strftime("%d/%m/%y")
        learning_record["learning_intention"] = self.learning_intention.text
        if self.success_yes.state == "down":
            learning_record["success"] = "Y"
        elif self.success_part.state == "down":
            learning_record["success"] = "P"
        else:
            learning_record["success"] = "N"
        learning_record["lesson_achievement"] = self.lesson_success.text
        learning_record["next steps"] = self.next_steps.text
        #learning_record["comments"] = self.comments.text

        learning_log.append(learning_record)

        json.dump(learning_log, open(file_path, "w"))

    def show_learning_log(self):
        self.clear_widgets()
        self.add_widget(LearningLog())


class LearningLogApp(App):
    def build(self):
        return LearningLog()


def get_session():
    month = int(time.strftime("%m"))
    year = int(time.strftime("%y"))
    if month > 8:
        session = str(year) + "-" + str(year + 1)
    else:
        session = str(year - 1) + "-" + str(year)
    return session

class TableHeader(Label):
    pass


class LearningRecord(Label):
    pass


class MyGrid(GridLayout):

    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.fetch_data_from_database()
        self.display_scores()

    def fetch_data_from_database(self):
        self.data = learning_log

    def display_scores(self):
        self.clear_widgets()

        row = self.create_header()
        for item in row:
            self.add_widget(item)

        for i in range(len(self.data)):
            row = self.add_record_to_table(i)
            for item in row:
                self.add_widget(item)

    def create_header(self):
        first_column = TableHeader(text="Date")
        second_column = TableHeader(text="Learning Intention")
        third_column = TableHeader(text="Successful?")
        fourth_column = TableHeader(text="Achievement in Lesson")
        fifth_column = TableHeader(text="Next Steps")
        return [first_column, second_column, third_column, fourth_column, fifth_column]

    def add_record_to_table(self, i):
        first_column = LearningRecord(text=self.data[i]['date'])
        second_column = LearningRecord(text=self.data[i]['learning_intention'])
        third_column = LearningRecord(text=self.data[i]['success'])
        fourth_column = LearningRecord(text=self.data[i]['lesson_achievement'])
        fifth_column = LearningRecord(text=self.data[i]['next steps'])
        return [first_column, second_column, third_column, fourth_column, fifth_column]

if __name__ == '__main__':
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

    LearningLogApp().run()

