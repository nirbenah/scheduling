from utils import *
import os


def generate_r(M: int, J: int, file_name: str, top_number: int, r: List[List[int]]):
    with open(file_name, "w") as file:
        file.write("p " + "wcnf " + str(222) + " " + str(7861-7) + " " + str(top_number) + "\n") #TODO change it for the real mumber of clauses and topnumber as well
        file.write("c  r clauses:"+"\n")
        for jj in range(J):
            file.write(str(top_number) + " ")
            for ii in range(M):
                file.write(str(r[ii][jj]) + " ")
            file.write("0\n")
            for ii in range(M):
                for n in range(ii):
                    file.write(str(top_number) + " -" + str(r[ii][jj]) + " -" + str(r[n][jj]) + " 0\n")

def generate_q(M: int, MAX: int, file_name: str, top_number: int, q: List[List[int]]):
    with open(file_name, "a") as file:
        file.write("c  q clauses:"+"\n")
        for ii in range(M):
            for k in range(MAX-1): #TODO: CHECK IF IT'S OK TO do only: q(m,k) --> q(m,k-1)
                file.write(str(top_number) + " " + str(q[ii][k]) + " -" + str(q[ii][k+1]) + " 0\n")

def generate_s(J: int, MAX: int, file_name: str, top_number: int, s: List[List[int]]):
    with open(file_name, "a") as file:
        file.write("c  s clauses:"+"\n")
        for jj in range(J):
            file.write(str(top_number) + " ")
            for ii in range(MAX):
                file.write(str(s[jj][ii]) + " ")
            file.write("0\n")
            for ii in range(MAX):
                for n in range(ii):
                    file.write(str(top_number) + " -" + str(s[jj][ii]) + " -" + str(s[jj][n]) + " 0\n")

def generate_execution_time_for_each_machine(P: List[List[int]], M: int, J: int, file_name: str, top_number: int, MAX: int, r: List[List[int]], q: List[List[int]], s: List[List[int]]):
    with open(file_name, "a") as file:
        file.write("c  execution_time_for_each_machine clauses:"+"\n")
        for ii in range(M):
            for jj in range(J):
                for k in range(MAX - P[ii][jj]+1):
                    for index_after_k in range(P[ii][jj]):
                        file.write(str(top_number) + " -" + str(r[ii][jj]) + " -" + str(s[jj][k]) + " " + str(q[ii][k + index_after_k]) + " 0\n")
                for k in range(MAX - P[ii][jj]+1, MAX): #new extention:
                    file.write(str(top_number) + " -" + str(s[jj][k]) + " -" + str(r[ii][jj]) + " 0\n")
                        

def generate_execution_time_are_unique(P: List[List[int]], M: int, J: int, file_name: str, top_number: int, MAX: int, r: List[List[int]], s: List[List[int]]):
    with open(file_name, "a") as file:
        file.write("c  generate_execution_time_are_unique clauses:"+"\n")
        for ii in range(M):
            for jj in range(J):
                for jj2 in range(J):
                    if jj == jj2:
                        continue
                    for k in range(0, MAX - P[ii][jj]):
                        for index_after_k in range(P[ii][jj]):
                            file.write(str(top_number) + " -" + str(r[ii][jj]) + " -" + str(r[ii][jj2]) + " -" + str(s[jj][k]) + " -" + str(s[jj2][k + index_after_k]) + " 0\n")
                    for k in range(P[ii][jj]-1, MAX):
                        for index_after_k in range(0, -P[ii][jj]+1):
                            file.write(str(top_number) + " -" + str(r[ii][jj]) + " -" + str(r[ii][jj2]) + " -" + str(s[jj][k])+ " -"  + str(s[jj2][k + index_after_k]) + " 0\n")


def generate_hard_clauses(P: List[List[int]], M: int, J: int, file_name: str, top_number: int, MAX: int, r: List[List[int]], q: List[List[int]], s: List[List[int]], o: List[int]):
    generate_r(M, J, file_name, top_number, r)
    generate_q(M, MAX, file_name, top_number, q)
    generate_s(J, MAX, file_name, top_number, s)
    generate_execution_time_for_each_machine(P, M, J, file_name, top_number, MAX, r, q, s)
    generate_execution_time_are_unique(P, M, J, file_name, top_number, MAX, r, s)

