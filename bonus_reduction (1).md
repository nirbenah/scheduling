# Reduction to MaxSAT (with hard and soft clauses)

Recall the problem: We are given a set $J$ of _jobs_, and a set $M$ of _machines_. Each machine can run at most one job at any given time. We are further given,
for each $i \in M$ and $j\in J$, the time $t_{i, j} > 0$ which is needed in order to execute job $j$ on machine $i$.

## Assigning each job to exactly one machine

You already found the correct constraints that model the assignment of each job in $J$ to exactly one machine in $M$.

For completeness, here are the constraints. We introduce a new Boolean variable $r_{i,j}$ for each $i \in M$ and for each $j \in J$, indictating that machine $i$ *runs* job $j$. We then add the following constraints:
* For every job $j \in J$, $j$ runs on at least one machine: $\bigvee_{i \in M} r_{i,j}$.
* For every job $j \in J$, $j$ runs on exactly one machine: $\bigwedge_{i \ne i', i, i' \in M} \, !(r_{i,j} \wedge r_{i',j})$. 

## The other constraints

We now explain how to extend the above constraints to an instance of MaxSAT, whose optimal (maximum) solution can be used to find the optimal (minimum) makespan.

### Variables and constraints that model the execution time of each machine

Let $MAX$ be an upper bound on the time needed to run jobs on any machine, in any allocation. That is, $$MAX := \max_{i \in M} \sum_{j \in J} t_{i, j}.$$

For every machine, we introduce $MAX$ new variables that represent time ticks. That is, for each machine $i \in M$, define new Boolean variables $q_{i,0}, q_{i,1}, ..., q_{i,MAX-1}$. When $q_{i,k}$ is true, it will mean that machine $i$ is running at time tick $k$.

For the sake of example, let's say $MAX = 10$. Further let's assume we have 3 machines, that is, $M = {0, 1, 2}$. 
It's best to imagine these time tick variables as a "linear sequence" of variables, as in the following:
```
Machine 0: q_{0, 0}, q_{0, 1}, q_{0, 2}, ..., q_{0, 9} // 10 time ticks
Machine 1: q_{1, 0}, q_{1, 1}, q_{1, 2}, ..., q_{1, 9} // 10 time ticks
Machine 2: q_{2, 0}, q_{2, 1}, q_{2, 2}, ..., q_{2, 9} // 10 time ticks
```
We will now add constraints so that if a machine $i\in M$ is allocated to run jobs for $T$ time (in total), then $q_{i,0}, ..., q_{i,T-1}$ will be true, and $q_{i,T}, ..., q_{i,MAX-1}$ will be false.

#### Capturing monotonicity

* For each machine $i \in M$, and every $k \in \\{1, ..., MAX-1\\}$, add the constraint: $q_{m,k} \implies q_{m,k-1}$. (Equivalently: $!q_{m,k} \vee q_{m,k-1}$).
* For each machine $i \in M$, and every $k \in \\{0, ..., MAX-2\\}$, add the constraint: $!q_{m,k} \implies !q_{m,k+1}$. (Equivalently: $q_{m,k} \vee !q_{m,k+1}$).

#### Capturing beginning time of each job

For each job, add variables that capture at which time tick it begins running. 
That is, for each $j \in J$, define new Boolean variables $s_{j, 0}, s_{j,1}, ..., s_{j,MAX-1}$. We will have $s_{j,k} = 1$ if and only if job $j$ starts running (on some machine) at time tick $k$.

It's best to imagine the variables $s_{j,k}$ as a linear sequence of variables, as in the following:
```
Job 0: s_{0, 0}, s_{0, 1}, s_{0, 2}, ..., s_{0, 9} 
Job 1: s_{1, 0}, s_{1, 1}, s_{1, 2}, ..., s_{1, 9} 
...
```
For each job $j\in J$, exactly one time tick $s_{j,k}$ should be true, while the other must be false (indicating that the job started exactly once). Add the constraint for capturing this. I.e.:
* For every job $j \in J$: $\bigvee_{0 \le k < MAX} s_{j,k}$.
* For every job $j \in J$: $\bigwedge_{0 \le k < k' < MAX} !(s_{j,k} \wedge s_{j,k'})$. 

#### Execution time for each machine

We now connect the machines time ticks (the variables $q$) and the job starts times (the variables $s$).

For each machine $i \in M$, job $j \in J$, and $k \in \\{0, ..., MAX-t_{i,j}\\}$, add the constraint 
$$r_{i,j} \wedge s_{j, k} \implies q_{i, k} \wedge q_{i, k+1} \wedge \ldots \wedge q_{i, k+t_{i,j}-1}.$$
That is, if machine $i$ runs job $j$ and $j$ starts at time tick $k$, then the time ticks $q_{i, k}$ up until $q_{i, k+t_{i,j}-1}$ are true. 

#### Execution times are uniqe

We don't allow for jobs to run in parallel on any machine. For that we add the constraints:

For each machine $i \in M$, jobs $j, j' \in J$ ($j \ne j'$), and $k \in \\{0, ..., MAX-t_{i,j}\\}$, add the constraint 
$$r_{i,j} \wedge r_{i,j'} \wedge s_{j, k} \implies !s_{j', k} \wedge !s_{j', k+1} \wedge \ldots \wedge !s_{j', k+t_{i,j}-1}.$$

Also, for each machine $i \in M$, jobs $j, j' \in J$ ($j \ne j'$), and $k \in \\{t_{i,j}-1, ..., MAX-1\\}$, add the constraint
$$r_{i,j} \wedge r_{i,j'} \wedge s_{j, k} \implies !s_{j', k} \wedge !s_{j', k-1} \wedge \ldots \wedge !s_{j', k-t_{i,j}+1}.$$


### Soft Clauses

Finally, add one new variable for each time tick; that is, for every $k \in \\{0, 1, \ldots, MAX-1\\}$, add
a new variable $o_k$. 

For all $k \in \\{0, 1, \ldots, MAX-1\\}$, add the constraint saying that $$o_k \iff \bigvee_{i \in M} q_{i, k}.$$
That is $o_k$ is true iff at least one machine runs some job at time tick $k$.

Add each of $!o_k$ as a soft clause (a total of $MAX$ soft clauses), each with weight 1.

Note that if the MaxSAT instance now has an optimal solution $opt$, then the optimal makespan will be $MAX-opt$.

