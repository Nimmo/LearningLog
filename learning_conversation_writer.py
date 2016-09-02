import getpass
import time
import json
import os.path


def get_learning_intention():
    intention = input("Please enter today's learning intention: ")
    return intention


def get_li_achieved():
    print("Did you achieve the learning intention today? (Yes, Partially, No)")
    li_achieved = input()
    while li_achieved not in ["Y", "N", "P"]:
        li_achieved = input("Please enter Y for yes, P for partially or N for no: ")
    return li_achieved


def get_lesson_success():
    success = input("Please write what your greatest success during this lesson was: ")
    return success


def get_next_steps():
    next_steps = input("Please enter your next steps: ")
    return next_steps


def get_lesson_thoughts():
    lesson_thoughts = input("Please enter any feedback that you'd like to give to your teacher from this lesson: ")
    return lesson_thoughts

if __name__ == '__main__':
    print("Welcome to the Learning Conversation Writer")
    learning_conversation = {}
    # Display prompt to enter LI

    if os.path.isfile("learning_conversation.conv"):
        learning_log = json.load(open("learning_conversation.conv"))
    else:
        learning_log = []

    print("You have written " + str(len(learning_log)) + " entries for your learning log already.")
    learning_conversation["learning_intention"] = get_learning_intention()

    # Ask user whether they achieved the LI
    learning_conversation["li_achieved"] = get_li_achieved()

    # Ask user what their greatest success was
    learning_conversation["lesson_success"] = get_lesson_success()

    # Ask user for next steps
    learning_conversation["next_steps"] = get_next_steps()

    # Ask user for thoughts on the lesson as a whole
    learning_conversation["lesson_thoughts"] = get_lesson_thoughts()

    #Gather some extra info we need to complete this learning conversation
    username = getpass.getuser()
    learning_conversation["date"] = time.strftime("%d/%m/%y")

    # Store statement in file
    # learning_conversation_file = open("learning conversation.csv", "ra")

    # learning_conversation_file.writeline()

    learning_log.append(learning_conversation)
    json.dump(learning_log, open("learning_conversation.conv", "w"))