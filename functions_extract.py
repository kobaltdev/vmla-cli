import os, shutil, tarfile
from zipfile import ZipFile
from fnmatch import fnmatch
import gzip

from functions_tools import rm_directory



def unzip_one_file(zipfile_to_extract: str, target_dir = ".", keep_original_file = "yes"):
    try:
        with ZipFile(zipfile_to_extract, 'r') as f:
            f.extractall(target_dir)
            extracted_file = f.filelist[0].filename
            extracted_file_abs_path = f"{target_dir}/{extracted_file}"
            print(f"Extracted from .zip : {extracted_file_abs_path}")
            if keep_original_file == "no":
                os.remove(zipfile_to_extract)
    except Exception as e:
        print("Error :", e)


def untar_one_file(tarfile_to_extract: str, target_dir = ".", keep_original_file = "yes"):

    try:
        with tarfile.open(tarfile_to_extract, 'r') as f:
            f.extractall(target_dir)
            print(f"Extracted from .tar : {f.name}")
            if keep_original_file == "no":
                os.remove(tarfile_to_extract)
    except Exception as e:
        print("Error :", e)


def ungzip_one_file(gzipfile_to_extract: str, keep_original_file = "yes"):
    try:
        with gzip.open(gzipfile_to_extract, 'rb') as f_in:
            with open(gzipfile_to_extract[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                print("Extracted from .gz : ", f_out.name)
                if keep_original_file == "no":
                    os.remove(gzipfile_to_extract)
    except Exception as e:
        print("Error :", e)


def parse_all_subdirs_and_extract(directory: str, keep_original_file = "yes"):
    extensions_to_extract = ["*.gz", "*.tar", "*.zip"]
    

    for path, subdirs, files in os.walk(directory):
        for name in files:
            if fnmatch(name, extensions_to_extract[0]):
                ungzip_one_file((os.path.join(path, name)), keep_original_file=keep_original_file)
            if fnmatch(name, extensions_to_extract[1]):
                untar_one_file((os.path.join(path, name)), target_dir=path, keep_original_file=keep_original_file)
            if fnmatch(name, extensions_to_extract[2]):
                unzip_one_file((os.path.join(path, name)), target_dir=path, keep_original_file=keep_original_file)

    for e in extensions_to_extract:
        for path, subdirs, files in os.walk(directory):
            for name in files:
                if fnmatch(name, e):
                    parse_all_subdirs_and_extract(directory, keep_original_file)

