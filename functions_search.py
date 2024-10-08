"""
Contains all the searching functions.
"""

# IMPORTS
from env_and_queries import *
from functions_tools import *
import os
import gzip

"""
These 2 functions are used to find an expression in a file, wether it's compressed or plain.
Both returns a list of occurrences.
"""

def find_in_one_plain_file(file_name: str, expression: str) -> list:
    occurences = []
    expression_lower = expression.lower()
    with open(file=file_name, mode='r') as f:
        try:
            for line in f:
                line_lower = line.lower()
                if expression_lower in line_lower:
                    occurences.append(line)
        except UnicodeDecodeError as e:
        # print(f"Non-decodable content (probably raw binary) in this archive file : {file_name}")
            pass # Placeholder : if I need to perform something with this exception later
        except Exception as e:
            print(type(e).__name__)
            print(e)
    return occurences


def find_in_one_compressed_file(file_name: str, expression: str) -> list:
    occurences = []
    expression_lower = expression.lower()
    try:
        with gzip.open(file_name, 'rt') as archive:
            content = archive.readlines()
            for l in content:
                line_lower = l.lower()
                if expression_lower in line_lower:
                    occurences.append(l)
    except UnicodeDecodeError as e:
        # print(f"Non-decodable content (probably raw binary) in this archive file : {file_name}")
        pass # Placeholder : if I need to perform something with this exception
    except EOFError as e:
        pass # Placeholder : if I need to perform something with this exception
    except Exception as e:
        print(type(e).__name__)
        print(file_name, " : ", e)
    return occurences


"""
This function is the main dict builder based on the occurences returned by the indidual file searching functions.
It returns a dictionnary containing a nested dictionnary of occurrences, following this hierarchy :
> { expression1 : {
                    file1 found containing expression1 : [List of occurrences in the said file]
                    file2 found containing expression1 : [List of occurrences in the said file]
                    ....
                  }
    expression2 : {
                    file1 found containing expression2 : [List of occurrences in the said file]
                    file2 found containing expression2 : [List of occurrences in the said file]
                    ....
    }                 
    expression 3 
    ....
}   

This dict is then exported as a .json file (see export_dict_to_json() in functions_tools.py)
"""

def search_expression_in_files(root_directory: str, expressions_to_search: list, verbose_mode = False) -> dict:
    cls()
    print("Starting search now ...\n")
    expressions = expressions_to_search
    results_all_expressions = {}

    for e in expressions:
        print(f"Now searching expression : '{e}'")
        results_all_files = {}
        for root, dirs, files in os.walk(root_directory):
            for f in files:
                filename, file_extension = os.path.splitext(f)
                if file_extension == ".log" or file_extension == ".txt":
                    if verbose_mode == True:
                        print(f"Analyzing : {filename}")
                    current_file_name = os.path.join(root, f)
                    plain_file_occurences = find_in_one_plain_file(file_name=current_file_name, expression=e)
                    if len(plain_file_occurences) > 0:
                        results_all_files[f] = plain_file_occurences

                elif file_extension == ".gz":
                    if verbose_mode == True:
                        print(f"Analyzing : {filename}")
                    current_file_name = os.path.join(root, f)
                    gz_occurrences = find_in_one_compressed_file(file_name=current_file_name, expression=e)
                    if len(gz_occurrences) > 0:
                        results_all_files[f] = gz_occurrences      
                
            results_all_expressions[e] = results_all_files
    return results_all_expressions
