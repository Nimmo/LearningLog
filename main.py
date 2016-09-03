from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import getpass
import time
import json
import os.path

log_file = ""
learning_log = []

class LearningConversationPupil(BoxLayout):

    learning_intention = ObjectProperty()
    success_yes = ObjectProperty()
    success_part = ObjectProperty()
    success_no = ObjectProperty()
    lesson_success = ObjectProperty()
    next_steps = ObjectProperty()
    comments = ObjectProperty()

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
        learning_record["comments"] = self.comments.text

        learning_log.append(learning_record)

        json.dump(learning_log, open(log_file, "w"))


class LearningConversations(App):
    pass


def get_session():
    month = int(time.strftime("%m"))
    year = int(time.strftime("%y"))
    if month > 8:
        session = str(year) + "-" + str(year + 1)
    else:
        session = str(year - 1) + "-" + str(year)
    return session

if __name__ == '__main__':


    username = getpass.getuser()
    session = get_session()
    log_file = username + " " + session + " learning log.json"

    if os.path.isfile(log_file):
        learning_log = json.load(open(log_file))

    LearningConversations().run()