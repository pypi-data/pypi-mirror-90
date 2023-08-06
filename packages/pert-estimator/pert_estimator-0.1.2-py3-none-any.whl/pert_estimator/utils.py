def calculate_expected_duration(optimistic, nominal, pessimistic):
    """ Calculate the expected duration of a task. """
    return round((optimistic + (4 * nominal) + pessimistic) / 6, 1)

def calculate_standard_deviation(pessimistic, optimistic):
    """ Calculate the standard deviation of a task. """
    return round((pessimistic - optimistic) / 6, 1)

def get_user_input_number(input_string):
    """ Ensure user input is of type Integer. """
    valid_user_input = False
    while not valid_user_input:
        user_input = input(input_string)
        try:
            user_input = float(user_input)
            valid_user_input = True
        except ValueError:
            print('ERROR: please ensure input is an integer.')

    return get_whole_number_or_float(user_input)

def get_user_input_boolean(input_string):
    """ Ensure user input is of type Boolean. """
    valid_user_input = False
    while not valid_user_input:
        user_input = input(input_string)
        if user_input == 'Y' or user_input == 'y':
            user_input = True
            valid_user_input = True
        elif user_input == 'N' or user_input == 'n':
            user_input = False
            valid_user_input = True
        else:
            print("ERROR: please enter 'Y' or 'N'.")

    return user_input

def get_whole_number_or_float(number):
    """ Get whole number of input or keep as float. """
    if number % 1 == 0:
        return int(number)

    return number