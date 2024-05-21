from utils import *
import sys


# The pre-alg' phase:
def greedy_alg(p_vals: List[List[int]]):
    #gets transposed mat JxM
    machines = [0] * len(p_vals[0]) 
    for item in p_vals: # a line - machine
        machines[item.index(min(item))] += min(item)
    return (max(machines) / len(p_vals[0]), max(machines)) #(alpah/M, alpha)
# print(greedy_alg([[4, 3, 5], [1, 6, 2], [9, 7, 9], [3, 2, 1], [2, 1, 6]]))

def P_to_Aub(p_vals: List[List[int]],):
    #from M X J to M X M*J
    #line 1 0....0
    #.............
    #0....0 line n
    p_rows = len(p_vals)
    p_cols = len(p_vals[0])
    Aub = [[0 for _ in range(p_rows*p_cols)] for _ in range(p_rows)]
    for m in range(len(Aub)):
        for j in range(len(Aub[0])):
            if(m*p_cols <= j and j <=(m+1)*p_cols-1):
                Aub[m][j] = p_vals[m][j%p_cols]
    return Aub
#print(P_to_Aub([[4, 1, 9, 3, 2,], [3, 6, 7, 2, 1], [5, 2, 9, 1, 6]]))
            
def P_to_Aeq(p_vals: List[List[int]]):
    #from M X J to J X M*J
    #1000010000100000
    #.............
    #0000100001000001
    p_rows = len(p_vals)
    p_cols = len(p_vals[0])
    Aeq = [[0 for _ in range(p_rows*p_cols)] for _ in range(p_cols)]
    for m in range(len(Aeq)):
        for j in range(len(Aeq[0])):
            if(j%p_cols == m):
                Aeq[m][j] = 1
    return Aeq
#print(P_to_Aeq([[4, 1, 9, 3, 2,], [3, 6, 7, 2, 1], [5, 2, 9, 1, 6]]))

def inf_all_the_numbers_bigger_than_T(T: int, p_vals: List[List[int]]):
    p_rows = len(p_vals)
    p_cols = len(p_vals[0])
    new_p_vals = copy.deepcopy(p_vals)
    for m in range(p_rows):
        for j in range(p_cols):
            if p_vals[m][j] > T:
                new_p_vals[m][j] = 1000000000000000 # sys.maxsize // 10
    return new_p_vals
#print(inf_all_the_numbers_bigger_than_T(4, [[4, 1, 9, 3, 2,], [3, 6, 7, 2, 1], [5, 2, 9, 1, 6]]))

def fractional_LP(T: int, p_vals: List[List[int]]):
    updated_p_vals = inf_all_the_numbers_bigger_than_T(T, p_vals) #p_vals.copy() #
    p_rows = len(updated_p_vals)
    p_cols = len(updated_p_vals[0])
    A_ub = P_to_Aub(updated_p_vals)
    A_eq = P_to_Aeq(updated_p_vals)
    c = [1] * p_rows*p_cols #minimize x1+x2+....
    b_ub = [T] * p_rows
    b_eq = [1] * p_cols
    bounds = [(0,1)] * p_rows*p_cols
    #res = optimize.linprog(c, A_ub, b_ub, A_eq, b_eq, bounds, method = 'highs')
    res = optimize.linprog(c, A_ub, b_ub, A_eq, b_eq, bounds)
    #simplex is wrong, we did not receive right results with it, highs crashes the CL
    return (res.success, res.x)


def X_fractional_sol(p_vals: List[List[int]]):
    min_T, max_T = greedy_alg(transpose(p_vals))
    #print(min_T, max_T)
    min_true_T = max_T
    res, min_true_X = fractional_LP(max_T, p_vals)
    while(min_T <= max_T):
        middle = (max_T + min_T)//2
        #print(max_T, min_T, middle)
        res, x = fractional_LP(middle, p_vals)
        # print("_______________________")
        # print(min_T)
        # print(max_T)
        # print("_______________________")
        if(res is True):
            min_true_T = middle
            min_true_X = x
            max_T = middle-1
        else:
            min_T = middle+1
    #print(min_true_X)
    return (min_true_T, min_true_X)
#print(X_fractional_sol([[4, 1, 9, 3, 2,], [3, 6, 7, 2, 1], [5, 2, 9, 1, 6]]))


def vec_to_mat(x, rows, cols):
    
    new_x = [[0 for _ in range(cols)] for _ in range(rows)]
    for m in range(rows):
        for j in range(cols):
            new_x[m][j] = round(x[(m * cols) + j],5)
    return new_x


class ApproxSolver:
    def __init__(self, p_vals: List[List[int]]):
        self.p_vals = copy.deepcopy(p_vals)

    def job_and_machine_solution(self) -> Dict[str, str]:
        #the output is {job: machine}
        res, fractional_sol_as_vec = X_fractional_sol(self.p_vals)
        # print("____________________________________________")
        # print("res:")
        # print(res)
        fractional_sol_as_mat = vec_to_mat(fractional_sol_as_vec, len(self.p_vals), len(self.p_vals[0]))
        # print("____________________________________________")
        # print(fractional_sol_as_mat) #helps to understand the first phase division
        dict_of_jobs_and_machine = dict()
        H = IndirectedGraph()
        for m in range(len(fractional_sol_as_mat)):
            for j in range(len(fractional_sol_as_mat[0])):
                if fractional_sol_as_mat[m][j] == 1:
                    dict_of_jobs_and_machine["j" + str(j)] = "m" + str(m)
                elif fractional_sol_as_mat[m][j]>0:
                    # print("Graph was built")
                    H.add_edge("m" + str(m), "j" + str(j))
        
        # print(H.maximum_matching())
        print("dict_of_jobs_and_machine")
        # for H, we add all the jobs and machine as vertexes , if there is a num that is >0 but not 1, we add edge.
        dict_of_jobs_and_machine.update(H.maximum_matching())
        dict_of_jobs_and_machine = sort_dict_by_keys(dict_of_jobs_and_machine)
        # print(dict_of_jobs_and_machine)
        return dict_of_jobs_and_machine
    
    def machine_with_jobs_solution(self) -> Dict[str, Set[str]]:
        return dict_reverse(self.job_and_machine_solution())
    
    def machine_with_jobs_and_times_solution(self) -> Dict[str, Tuple[Set[str], int]]:
        return sol_by_machine_with_times(self.job_and_machine_solution(), self.p_vals)
    
    def machine_with_times_solution(self) -> Dict[str,  int]:
        return machine_with_times(self.machine_with_jobs_and_times_solution())
    
    def print_run_time_of_machines(self):
        return print_run_time_of_machines(self.machine_with_times_solution())
    