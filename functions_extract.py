import os, shutil, tarfile
from zipfile import ZipFile
from fnmatch import fnmatch
import gzip

from functions_tools import *


def unzip_one_file(zipfile_to_extract: str, target_dir = ".", keep_original_file = "yes") -> str:
    try:
        with ZipFile(zipfile_to_extract, 'r') as f:
            f.extractall(target_dir)
            extracted_file = f.filelist[0].filename
            extracted_file_abs_path = f"{target_dir}/{extracted_file}"
            if keep_original_file == "no":
                os.remove(zipfile_to_extract)
    except Exception as e:
        print("Error :", e)
    return extracted_file_abs_path


def untar_one_file(tarfile_to_extract: str, target_dir = ".", keep_original_file = "yes") -> None:
    try:
        with tarfile.open(tarfile_to_extract, 'r') as f:
            try:
                f.extractall(target_dir)
                print(f"Extracted : {f.name}")
            except Exception as e:
                print(e)
                input("Press Enter")
            if keep_original_file == "no":
                os.remove(tarfile_to_extract)
    except Exception as e:
        print("Error :", e)


def get_tar_archive_folder_root_name(archive_full_path: str) -> str:
    with tarfile.open(archive_full_path, 'r') as f:
        members = f.getmembers()
        first_member = members[0]
        splitted_first_member = first_member.path.split("/")
        return splitted_first_member[0]


def ungzip_one_file(gzipfile_to_extract: str, keep_original_file = "yes") -> None:
    try:
        with gzip.open(gzipfile_to_extract, 'rb') as f_in:
            with open(gzipfile_to_extract[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                print("Extracted : ", f_out.name)
                if keep_original_file == "no":
                    os.remove(gzipfile_to_extract)
    except Exception as e:
        print("Error :", e)


def parse_all_subdirs_and_extract(directory: str, keep_original_file = "yes") -> None:
    extensions_to_extract = ["*.gz", "*.tar", "*.zip"]

    for path, subdirs, files in os.walk(directory):
        for name in files:
            if fnmatch(name, extensions_to_extract[0]):
                ungzip_one_file((os.path.join(path, name)), keep_original_file=keep_original_file)
            if fnmatch(name, extensions_to_extract[1]):
                untar_one_file((os.path.join(path, name)), target_dir=path, keep_original_file=keep_original_file)
            if fnmatch(name, extensions_to_extract[2]):
                unzip_one_file((os.path.join(path, name)), target_dir=path, keep_original_file=keep_original_file)


def extract_initial_archive(file_to_extract: str, extraction_dir_path: str, full_extract = False) -> bool:
    print()
    print("Trying to extract :", file_to_extract)
    try:
        tgz_file = unzip_one_file(file_to_extract, extraction_dir_path, keep_original_file="yes")
        print("In progress ..")
        tgz_root_folder_name = get_tar_archive_folder_root_name(tgz_file)
        untar_one_file(tgz_file, extraction_dir_path, keep_original_file="yes")
        extracted_archive_dir_path = os.path.join(os.getcwd(), extraction_dir_path, tgz_root_folder_name)
        delete_files_by_type(directory=extraction_dir_path, file_extension=".tgz")
        if full_extract == True:
            parse_all_subdirs_and_extract(directory=extracted_archive_dir_path, keep_original_file="no")
        return True
    except Exception as e:
        print(e)

