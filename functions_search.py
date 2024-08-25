from env_and_queries import *
import os
import gzip


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
            pass # Placeholder : if I need to perform something with this exception
        except Exception as e:
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
    except Exception as e:
        print(file_name, " : ", e)
    return occurences


def search_expression_in_files(root_directory: str, search_type: str) -> dict:
    if search_type == "esxi":
        expressions_type = esxi_hardware
    else:
        expressions_type = vcenter_expressions

    results_all_expressions = {}

    for e in expressions_type:
        print(f"Now searching expression : '{e}'")
        results_all_files = {}
        for root, dirs, files in os.walk(root_directory):
            for f in files:
                filename, file_extension = os.path.splitext(f)
                if file_extension == ".log" or file_extension == ".txt":
                    current_file_name = os.path.join(root, f)
                    plain_file_occurences = find_in_one_plain_file(file_name=current_file_name, expression=e)
                    if len(plain_file_occurences) > 0:
                        results_all_files[f] = plain_file_occurences

                elif file_extension == ".gz":
                    current_file_name = os.path.join(root, f)
                    gz_occurrences = find_in_one_compressed_file(file_name=current_file_name, expression=e)
                    if len(gz_occurrences) > 0:
                        results_all_files[f] = gz_occurrences      
                
            results_all_expressions[e] = results_all_files
    return results_all_expressions
