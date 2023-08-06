import os
import logging
from datetime import datetime
from .print_manager import mcprint, Color


class DirectoryManager:
    class File:
        def __init__(self, path, name, extension, size, created_at):
            self.path = path
            self.name = name
            self.extension = extension
            self.size = size
            self.created_at = created_at

        def print_info(self):
            mcprint("Name: {}".format(self.name))
            mcprint("Path: {}".format(self.path))
            mcprint("Extension: {}".format(self.extension))
            mcprint("Size: {}".format(self.size))
            mcprint("Created at: {}".format(self.created_at))
            print()

        # Modify delete function
        def delete_file(self):
            mcprint("Deleting File <{}>".format(self.path), color=Color.RED)
            os.remove(self.path)

    def __init__(self, directories=None):
        if not directories:
            directories = [os.getcwd()]
        self.directories = directories
        self.files = []
        self.selected_files = []
        self.get_files()

    def get_dirs(self):
        dirs_list = []
        for file in self.files:
            dirs_list.append(file.path)
        return dirs_list

    # Retrieves a list of Files in self.files
    def get_files(self):
        import os

        def create_file(directory_name, new_file_name=None):

            file_dir = directory_name
            if new_file_name:
                file_dir = os.path.join(directory_name, new_file_name)
            else:
                new_file_name = file_dir.rsplit('\\', 1)[-1]

            created_at = datetime.fromtimestamp(os.path.getctime(file_dir)).strftime('%Y-%m-%d %H:%M:%S')
            file = self.File(file_dir, new_file_name, new_file_name.rsplit('.', 1)[-1],
                             os.path.getsize(file_dir), created_at)
            self.files.append(file)

        for directory in self.directories:
            if os.path.isdir(directory):
                if os.path.exists(directory):
                    for file_name in os.listdir(directory):
                        create_file(directory, file_name)
                else:
                    logging.error("Path \"{}\" doesn't exists".format(directory))
            elif os.path.isfile(directory):
                create_file(directory_name=directory)
            else:
                logging.error("Path \"{}\" not found".format(directory))

    def print_files_info(self):
        for file in self.files:
            file.print_info()

    def filter_format(self, extensions=None):
        new_files = []
        for file in self.files:
            if file.extension in extensions:
                new_files.append(file)
        self.files = new_files

    @staticmethod
    def create_directory(directory):
        try:
            os.makedirs(directory)
        except IsADirectoryError:
            logging.error(error_string="Couldn't create the directory '{}'".format(directory))

    def open_file(self, file):
        import platform
        import subprocess
        current_os = platform.system()

        if isinstance(file, self.File):
            path = file.path
        elif isinstance(file, str):
            path = file
        else:
            raise NotADirectoryError

        if os.path.isfile(path):
            logging.info("Open File <{}> // current os {}".format(file, current_os))
            if current_os == 'Linux':
                subprocess.call(('xdg-open', path))
            elif current_os == 'Windows':
                os.startfile(path)
            elif current_os == "Darwin":
                subprocess.call(('open', path))
            else:
                logging.error("OS not supported")

        else:
            logging.error("File \"{}\" not found".format(path))

    def add_file_to_selection(self, *args):
        logging.info("Adding Files <{}> to Selection".format(args))
        files = None
        for arg in args:
            if isinstance(arg, self.File):
                files = [arg]
            elif isinstance(arg, list):
                files = list(arg)
            elif isinstance(arg, str):
                files = list(filter(lambda x: arg in x.name, self.files))
            if files:
                self.selected_files += files
        return self.selected_files

    def clear_file_selection(self):
        self.selected_files.clear()
