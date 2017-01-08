import os
import json
import time
from nimmo_library import *
import sys


def load_class_list():
    if os.path.isfile("class_lists.json"):
        return json.load(open("class_lists.json"))
    else:
        create_classes = yes_no_confirmation("No classes are defined, would you like to create some? (Y/N)")

        if create_classes:
            return build_class_list()
        else:
            return {}


def build_class_list():
    print("You will now be asked to enter a series of class titles.\nWhen complete enter a blank class title.")
    class_title = input("Please enter a class title: ")
    class_list = {}
    while class_title != "":
        class_list[class_title] = []
        class_title = input("Please enter a class title: ")

    print("You created", len(list(class_list.keys())), "classes.")
    confirmation = yes_no_confirmation("Is this correct? (Y/N)")
    if confirmation:
        json.dump(class_list, open("class_lists.json", "w"))
        return class_list
    else:
        print("Restarting class list creation process.")
        return build_class_list()


def manage_pupils(class_list):
    try:
        server_settings = json.load(open("server_settings.json"))
        log_dir = server_settings["log_dir"]

    except FileNotFoundError:
        print("Server settings file not found, assuming default settings")
        sys.exit()

    try:
        unknown_pupils = json.load(open("unknown_pupils.txt"))
        for day in list(unknown_pupils.keys()):
            current_day = unknown_pupils[day]
            day_complete = True
            for lesson in range(len(current_day)):

                if len(current_day[lesson]) > 0:
                    print("Day:", day, "\tLesson:", lesson, "has", len(current_day[lesson]), "pupils.")
                    class_title = input("Please enter the title of this class: ")
                    if class_title not in list(class_list.keys()):
                        add_class_prompt = "Would you like to add " + class_title + " to your list of classes? (Y/N): "
                        add_class = yes_no_confirmation(add_class_prompt)
                        if add_class:
                            class_list[class_title] = []
                    else:
                        add_class = True

                    if add_class:
                        for pupil in current_day[lesson]:
                            if pupil not in class_list[class_title]:
                                class_list[class_title].append(pupil)
                                migrate_log_file(log_dir, class_title, pupil)
                        unknown_pupils[day][lesson] = []
                    else:
                        day_complete = False
                        print("Not processing this class, rerun to try again.")
            if day_complete:
                print("Processed all classes for today.")
                unknown_pupils.pop(day, None)
        print(class_list)
        json.dump(class_list, open("class_lists.json", "w"))
        json.dump(unknown_pupils, open("unknown_pupils.txt", "w"))
    except FileNotFoundError:
        print("Unknown pupils file not found, no need to update class list")


def new_unknown(user_name, lesson_times):
    day, lesson = find_lesson(lesson_times)
    if os.path.isfile("unknown_pupils.txt"):
        unknown_pupils = json.load(open("unknown_pupils.txt"))
    else:
        unknown_pupils = {day: [[], [], [], [], [], []]}
    try:
        if user_name not in unknown_pupils[day][lesson]:
            unknown_pupils[day][lesson].append(user_name)
    except KeyError:
        unknown_pupils[day] = [[], [], [], [], [], []]
        unknown_pupils[day][lesson].append(user_name)
    json.dump(unknown_pupils, open("unknown_pupils.txt", "w"))


def get_lesson_list():
    if os.path.isfile("lesson_times.json"):
        return json.load(open("lesson_times.json"))
    else:
        lesson_count = get_int("How many lessons are there in a day? ", 0)
        lesson_times = []
        for times in range(lesson_count):
            prompt = "What time does lesson " + str(times + 1) + " start? "
            start_time = input(prompt)
            prompt = "What time does lesson " + str(times + 1) + " end? "
            end_time = input(prompt)
            start_mins = 60 * int(start_time[0:2]) + int(start_time[-2:])
            end_mins = 60 * int(end_time[0:2]) + int(end_time[-2:])
            lesson_times.append([start_mins, end_mins])

        json.dump(lesson_times, open("lesson_times.json", "w"))
        return lesson_times


def find_lesson(lesson_times):
    day = time.strftime("%A %d/%m/%Y")
    hours = int(time.strftime("%H"))
    minutes = int(time.strftime("%M"))
    current_time = hours * 60 + minutes
    for lesson in range(len(lesson_times)):
        if lesson_times[lesson][0] <= current_time <= lesson_times[lesson][1]:
            return day, lesson + 1
    return day, 0


def find_class(file_name, class_list, lesson_times):
    user_name = file_name.split(" ")[0].lower()
    if class_list != {}:
        for item in list(class_list.keys()):
            if user_name in class_list[item]:
                return item

        new_unknown(user_name, lesson_times)
        return "unknown"
    else:
        new_unknown(user_name, lesson_times)
        return "unknown"


def get_file_path(log_directory, file_name, class_list, lesson_times):

    class_directory = find_class(file_name, class_list, lesson_times)
    file_path = os.path.join(log_directory, class_directory, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path


def migrate_log_file(log_dir, class_title, user_name):
    import shutil
    try:
        files = os.listdir(log_dir)
        for file in files:
            if file.startswith(user_name):
                old_path = os.path.join(log_dir, "unknown", file)
                os.makedirs(os.path.join(log_dir, class_title), exist_ok=True)
                new_path = os.path.join(log_dir, class_title, file)
                print("Copying", old_path, "to", new_path, ".")
                shutil.copyfile(old_path, new_path)
                os.remove(old_path)

    except FileNotFoundError:
        print("User's old file doesn't exist, skipping copy.")

