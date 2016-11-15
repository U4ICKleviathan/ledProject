import json


SIM_TAG = "GPIO SIMULATION:"


def print_simulation_message(message, **kwargs):
    print SIM_TAG, message
    for key, val in kwargs.iteritems():
        print SIM_TAG, key, "=", val


def change_brightness(brightness):
    action_variables = {"brightness": brightness}
    print_simulation_message("Changing Brightness", **action_variables)


def change_color(**kwargs):
    print_simulation_message("Changing Color", **kwargs)






