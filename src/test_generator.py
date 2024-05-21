import random

def write_random_grid_to_file(filename, rows, cols, max_val):
    with open(filename, 'w') as file:
        for _ in range(rows):
            row = [random.randint(1, max_val) for _ in range(cols)]
            file.write(', '.join(map(str, row)) + '\n')


filename = 'random_grid.txt'
jobs = 100
machines = 20
max_val = 100  # Maximum value for the random numbers

write_random_grid_to_file(filename, jobs, machines, max_val)
