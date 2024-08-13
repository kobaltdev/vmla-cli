from functions_extract import *
from functions_tools import *

import os
from simple_term_menu import TerminalMenu


zip_file_esxi = "./source_files/VMware-vCenter-support-2024-08-08@18-19-48.zip"
zip_file_vcenter = "./source_files/VMware-vCenter-support-2024-08-09@12-09-50.zip"
tar_file_esxi = "./extracted_files/172.16.108.52-vm2024-8-08@18-19-48.tgz"
tar_file_vcenter = "./extracted_files/pcc-145-239-249-63.ovh.uk-vcsupport2024-9-08@12-18-52.tgz"
extraction_dir = "./extracted_files"

rm_directory("./extracted_files/")

cls()

# def menu1(options):
#     terminal_menu = TerminalMenu(options, title="TITRE DE MENU", status_bar="this is a status bar")
#     menu_entry_index = terminal_menu.show()
#     print(f"You have selected {options[menu_entry_index]}!")

# ls_files_and_size("./source_files")


# if __name__ == "__main__":
#     main()

unzip_one_file(zip_file_vcenter, extraction_dir)

untar_one_file(tar_file_vcenter, extraction_dir)

parse_all_subdirs_and_extract(extraction_dir, keep_original_file="no")