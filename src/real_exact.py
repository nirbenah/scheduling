import pulp
from utils import *
 

#p = [[4, 1, 9, 3, 2], [3, 6, 7, 2, 1], [5, 2, 9, 1, 6]]

class ExactILP:
    def __init__(self, p_vals: List[List[int]]):
        self.p_vals = copy.deepcopy(p_vals)
    
    def job_and_machine_solution(self) -> Dict[str, str]:  
        # Create a linear programming problem
        lp_problem = pulp.LpProblem("Scheduling_Problem", pulp.LpMinimize)

        # Define decision variables x_i,j
        M = len(self.p_vals) # Define your set of machines
        J = len(self.p_vals[0])  # Define your set of jobs
        x = {}
        for i in range(M):
            for j in range(J):
                x[i, j] = pulp.LpVariable(f'x_{i}_{j}', cat=pulp.LpBinary)

        # Define the objective function: minimize t
        t = pulp.LpVariable('t', lowBound=0)  # Makespan
        lp_problem += t  # Objective

        # Add constraints
        for j in range(J):
            lp_problem += sum(x[i, j] for i in range(M)) == 1  # Each job is scheduled on one machine

        for i in range(M):
            lp_problem += sum(x[i, j] * self.p_vals[i][j] for j in range(J)) <= t  # Processing time constraint for each machine

        # Solve the linear programming problem
        lp_problem.solve()

        # Print the results
        schedule_by_machines = {}
        for i in range(M):
            schedule_by_machines[i] = []
        if pulp.LpStatus[lp_problem.status] == 'Optimal':
            print("Optimal Schedule:")
            for i in range(M):
                for j in range(J):
                    if pulp.value(x[i, j]) == 1:
                        # print(f"Job {j} is scheduled on Machine {i}")
                        schedule_by_machines[i].append(j)
            print(f"Makespan (t): {pulp.value(t)}")
            return schedule_by_machines
        else:
            print("***** No optimal solution found ********")
            
        