def generate_soft_clauses(M: int, J: int, MAX: int, file_name: str, o: List[int], q: List[List[int]], top_number: int):
    with open(file_name, "a") as file:
        file.write("c  soft clauses:"+"\n")
        for kk in range(MAX):
            file.write(str(top_number) + " -" + str(o[kk]) + " ")
            for ii in range(M):
                file.write( str(q[ii][kk]) + " ")
            file.write(" 0\n")
        for kk in range(MAX):
            for ii in range(M):
                file.write( str(top_number) + " -" + str(q[ii][kk]) + " " + str(o[kk]) + " 0\n" )
            
        for kk in range(MAX):
            file.write( str(1) + " -" +  str(o[kk]) + " 0\n" )

def get_indexes_from_number(num, n):
    j = (num - 1) // n
    i = num - j * n - 1
    return i, j


def solver_output_to_schedule_solution(m: int, j: int, file_name):
    # each cell represents a job, the value represents the machine to run the job on
    jobs_on_machines = [None for _ in range(j)]
    counter = 0
    with open(file_name, "r") as file:
        for line in file:
            tokens = line.split()
            if tokens[0] == "v":
                for token in tokens[1:]:
                    if counter == m*j:
                        break
                    counter+=1
                    if int(token) > 0:
                        machine, job = get_indexes_from_number(int(token), m)
                        jobs_on_machines[job] = machine
                break
    return jobs_on_machines


def get_top_number(p_vals: List[List[int]]):
    return sum([sum(row) for row in p_vals])



def max_sum_line(p_vals: List[List[int]]) -> int:
    # Initialize the maximum sum to be very small
    max_sum = float('-inf')
    
    # Iterate over each sublist
    for sublist in p_vals:
        # Calculate the sum of the current sublist
        current_sum = sum(sublist)
        # Update the maximum sum if the current sum is greater
        if current_sum > max_sum:
            max_sum = current_sum
    
    return max_sum

class MaxSatSolver:
    def __init__(self, p_vals: List[List[int]]):
        self.p_vals = copy.deepcopy(p_vals)
        self.M = len(p_vals)
        self.J = len(p_vals[0])
        self.MAX = max_sum_line(self.p_vals)
        self.r = [[0 for _ in range(self.J)] for _ in range(self.M)]
        self.q = [[0 for _ in range(self.MAX)] for _ in range(self.M)]
        self.s = [[0 for _ in range(self.MAX)] for _ in range(self.J)]
        self.o = [0 for _ in range(self.MAX)]
        counter = 1
        for j in range(self.J): #by column
            for i in range(self.M):
                self.r[i][j] = counter
                counter +=1
        for i in range(self.M):
            for k in range(self.MAX):
                self.q[i][k] = counter
                counter +=1   
        for j in range(self.J):
            for k in range(self.MAX):
                self.s[j][k] = counter
                counter +=1
        for k in range(self.MAX):
            self.o[k] = counter
            counter +=1   
        
    def generate_clauses(self, M, J, file_name = "dimacs_format"):
        generate_hard_clauses(self.p_vals, M, J, file_name, get_top_number(self.p_vals), self.MAX, self.r, self.q, self.s, self.o)
        generate_soft_clauses(M, J,  self.MAX, file_name, self.o, self.q, get_top_number(self.p_vals))

        print("DONE")
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


def transpose(list_of_lists : List[List[int]]):
    new_list_of_lists = list_of_lists
    return np.array(new_list_of_lists).T.tolist()

# p_vals_org = [[4, 3, 5], [1, 6, 2], [9, 7, 9], [3, 2, 1], [2, 1, 6]]
# solver = MaxSatSolver(transpose(p_vals_org))
# solver.generate_clauses(solver.M, solver.J)