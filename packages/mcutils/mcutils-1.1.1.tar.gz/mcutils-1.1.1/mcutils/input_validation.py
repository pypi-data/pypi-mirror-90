from .print_manager import mcprint, Color
import logging


def exit_application(text=None, enter_quit=False):
    if text:
        mcprint(text=text, color=Color.YELLOW)
    logging.info('Exiting Application Code:0')
    if enter_quit:
        get_input('Press Enter to exit...')
    exit(0)


def print_error(operators_list=None, contains_list=None, return_type=None):
    if operators_list:
        for operator in operators_list:
            if return_type == int:
                logging.warning('input must be {}'.format(operator))
            elif return_type == str:
                logging.warning('input length must be {}'.format(operator))
    if contains_list:
        logging.warning('input must be one of the following')
        for contains in contains_list:
            mcprint(text='\t{}'.format(contains), color=Color.RED)


def input_validation(user_input, return_type, valid_options):
    if return_type == int:
        if not user_input.isnumeric():
            return False
        user_input = int(user_input)

    # Contains validation
    if valid_options:

        operators_list = list(filter(lambda x: str(x).startswith(('<', '>', '==', '!=')), valid_options))
        contains_list = list(set(valid_options) - set(operators_list))

        # Complex validation
        # Special operators
        for operator in operators_list:
            if '<=' in operator:
                value = operator.replace('<=', '')
                if return_type == int:
                    if not user_input <= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) <= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '>=' in operator:
                value = operator.replace('>=', '')
                if return_type == int:
                    if not user_input >= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) >= int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '<' in operator:
                value = operator.replace('<', '')
                if return_type == int:
                    if not user_input < int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) < int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '>' in operator:
                value = operator.replace('>', '')
                if return_type == int:
                    if not user_input > int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) > int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

            elif '==' in operator:
                value = operator.replace('==', '')
                if return_type == int:
                    if not user_input == int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) == int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
            elif '!=' in operator:
                value = operator.replace('!=', '')
                if return_type == int:
                    if not user_input != int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False
                elif return_type == str:
                    if not len(user_input) != int(value):
                        print_error(operators_list=operators_list, return_type=return_type)
                        return False

        # if contains in valid options
        if len(contains_list) > 0:
            if user_input not in contains_list:
                return False

    return True


def get_input(format_='>> ', text=None, can_exit=True, exit_input='exit', valid_options=None, return_type=str,
              validation_function=None, color=None):
    if text:
        mcprint(text=text, color=color)

    while True:
        user_input = input(format_)

        # Emergency exit system
        if user_input == exit_input:
            if can_exit:
                exit_application()
            else:
                logging.warning('Can\'t exit application now')

        # This is the build-in validations system
        if validation_function:
            validation = validation_function.__call__(user_input)

        # This is the external validation system
        else:
            # from input_validation import input_validation
            validation = input_validation(user_input=user_input, return_type=return_type, valid_options=valid_options)
        if validation:
            break

        logging.warning('Not Valid Entry')

    return user_input
