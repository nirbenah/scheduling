from typing import Dict

#strategy:
# send to scipy with: integer ....

from lin_prog_solver import *

def exact_specific_integer_solver_by_simplex(T : int ,p_vals: List[List[int]])-> Dict[str, str]:
    p_rows = len(p_vals)
    p_cols = len(p_vals[0])
    A_ub = P_to_Aub(p_vals)
    A_eq = P_to_Aeq(p_vals)
    c = [0] * p_rows*p_cols #minimize x1+x2+....
    b_ub = [T] * p_rows
    b_eq = [1] * p_cols
    bounds = [(0,1)] * p_rows*p_cols
    res = optimize.linprog(c, A_ub, b_ub, A_eq, b_eq, bounds, 'highs', integrality = 1)
    return (res.success, res.x)

def exact_optimized_integer_solver_by_simplex(p_vals: List[List[int]])-> Dict[str, str]:
    print("~")
    min_T, max_T = greedy_alg(transpose(p_vals))
    #print(min_T, max_T)
    min_true_T = max_T
    res, min_true_X = exact_specific_integer_solver_by_simplex(max_T, p_vals)
    while(min_T <= max_T):
        print("Still binary search")
        middle = (max_T + min_T)//2
        #print(max_T, min_T, middle)
        res, x = exact_specific_integer_solver_by_simplex(middle, p_vals)
        if(res is True):
            min_true_T = middle
            min_true_X = x
            max_T = middle-1
        else:
            min_T = middle+1
    #print(min_true_X)
    return (min_true_T, min_true_X)

def exact_solver_to_dict_of_jobs_and_machine(p_vals: List[List[int]])-> Dict[str, str]:
    #the output is {job: machine}
    res, fractional_sol_as_vec = exact_optimized_integer_solver_by_simplex(p_vals)
    fractional_sol_as_mat = vec_to_mat(fractional_sol_as_vec, len(p_vals), len(p_vals[0]))
    dict_of_jobs_and_machine = dict()
    for m in range(len(fractional_sol_as_mat)):
        for j in range(len(fractional_sol_as_mat[0])):
            if fractional_sol_as_mat[m][j] == 1:
                dict_of_jobs_and_machine["j" + str(j)] = "m" + str(m)
    
    # for H, we add all the jobs and machine as vertexes , if there is a num that is >0 but not 1, we add edge.
    dict_of_jobs_and_machine = sort_dict_by_keys(dict_of_jobs_and_machine)    
    return dict_of_jobs_and_machine

rows = 10  # Number of rows in the list
cols = 100  # Number of columns in the list
matrix = numpy.random.uniform(1, 100, (rows, cols))
natrix_not_numpy = matrix.tolist()

P = [[4, 1, 9, 3, 2], [3, 6, 7, 2, 1], [5, 2, 9, 1, 6]]
print("~")
sol = exact_solver_to_dict_of_jobs_and_machine(natrix_not_numpy)
#print(sol)
sol_by_machine_with_times_var = sol_by_machine_with_times(sol, natrix_not_numpy)
print_dict(sol_by_machine_with_times_var)
machine_with_times_var = machine_with_times(sol_by_machine_with_times_var)
print_dict(machine_with_times_var)
print_run_time_of_machines(machine_with_times_var)