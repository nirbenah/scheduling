from utils import *
import os


def generate_hard_clauses(m: int, j: int, file_name: str, top_number: int):
    with open(file_name, "w") as file:
        file.write("p " + "wcnf " + str(m*j) + " " + str(j + j*m * (m-1) // 2 + j*m) + " " + str(top_number) + "\n")
        for jj in range(j):
            file.write(str(top_number) + " ")
            for k in range(m):
                file.write(str(jj * m + k + 1) + " ")
            file.write("0\n")
            for k in range(m):
                for n in range(k):
                    file.write(str(top_number) + " -" + str(jj * m + k + 1) + " -" + str(jj * m + n + 1) + " 0\n")


def generate_soft_clauses(m: int, j: int, file_name: str, p_vals: List[List[int]]):
    with open(file_name, "a+") as file:
        file.seek(0, 2)
        for jj in range(j):
            for mm in range(m):
                file.write(str(p_vals[mm][jj]) + " -" + str(jj * m + mm + 1) + " 0\n")


def get_indexes_from_number(num, n):
    j = (num - 1) // n
    i = num - j * n - 1
    return i, j


def solver_output_to_schedule_solution(m: int, j: int, file_name):
    # each cell represents a job, the value represents the machine to run the job on
    jobs_on_machines = [None for _ in range(j)]
    with open(file_name, "r") as file:
        for line in file:
            tokens = line.split()
            if tokens[0] == "v":
                for token in tokens[1:]:
                    if int(token) > 0:
                        machine, job = get_indexes_from_number(int(token), m)
                        jobs_on_machines[job] = machine
                break
    return jobs_on_machines


def get_top_number(p_vals: List[List[int]]):
    return sum([sum(row) for row in p_vals])


class MaxSatSolver:
    def __init__(self, p_vals: List[List[int]]):
        self.p_vals = copy.deepcopy(p_vals)

    def generate_clauses(self, n_m, n_j):
        file_name = "tmp_file"
        generate_hard_clauses(n_m, n_j, file_name, get_top_number(self.p_vals))
        generate_soft_clauses(n_m, n_j, file_name, self.p_vals)
        return file_name

    def job_and_machine_solution(self):
        num_machines = len(self.p_vals)
        num_jobs = len(self.p_vals[0])
        file_name = self.generate_clauses(num_machines, num_jobs)
        solution_file = solver(file_name)
        output = solver_output_to_schedule_solution(num_machines, num_jobs, solution_file)
        os.remove(file_name)
        return output

    def dump_maxsat(self):
        num_machines = len(self.p_vals)
        num_jobs = len(self.p_vals[0])
        file_name = self.generate_clauses(num_machines, num_jobs)
        with open(file_name, 'r') as f:
            print(f.read())
        os.remove(file_name)



# p_vals_org = [[4, 3, 5], [1, 6, 2], [9, 7, 9], [3, 2, 1], [2, 1, 6]]
