import os
import shutil
import time
import stat


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def fix_perm(directory_to_fix: str):
    for root, dirs, files in os.walk(directory_to_fix):
        for d in dirs:
            # recursively fix directories
            os.chmod(os.path.join(root, d), stat.S_IWUSR)
        for f in files:
            # recursively fix files
            os.chmod(os.path.join(root, f), stat.S_IWUSR)
    

def rm_directory(dir_to_empty: str, first_try: bool):
    path = os.path.dirname(__file__)
    dir_to_rm = os.path.join(path, dir_to_empty)
    print("Trying to delete :", dir_to_rm, "\n")
    if os.path.exists(dir_to_rm) and os.path.isdir(dir_to_rm):
        try:
            shutil.rmtree(dir_to_rm)
            print("Deletion is successful !\n")
            time.sleep(2)
        except PermissionError:
            if first_try:
                fix_perm(directory_to_fix=dir_to_empty)
                rm_directory(dir_to_empty=dir_to_empty, first_try=False)
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


def invalid_input():
    print("Please enter a valid input !")
    time.sleep(1)