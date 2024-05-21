import our_parser
print("Usage:")
print("To get the makespan of test (table) and assignment (by machines) : ./schedule test.txt --makespan schedule.txt")
print("To get the assignment  of test (table) :                           ./schedule test.txt --method [approx | exact_ilp | exact_maxsat ]")
print("To get the input problem format :                                  ./schedule test.txt --method [dump_ilp | dump_maxsat]")
print("To get the assignment from the output of max sat :                 ./schedule test.txt --maxsat_sol_from_dimacs output.txt")
print("To every one of them you can export to a file by adding:           --export file_name")
print("*** Test file format: every job is a line, t(j,i) = time of machine i to run job j. inexes starts from zero. seperated by comma ***")
print("IMPORTANT:")
print("*** From personal experience pulp exact_ilp works well just with conda interpeter, scipy works well with python 3 (not conda) ***\n\n")

#for example the simple example with the approx solution (scipy) does not work well with conda interpeter - the graph is built with too many edges.
#but it works very well with /bin/python3

#that's why sometimes the import pulp in comment
exec(open('our_parser.py').read())