from .print_manager import mcprint
from .input_validation import get_input
from .utilities import clear
import logging


class MenuFunction:
    def __init__(self, title=None, function=None, **kwargs):
        self.function = function
        self.title = title
        self.kwargs = kwargs
        self.returned_value = None

    def print_function_info(self):
        mcprint('Function: %s' % self.function)

        for parameter in self.kwargs:
            mcprint(parameter)

    def get_unassigned_params(self):
        unassigned_parameters_list = []
        for parameter in self.function.func_code.co_varnames:
            if parameter not in self.kwargs:
                mcprint(parameter)
                unassigned_parameters_list.append(parameter)
        return unassigned_parameters_list

    def get_args(self):
        mcprint(self.kwargs)
        return self.kwargs

    def call_function(self):
        self.returned_value = self.function(**self.kwargs)
        return self.returned_value


class Menu:

    def __init__(self, title=None, subtitle=None, text=None, options=None, return_type=int, parent=None,
                 input_each=False,
                 previous_menu=None, back=True):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.options = options
        self.return_type = return_type
        self.parent = parent
        self.input_each = input_each
        self.previous_menu = previous_menu
        self.back = back
        self.returned_value = None
        self.function_returned_value = None

    def set_parent(self, parent):
        self.parent = parent

    def set_previous_menu(self, previous_menu):
        self.previous_menu = previous_menu

    def get_selection(self):

        start_index = 1
        if self.back:
            start_index = 0

        # if there exist options it means user have to select one of them
        if (self.options.__len__() != 0) and (not self.input_each):

            while True:

                selection = get_input()

                if selection.__str__().isdigit():
                    if int(selection) in range(start_index, (self.options.__len__()) + 1):
                        if int(selection) != 0:
                            if isinstance(self.options[int(selection) - 1], MenuFunction):
                                function = self.options[int(selection) - 1]
                                self.function_returned_value = function.call_function()
                            elif isinstance(self.options[int(selection) - 1], Menu):
                                sub_menu = self.options[int(selection) - 1]
                                sub_menu.set_parent(self)
                                sub_menu.show()
                        else:
                            if self.parent:
                                self.parent.set_previous_menu(self)
                                self.parent.show()
                        break
                    else:
                        logging.warning('Index not in range')

                else:
                    logging.warning('Entered value must be int')

        elif self.input_each:
            selection = {}
            for option in self.options:
                print(option)
                if isinstance(self.options, dict):
                    filter_criteria = self.options[option]
                    return_type = int
                    if filter_criteria[0] in [str, int]:
                        return_type = filter_criteria[0]
                        filter_criteria = filter_criteria[1:]
                    parameter_value = get_input(format_='{} >> '.format(option),
                                                valid_options=filter_criteria,
                                                return_type=return_type)
                else:
                    parameter_value = get_input('{} >> '.format(option))
                selection[option] = parameter_value

        # if there aren't any option it means user must input a string
        else:
            selection = get_input()

        self.returned_value = selection
        return selection

    def show(self):

        # if(self.previous_menu != None) and (self != self.previous_menu):
        #     del(self.previous_menu)
        clear()
        if self.title:
            mcprint('=== %s ' % self.title)
        if self.subtitle:
            mcprint('- - %s' % self.subtitle)
        print()
        if self.text:
            mcprint(self.text)

        # print 'Parent:',self.parent
        if self.options and not self.input_each:
            for index, option in enumerate(self.options):
                if isinstance(option, MenuFunction):
                    print('%s. %s' % (str(index + 1), option.title))
                elif isinstance(option, Menu):
                    print('%s. %s' % (str(index + 1), option.title))
                else:
                    print('%s. %s' % (str(index + 1), option))
            if self.back:
                mcprint('0. Back')

        selected_option = self.get_selection()
        return selected_option
