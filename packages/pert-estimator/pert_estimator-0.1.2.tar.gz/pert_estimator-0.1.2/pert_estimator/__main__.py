import sys

from prettytable import PrettyTable

from pert_estimator import utils

def main():
    """ Main """
    table = PrettyTable(['Task', 'Optimistic', 'Nominal', 'Pessimistic', 'Expected Duration', 'Standard Deviation'])

    add_task = True
    while add_task:
        task_name = input('Task name: ')
        optimistic_estimate = utils.get_user_input_number('Optimistic estimate: ')
        nominal_estimate = utils.get_user_input_number('Nominal estimate: ')
        pessimistic_estimate =  utils.get_user_input_number('Pessimistic estimate: ')
        add_task = utils.get_user_input_boolean('Add task? (Y/N): ')
        print('\n')

        expected_duration = utils.calculate_expected_duration(optimistic_estimate, nominal_estimate, pessimistic_estimate)
        standard_deviation = utils.calculate_standard_deviation(pessimistic_estimate, optimistic_estimate)

        table.add_row([task_name, optimistic_estimate, nominal_estimate, pessimistic_estimate, expected_duration, standard_deviation])

    print(table)

if __name__ == '__main__':
    sys.exit(main())