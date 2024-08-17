import os
import shutil
import time


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def rm_directory(dir_to_empty: str):
    path = os.path.dirname(__file__)
    dir_to_rm = os.path.join(path, dir_to_empty)
    print("Deleting :", dir_to_rm)
    if os.path.exists(dir_to_rm) and os.path.isdir(dir_to_rm):
        try:
            shutil.rmtree(dir_to_rm)
            print("Deleted :", dir_to_rm)
        except Exception as e:
            print(e)
    else:
        print("No action performed : the directory does not exist or is empty.\n")
    input("Press enter to continue ...")


def get_one_directory_absolute_path(directory_name: str) -> str:
    base_path = os.path.dirname(__file__)
    subfolder_path = directory_name
    dir_abs_path = os.path.join(base_path, subfolder_path)
    return dir_abs_path


def get_one_file_absolute_path(filename: str):
    # Path du dossier de travail
    directory = os.path.dirname(__file__)
    # contruction du chemin de fichier complet
    file_to_compute = os.path.join(directory, filename)
    return file_to_compute


def ls_and_return_files_abs_format(directory: str) -> list:
    file_list = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            file_list.append(os.path.abspath(os.path.join(dirpath, f)))
    return file_list


def print_menu_and_return_choice(title: str, menu_entries: list):
    options = menu_entries
    terminal_menu = TerminalMenu(options, title=title)
    menu_entry_index = terminal_menu.show()
    return options[menu_entry_index]


def invalid_input():
    print("Please enter a valid input !")
    time.sleep(1)

