from lin_prog_solver import *
from scheduling_new.job_scheduling_to_push.src.nice_but_not_to_final_sol.brute_force_solver import *
# from real_exact import *

#tests:
rows = 20  # Number of rows in the list
cols = 1000  # Number of columns in the list
matrix = numpy.random.randint(1, 100, (rows, cols))
matrix_not_numpy = matrix.tolist()
# # print(natrix_not_numpy)
# approx = ApproxSolver(matrix_not_numpy)
# #print_dict(approx.job_and_machine_solution())
# print_dict(approx.machine_with_times_solution())
# #approx.print_run_time_of_machines()


print("____________________________________________________________")

# exact_ilp = ExactILP(matrix_not_numpy)
# exact_ilp.job_and_machine_solution()

P = [[4, 1, 9, 3, 2], [3, 6, 7, 2, 1], [5, 2, 9, 1, 6]]

approx = ApproxSolver(P)
print_dict(approx.job_and_machine_solution())
print_dict(approx.machine_with_times_solution())
approx.print_run_time_of_machines()
print("____________________________________________________________")
obvious = ObviousSolver(P)
obvious.print_obvious_sol()