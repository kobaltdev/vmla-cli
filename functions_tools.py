import os
import shutil

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def rm_directory(dir_to_empty: str):
    if os.path.exists(dir_to_empty) and os.path.isdir(dir_to_empty):
        shutil.rmtree(dir_to_empty)


def set_file_path(filename: str):
    # Path du dossier de travail
    directory = os.path.dirname(__file__)
    # contruction du chemin de fichier complet
    file_to_compute = os.path.join(directory, filename)
    return file_to_compute

def ls_files_and_size(directory: str) -> list:
    ls_files = os.listdir(directory)
    
    for f in ls_files:
        size_in_mb = round((os.stat(os.path.join(directory, f)).st_size)/(1024*1024), 0)
        print(f"{f}  /  size : {size_in_mb} MB")


    
ls_files_and_size("./source_files")