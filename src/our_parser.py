import argparse
from typing import List
from lin_prog_solver import *
from utils import *
from real_exact import *
from new_max_sat_reduction import *


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('input_problem', help='Instance file format, which specifies the jobs, the machines, and the time matrix specifying the run time of each job on each machine.', type = str)
    parser.add_argument('-fe', '--export', help='add filename and export there', type = str)
    solution_type = parser.add_mutually_exclusive_group(required=True)
    solution_type.add_argument('-m', '--makespan', help='prints the makespan of the given schedule file. Should be activated with: schedule file format, which specifies an assignment of jobs to machines.', type = str)
    solution_type.add_argument('-a', '--approx', help='prints an approximate schedule by the approx solver', action='store_true')
    solution_type.add_argument('-ei', '--exact_ilp', help='prints a schedule by exact_ilp', action='store_true')
    # solution_type.add_argument('-di', '--dump_ilp', help='prints the ILP program', action='store_true')
    solution_type.add_argument('-em', '--exact_maxsat', help='prints a scheudle by exact_maxsat', action = 'store_true')
    solution_type.add_argument('-dm', '--dump_maxsat', help='prints the MaxSat program', action = 'store_true')
    solution_type.add_argument('-msfd', '--maxsat_sol_from_dimacs', help='prints the MaxSat program', type = str)
    
    # solution_type.add_argument('-bj', '--by_jobs', help='add filename and export there', action = 'store_true')

    args = parser.parse_args()

    print(f"Working on file \"{args.input_problem}\"\n")
    matrix_from_input = read_file_to_list_of_lists(args.input_problem)
    original_p = transpose(matrix_from_input)
    if args.makespan:
        print(f"calculating the makespan of the schedule \'{args.makespan}\'....\n")
        #sol_m_j = read_file_to_dict(args.makespan) # from old foramt:  m0  :  {'j1', 'j0', 'j4', 'j3'}.....
        sol_m_j = transform_file_to_dict(args.makespan)
        # print(sol_m_j)
        machine_with_times_var = machine_with_times(add_times_to_m_j(sol_m_j, original_p))
        print(machine_with_times_var)
        print_run_time_of_machines(machine_with_times_var)
    
    if args.approx:
        print("calculating the approximate solution....\n")
        approx = ApproxSolver(original_p)
        #print_dict(approx.machine_with_jobs_solution())
        sol_by_machines = transform_dict(approx.machine_with_jobs_solution())
        print("\n\noptimal schedule assignmnent:\nmachine [jobs]")
        if args.export:
            filename = args.export
            print("export to file " + filename)
            with open(filename, 'w') as file:
                for key, value in sol_by_machines.items():
                    file.write(f"{key} {value}\n")
        else:   
            for key, value in sol_by_machines.items() :
                print(key, value)
    if args.exact_ilp:
        print("calculating the exact_ilp solution....\n")
        exact_ilp = ExactILP(original_p)
        assignment_by_machines = exact_ilp.job_and_machine_solution()
        print("\n\noptimal schedule assignmnent:\nmachine [jobs]")
        if args.export:
            filename = args.export
            print("export to file " + filename)
            with open(filename, 'w') as file:
                for key, value in assignment_by_machines.items():
                    file.write(f"{key} {value}\n")
        else:   
            for key, value in assignment_by_machines.items() :
                print(key, value)

    # if args.dump_ilp:
    #         print("calculating the MaxSat program....\n")
    if args.maxsat_sol_from_dimacs:
        print("calculating the exact_maxsat solution....\n")
        exact_maxsat = MaxSatSolver(original_p)
        sol_j_to_m = solver_output_to_schedule_solution(exact_maxsat.M, exact_maxsat.J, args.maxsat_sol_from_dimacs)
        print("\nsolution by job to machine:")
        print(sol_j_to_m)
        sol_m_to_j = array_to_dict(sol_j_to_m)
        print("\n\noptimal schedule assignmnent:\nmachine [jobs]")
        if args.export:
            filename = args.export
            print("export to file " + filename)
            with open(filename, 'w') as file:
                for key, value in sol_m_to_j.items():
                    file.write(f"{key} {value}\n")
        else:
            for key, value in sol_m_to_j.items() :
                print(key, value)
    if args.exact_maxsat:
        print("need to combine the dump_maxSat + call to EvalMaxSat + taking the output to maxsat_sol_from_dimacs ")
    if args.dump_maxsat:
        print("calculating the dump_maxsat program....\n")
        dump_maxsat = MaxSatSolver(original_p)
        filename = "default_file_dimacs_format"
        if args.export:
            filename = args.export
        dump_maxsat.generate_clauses(dump_maxsat.M, dump_maxsat.J, filename)
    print("BYE")


if __name__ == '__main__':
    exit(main())
    
p_vals_org = [[4, 3, 5], [1, 6, 2], [9, 7, 9], [3, 2, 1], [2, 1, 6]]
solver = MaxSatSolver(transpose(p_vals_org))
