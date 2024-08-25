from functions_extract import *
from functions_tools import *
from functions_search import *


def main_menu(source_directory: str, extraction_directory: str) -> str:
    cls()
    print("** Welcome to vmla-cli, a VMware log extractor and analyser **\n")
    print("1 - Extract a log bundle")
    print("2 - Delete the /extracted_files folder")
    print("3 - Analyse an existing extracted log bundle")
    print("Q - Quit\n")
    answer = input("Your choice ? : ").lower()
    match answer:
        case "1":
            cls()
            extract_menu(source_directory=source_directory, 
                         extraction_directory=extraction_directory)
        case "2":
            rm_directory(extraction_directory, first_try=True)
        case "3":
            cls()
            search_menu(source_directory=source_dir, extraction_directory=extraction_directory)
        case "q":
            print("Bye !")
            quit()
        case _:
            invalid_input()


def extract_menu(source_directory: str, extraction_directory: str) -> None:
    cls()
    source_dir = get_one_directory_absolute_path(source_directory)
    list_of_files_in_source_dir = ls_and_return_files_abs_format(source_dir)
    n = 1
    print("Current log bundle file(s) in the /source folder :\n")
    if len(list_of_files_in_source_dir) == 0:
        print("The folder is currently empty\n")
        input("Press Enter to continue ...")
        main_menu(source_directory, extraction_directory)
    else:
        for f in list_of_files_in_source_dir:
            print(f"{n} - {f}")
            n += 1
    print()
    print(f"{n} - Back to main menu\n")
    try:
        answer = int(input("Which file to extract ? = "))
        if answer == len(list_of_files_in_source_dir)+1:
            main_menu(source_directory, extraction_directory)        
        if answer > len(list_of_files_in_source_dir):
            invalid_input()
            extract_menu(source_directory, extraction_directory)
        if answer <= 0:
            invalid_input()
            extract_menu(source_directory, extraction_directory)
        else:
            file_index = answer - 1
            full_extract = False
            print()
            print("Do you want to perform a full extract ? (WARNING : this will consume a lot of space on your drive !)")
            print()
            fe = input("y/n : ").lower()
            while True:
                match fe:
                    case "y":
                        full_extract = True
                        break
                    case "n":
                        full_extract = False
                        break
                    case _:
                        invalid_input()
            if extract_initial_archive(file_to_extract=list_of_files_in_source_dir[file_index], 
                                    extraction_dir_path=extraction_directory, full_extract=full_extract):
                print()
                print("Log bundle successfully extracted.\n")
                input("Press Enter to continue ..")
                main_menu(source_directory, extraction_directory)            
    except ValueError as e:
        invalid_input()
        extract_menu(source_directory, extraction_directory)


def search_menu(source_directory: str, extraction_directory: str) -> None:
    cls()
    extracted_folder = ls_dir_current_folder(base_directory=extraction_directory)
    n = 1
    print("Choose an extracted log bundle directory to analyse :\n")
    if len(extracted_folder) == 0:
        print("The folder is currently empty\n")
        input("Press Enter to continue ...")
        main_menu(source_directory, extraction_directory)
    else:
        for f in extracted_folder:
            print(f"{n} - {f}")
            n += 1
    print()
    print(f"{n} - Back to main menu\n")
    try:
        answer = int(input("Your choice ? = "))
        if answer == len(extracted_folder)+1:
            main_menu(source_directory, extraction_directory)        
        if answer > len(extracted_folder):
            invalid_input()
            search_menu(source_directory, extraction_directory)
        if answer <= 0:
            invalid_input()
            search_menu(source_directory, extraction_directory)
        else:
            file_index = answer - 1
    except ValueError as e:
        invalid_input()
        search_menu(source_directory, extraction_directory)
    search_type = check_bundle_type_and_return_log_path(directory_to_check=extracted_folder[file_index])
    varlog = build_var_log_location_and_return_path(directory=extracted_folder[file_index], bundle_type=search_type)
    print(f"Ok, beginning search for this {search_type} bundle...\n")
    search_results = search_expression_in_files(root_directory=varlog, search_type=search_type)
    reports_dir_location = get_one_directory_absolute_path(directory_name=reports_dir)
    try:
        json_file = export_dict_to_json(dict_to_export=search_results,
                            base_folder=extracted_folder[file_index],
                            save_location=reports_dir_location)
        print("Search results successfully exported as :", json_file)
        input("\nPress Enter to continue ...")
    except Exception as e:
        print("Error while generating the JSON export :", e)
        input("Press Enter to continue ...")
    main_menu(source_directory, extraction_directory)
