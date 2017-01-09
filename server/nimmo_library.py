def yes_no_confirmation(prompt):
    response = input(prompt).lower()
    while response != "y" and response != "n":
        print("Please answer Y for yes or N for no.")
        response = input(prompt).lower()
    return response == "y"


def get_int(prompt, min, max):
    user_input = int(input(prompt))
    while not min <= user_input <= max:
        user_input = int(input(prompt))

    return user_input

def get_int(prompt, min):
    user_input = int(input(prompt))
    while not min <= user_input:
        user_input = int(input(prompt))

    return user_input
