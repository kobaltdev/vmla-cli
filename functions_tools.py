from env_and_queries import *

from datetime import datetime

import os
import shutil
import time
import stat
import json



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
    # get the CWD
    directory = os.path.dirname(__file__)
    # build the abs path
    file_to_compute = os.path.join(directory, filename)
    return file_to_compute


def ls_and_return_files_abs_format(directory: str) -> list:
    file_list = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            file_list.append(os.path.abspath(os.path.join(dirpath, f)))
    return file_list


def ls_dir_current_folder(base_directory: str) -> list:
    dir_only = [f for f in os.listdir(base_directory) if os.path.isdir(os.path.join(base_directory, f))]
    return dir_only


def delete_files_by_type(directory: str, file_extension: str) -> None:
    dir_content = os.listdir(directory)
    for c in dir_content:
        if c.endswith(file_extension):
            os.remove(os.path.join(directory, c))


def create_required_folders_if_needed(base_directory: str) -> None:
    required_folders = [source_dir, extraction_dir, reports_dir, custom_dir]

    current_folders = ls_dir_current_folder(base_directory=base_directory)
    for f in required_folders:
        if f not in current_folders:
            os.mkdir(os.path.join(base_directory, f))


def check_bundle_type_and_return_log_path(directory_to_check: str) -> str:
    esxi_specific_mark = "altbootbank"
    dir_to_check_relative_path = f"{extraction_dir}/{directory_to_check}"
    full_dir_path = get_one_directory_absolute_path(dir_to_check_relative_path)
    folders_in_bundle = ls_dir_current_folder(full_dir_path)
    if esxi_specific_mark in folders_in_bundle:
        return "esxi"
    else:
        return "vcenter"


def build_var_log_location_and_return_path(directory: str, bundle_type: str) -> str:
    bundle_relative_path = f"{extraction_dir}/{directory}"
    full_dir_path = get_one_directory_absolute_path(bundle_relative_path)
    if bundle_type == "esxi":
        log_dir = f"{full_dir_path}/var"
        return log_dir
    else:
        log_dir = f"{full_dir_path}/var/log"
        return log_dir
    

def export_dict_to_json(dict_to_export: str, base_folder: str, save_location: str) -> str:
    splitted_folder_name = base_folder.split(".")
    t = datetime.now()
    output_file_name = (f"{splitted_folder_name[0]}_generated_at_{t.hour}_{t.minute}_{t.second}.json")
    export_path_name = os.path.join(save_location, output_file_name)
    
    with open(export_path_name, 'w') as outfile :
        json.dump(dict_to_export, outfile)
    return export_path_name


def get_infos_from_txt(txt_file: str) -> list:
    custom_expressions = []
    try:
        with open(txt_file, 'r') as input_file:
            content = input_file.readlines()
    except Exception as e:
        print(e)
    for line in content:
        if len(line) > 0:
            linea = line.rstrip()
            custom_expressions.append(linea)
    return custom_expressions


def invalid_input():
    print("Please enter a valid input !")
    time.sleep(1)

