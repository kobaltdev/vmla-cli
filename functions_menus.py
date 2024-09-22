"""
This contains all the functions used to display menus.
"""


# IMPORTS
from functions_extract import *
from functions_tools import *
from functions_search import *
from env_and_queries import *


def main_menu() -> None:
    global verbose_mode
    create_required_folders_if_needed(base_directory=(os.path.join(os.getcwd())))
    cls()
    print("****  Welcome to vmla-cli, a VMware log extractor and analyser  ****\n")
    print("Available actions : \n")
    print("1 - Extract an Esxi or vCenter log bundle")
    print("2 - Delete the /extracted_files folder")
    print("3 - Analyse an existing extracted log bundle")
    print("4 - Clear the /reports folder")
    print("5 - Switch verbose mode (extraction + search)\n")
    print("Q - Quit\n")
    answer_main_action = input("Your choice ? : ").lower()
    match answer_main_action:
        case "1":
            cls()
            extract_menu()
        case "2":
            rm_directory(dir_to_empty=extraction_dir, first_try=True)
            main_menu()
        case "3":
            cls()
            search_menu(verbose_mode=verbose_mode)
        case "4":
            rm_directory(dir_to_empty=reports_dir, first_try=True)
            main_menu()
        case "5":
            if verbose_mode == False:
                print("\nVerbose mode enabled")
                time.sleep(1)
                verbose_mode = True
                main_menu()
            else:
                print("\nVerbose mode disabled")
                verbose_mode = False
                time.sleep(1)
                main_menu()
        case "q":
            print("Bye !")
            quit()
        case _:
            invalid_input()


def extract_menu() -> None:
    global source_dir
    cls()
    source_dir = get_one_directory_absolute_path(directory_name=source_dir)
    list_of_files_in_source_dir = ls_and_return_files_abs_format(source_dir)
    n = 1
    print("Current log bundle file(s) in the /source folder :\n")
    if len(list_of_files_in_source_dir) == 0:
        print("! The /source_files folder is currently empty !\n")
        input("Press Enter to continue ...")
        main_menu()
    else:
        for f in list_of_files_in_source_dir:
            print(f"{n} - {f}")
            n += 1
    print()
    print(f"{n} - Back to main menu\n")
    try:
        answer_extract_file = int(input("Which file to extract ? = "))
        if answer_extract_file == len(list_of_files_in_source_dir)+1:
            main_menu()        
        if answer_extract_file > len(list_of_files_in_source_dir):
            invalid_input()
            extract_menu()
        if answer_extract_file <= 0:
            invalid_input()
            extract_menu()
        else:
            file_index = answer_extract_file - 1
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
                        extract_menu()
            if extract_initial_archive(file_to_extract=list_of_files_in_source_dir[file_index], 
                                    extraction_dir_path=extraction_dir, full_extract=full_extract):
                print()
                print("Log bundle successfully extracted.\n")
                input("Press Enter to continue ..")
                main_menu()            
    except ValueError as e:
        invalid_input()
        extract_menu()


def search_menu(verbose_mode: bool) -> None:
    global source_dir, extraction_dir, custom_dir, reports_dir
    cls()
    extracted_folder = ls_dir_current_folder(base_directory=extraction_dir)
    n = 1
    print("Choose an extracted log bundle directory to analyse :\n")
    if len(extracted_folder) == 0:
        print("The folder is currently empty\n")
        input("Press Enter to continue ...")
        main_menu()
    else:
        for f in extracted_folder:
            print(f"{n} - {f}")
            n += 1
    print()
    print(f"{n} - Back to main menu\n")
    try:
        answer_bundle_choice = int(input("Your choice ? = "))
        if answer_bundle_choice == len(extracted_folder)+1:
            main_menu()        
        if answer_bundle_choice > len(extracted_folder):
            invalid_input()
            search_menu(verbose_mode=verbose_mode)
        if answer_bundle_choice <= 0:
            invalid_input()
            search_menu(verbose_mode=verbose_mode)
        else:
            file_index = answer_bundle_choice - 1
    except ValueError as e:
        invalid_input()
        search_menu(verbose_mode=verbose_mode)
    search_type = check_bundle_type_and_return_log_path(directory_to_check=extracted_folder[file_index])
    search_path = build_var_log_path_and_return_it(directory=extracted_folder[file_index], bundle_type=search_type)
    chosen_search = search_menu2(bundle_type=search_type)
    if len(chosen_search) == 0:
        cls()
        print("The expression list is empty.")
        print("No action performed.\n")
        input("Press Enter to continue ...")
        main_menu()
    else:
        search_results = search_expression_in_files(root_directory=search_path, 
                                                    expressions_to_search=chosen_search, 
                                                    verbose_mode=verbose_mode)
        reports_dir_location = get_one_directory_absolute_path(directory_name=reports_dir)
        try:
            json_file = export_dict_to_json(dict_to_export=search_results,
                                base_folder=extracted_folder[file_index],
                                save_location=reports_dir_location)
            print("\nSearch results successfully exported as :", json_file)
            input("\nPress Enter to continue ...")
        except Exception as e:
            print("Error while generating the JSON export :", e)
            input("Press Enter to continue ...")
        main_menu()


def search_menu2(bundle_type: str = "") -> list:
    print(f"\nOk, you chose a '{bundle_type}' type bundle...\n")
    while True:
        cls()
        print("Do you want to perform :")
        print("1 - a generic search (most common hardware and services problems)")
        print("2 - a custom search (using your own searching expressions) ?")
        print("3 - choose another bundle\n")
        answer_search_type = input("Your choice ? = ")
        match answer_search_type:
            case "1":
                if bundle_type == 'esxi':
                    return esxi_generic
                else:
                    return vcenter_generic
            case "2":
                custom_expressions_file = choose_custom_expression_set_menu(bundle_type=bundle_type)
                list_from_custom_choice = get_infos_from_txt(custom_expressions_file)
                return list_from_custom_choice
            case "3":
                search_menu(verbose_mode=verbose_mode)
            case _:
                invalid_input()
                search_menu2(bundle_type=bundle_type)


def choose_custom_expression_set_menu(bundle_type :str = "") -> list:
    n = 1
    cls()
    available_custom_files = ls_and_return_files_abs_format(directory=os.path.join(os.getcwd(), custom_dir))
    if len(available_custom_files) == 0:
        cls()
        print("There is no custom .txt expression file in the /custom_searches folder\n")
        input("Press Enter to continue ...")
        main_menu()
    print("\n Choose a custom expressions file to use :\n")
    for c in available_custom_files:
        print(f"{n} - {c}")
        n += 1
    print()
    print(f"{n} - Back to search menu\n")
    try:
        answer_custom_list = int(input("Your choice ? = "))
        if answer_custom_list == len(available_custom_files)+1:
            search_menu(verbose_mode=verbose_mode)
        if answer_custom_list > len(available_custom_files)+1:
            invalid_input()
            choose_custom_expression_set_menu(bundle_type=bundle_type)
        if answer_custom_list <= 0:
            invalid_input()
            choose_custom_expression_set_menu(bundle_type=bundle_type)
        else:
            file_index = answer_custom_list - 1
            return available_custom_files[file_index]
    except ValueError as e:
        invalid_input()
        choose_custom_expression_set_menu(bundle_type=bundle_type)
    