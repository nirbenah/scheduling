from scipy import optimize
import numpy as np
from graph import IndirectedGraph
from collections import defaultdict
from typing import Dict, Set, List, Tuple
import copy
import numpy


# transpose:
def transpose(list_of_lists : List[List[int]]):
    new_list_of_lists = list_of_lists
    return np.array(new_list_of_lists).T.tolist()


# sort the dict by the key as a number, except the first letter:
def sort_dict_by_keys(dictionary):
    sorted_dict = dict(sorted(dictionary.items(), key=lambda x: int(x[0][1:])))
    return sorted_dict


# from dict(j,m) to dict(m,{jobs}):
def dict_reverse(j_m_dict: Dict[str, str]) -> Dict[str, Set[str]]:
    reversed_dict = defaultdict(set)
    for key, value in j_m_dict.items():
        reversed_dict[value].add(key)
    reversed_dict = sort_dict_by_keys(reversed_dict)
    return dict(reversed_dict)


# from dict(m,{jobs}) to dict( m , ({jobs}, time) ):
def add_times_to_m_j(m_j: Dict[str, Set[str]], p_vals: List[List[int]]) -> Dict[str, Tuple[Set[str], int]]:
    dict_with_times: Dict[str, Tuple[Set[str], int]] = {}
    for m, set_of_j in m_j.items():
        set_sum = sum(p_vals[int(m[1:])][int(obj[1:])] for obj in set_of_j)
        dict_with_times[m] = (set_of_j, set_sum)
    return dict_with_times


# from dict(j,m) to dict( m , ({jobs}, time) ):
def sol_by_machine_with_times(j_m_dict: Dict[str, str], p_vals: List[List[int]]) -> Dict[str, Tuple[Set[str], int]]:
    sol_by_machine = dict_reverse(j_m_dict)
    return add_times_to_m_j(sol_by_machine, p_vals)


# from dict( m , ({jobs}, time) ) to dict(m, time)
def machine_with_times(sol_machine_times : Dict[str, Tuple[Set[str], int]]) -> Dict[str,  int]:
    just_machine_times = dict()
    for k, v in sol_machine_times.items():
        #print(k,v)
        just_machine_times[k] = v[1]
    return just_machine_times


# the run time of all machines together:
def print_run_time_of_machines(_dict: Dict[str,  int]):
    max_val = max(_dict.values())
    print(f'\nThe run took: {max_val:.3f}')


# nice way to print dict:
def print_dict(d : dict):
    for key in d:
        print(key, ' : ', d[key])
        # print("\n")
    print("\n\n")


def read_file_to_list_of_lists(file_path: str) -> List[List[str]]:
    # every line is a job with machine times, P transose
    result = []
    with open(file_path, 'r') as file:
        for line in file:
            words = line.strip().split(',')
            result.append(words)
    result = [[int(num) for num in sublist] for sublist in result]
    return result


def read_file_to_dict(filename):
    result_dict = {}

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespaces
            if line:
                key, value = line.split(':')
                key = key.strip()
                value = value.strip().strip('{}').split(', ')
                fixed_value = []
                for x in value:
                    fixed_value.append(x[1:-1])
                result_dict[key] = fixed_value
    return result_dict

def array_to_dict(array1):
    result_dict = {}
    for index, value in enumerate(array1):
        if value in result_dict:
            result_dict[value].append(index)
        else:
            result_dict[value] = [index]
    # Sort the dictionary by the keys
    sorted_dict = {k: v for k, v in sorted(result_dict.items())}

    return sorted_dict

def transform_dict(input_dict):
    result_dict = {}
    for key, value_set in input_dict.items():
        int_key = int(key[1:])  # Convert 'm0' to 0, 'm1' to 1, etc.
        int_values = sorted(int(val[1:]) for val in value_set)  # Convert {'j3', 'j4'} to [3, 4], etc.
        result_dict[int_key] = int_values
    return result_dict

def transform_file_to_dict(filename):
    result_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            # Strip the line of whitespace and split by the first space
            key_str, value_str = line.strip().split(' ', 1)
            
            # Convert key to required format 'm0', 'm1', etc.
            key = f"m{key_str}"
            
            # Convert value part to list of integers
            value_list = eval(value_str)
            
            # Convert the integers to the required format 'j3', 'j4', etc.
            value_set = [f"j{val}" for val in value_list]
            
            # Update the result dictionary
            result_dict[key] = value_set

    return result_dict
