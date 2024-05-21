from typing import List
from scipy import optimize
import numpy as np
from graph import IndirectedGraph
from collections import defaultdict
from typing import Dict, Set, List, Tuple
import copy
from utils import *

class ObviousSolver:
    def __init__(self, p_vals: List[List[int]]):
        self.p_vals = copy.deepcopy(p_vals)
        self.M = len(p_vals)
        self.J = len(p_vals[0])
    
    @staticmethod    
    def calculating_longest_machine_time(jobs_array: List,  M: int, J: int, p_vals: List[List[int]]):
        m_list = [0] * M
        for j in range(J):
            m_list[jobs_array[j]] += p_vals[jobs_array[j]][j]
        return max(m_list), m_list

    @staticmethod
    def best_sol(M: int, J: int, p_vals: List[List[int]])-> Dict[str, str]:
        best_jobs_array = [None] * J
        best_dict = dict()
        best_m_list = [None] * M 
        shortest_time = float('inf')
        jobs_array = [None] * J
        num_of_options = M ** J 
        for x in range(num_of_options):
            temp_X = x
            for y in range(J):
                jobs_array[y] = temp_X % M
                temp_X = temp_X//M
            time, m_list = ObviousSolver.calculating_longest_machine_time(jobs_array, M, J, p_vals)
            if(time<shortest_time):
                shortest_time = time
                best_jobs_array = copy.deepcopy(jobs_array)
                best_m_list = m_list
        
        best_dict = {'j' + str(index): 'm' + str(value) for index, value in enumerate(best_jobs_array)}
        return best_dict, shortest_time, best_m_list
    
    def print_obvious_sol(self):
        sol = ObviousSolver.best_sol(self.M, self.J, self.p_vals)
        print(f"The shortest time found is:{sol[1]}")
        print("The solution by jobs:")
        print(sol[0])

# solver = ObviousSolver([[4, 1, 9, 3, 2,], [3, 6, 7, 2, 1], [5, 2, 9, 1, 6]])
# solver.print_obvious_sol()