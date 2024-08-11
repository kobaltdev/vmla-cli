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


def parse_all_subdirs_and_extract(directory: str):
    extensions_to_extract = ["*.gz", "*.tar", "*.zip"]

    for path, subdirs, files in os.walk(directory):
        for name in files:
            if fnmatch(name, extensions_to_extract[0]):
                ungzip_one_file((os.path.join(path, name)), keep_original_file="yes")
            if fnmatch(name, extensions_to_extract[1]):
                untar_one_file((os.path.join(path, name)), target_dir=path, keep_original_file="yes")
            if fnmatch(name, extensions_to_extract[2]):
                unzip_one_file((os.path.join(path, name)), target_dir=path, keep_original_file="yes")



zip_file_esxi = "/home/coffee/vmla-cli/source_files/VMware-vCenter-support-2024-08-08@18-19-48.zip"
zip_file_vcenter = "/home/coffee/vmla-cli/source_files/VMware-vCenter-support-2024-08-09@12-09-50.zip"
tar_file_esxi = "/home/coffee/vmla-cli/extracted_files/172.16.108.52-vm2024-8-08@18-19-48.tgz"
tar_file_vcenter = "/home/coffee/vmla-cli/extracted_files/pcc-145-239-249-63.ovh.uk-vcsupport2024-9-08@12-18-52.tgz"
extraction_dir = "/home/coffee/vmla-cli/extracted_files"

rm_directory("./extracted_files/")

unzip_one_file(zip_file_vcenter, extraction_dir)

untar_one_file(tar_file_vcenter, extraction_dir)

parse_all_subdirs_and_extract(extraction_dir)