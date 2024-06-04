To run the program, run python3 schedule.py, all the instructions are there too.<br />

To get the makespan of test (table) and assignment (by machines) :&nbsp; ./schedule test.txt --makespan schedule.txt <br />
To get the assignment  of test (table) :  &emsp; &emsp; &emsp; &emsp;&emsp; &emsp;&emsp; &emsp;&emsp;&emsp;&emsp; &nbsp;   ./schedule test.txt --method [approx | exact_ilp | exact_maxsat ] <br />
To get the input problem format : &emsp; &emsp; &emsp; &emsp;&emsp;&emsp; &emsp; &emsp; &emsp;&emsp; &emsp;&emsp; &nbsp; ./schedule test.txt --method [dump_maxsat] <br />
To get the assignment from the output of max sat : &emsp; &emsp; &emsp; &emsp;&emsp;&emsp;&nbsp; ./schedule test.txt --maxsat_sol_from_dimacs output.txt <br />
To every one of them you can export to a file by adding:  &emsp; &emsp; &emsp; &emsp;         --export file_name <br /> <br />

*** Test file format: every job is a line, t(j,i) = time of machine i to run job j. inedxes starts from zero. seperated by comma *** <br />

IMPORTANT: <br />
From personal experience pulp (used in exact_ilp) works well just with conda interpeter <br />
Scipy works well with python 3 (not conda) <br />

for example the simple test with the approx solution (scipy) does not work well with conda interpeter - the graph is built with too many edges <br />
but it works very well with /bin/python3 <br /> <br />

that's why sometimes the import pulp in comment, because when I use /bin/python3 it does not recognize pulp <br /> <br />

in real_exact.py (the ilp exact solver), there is a useful option to achieve better time: <br>
change from: <br>
&emsp; lp_problem.solve(solver) <br>
to: <br>
&emsp; solver = pulp.PULP_CBC_CMD(timeLimit=TIME_LIMIT_YOU_WANT) <br>
&emsp; lp_problem.solve(solver)
