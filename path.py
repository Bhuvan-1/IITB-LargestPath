import pulp

# Create a LP Maximization problem
Lp_prob = pulp.LpProblem('Problem', pulp.LpMaximize)


#############################################  Read from file the edges of graph, vertices
GRAPH='NewMap.txt'
file = open(GRAPH, "r")

edges = []              ## denote all edges in graph in the format (u,v,w)
ADJ = {}                ## Adjanecy list of graph, ADJ[i] gives indices of all edges incident on vertex i
N = int(file.readline())
for line in file:
    if(line == '\n'):
        continue
    data = line.split()
    edges.append((int(data[0]), int(data[1]), int(data[2])))

    if(int(data[0]) not in ADJ):
        ADJ[int(data[0])] = []
    if(int(data[1]) not in ADJ):
        ADJ[int(data[1])] = []

    ADJ[int(data[0])] += [ len(edges) - 1]
    ADJ[int(data[1])] += [ len(edges) - 1]


for i in range(1,N+1):
    if(i not in ADJ):
        ADJ[i] = []

################################################### Create problem Variables, constraints, objective

############# Variables

# A decision variable per edge
x = []
for i in range(len(edges)):
    x.append(pulp.LpVariable("x"+str(i), lowBound=0, upBound=1, cat='Integer'))


# A variable per vertex, number of visits
n = [0]
for i in range(1,N+1):
    n.append(pulp.LpVariable("n"+str(i), lowBound=0, upBound=4, cat='Integer'))


# A variable to denote end points.
f = [0]
for i in range(1,N+1):
    f.append(pulp.LpVariable("f"+str(i), lowBound=0, upBound=1, cat='Integer'))


# Objective function
Lp_prob += pulp.lpSum(x[i] * edges[i][2] for i in range(len(edges)))



############  Constraints

# Constraint 1: Each vertex must have 2 OR 0 edges
for i in range(1,N+1):
    Lp_prob += pulp.lpSum(x[j] for j in ADJ[i]) == 2*n[i] - f[i]

# Constraint 2: Only 2 end points
Lp_prob += pulp.lpSum(f[i] for i in range(1,N+1)) == 2




#################################################
# Solve the problem
status = Lp_prob.solve()
print(pulp.value(Lp_prob.objective))        ## Print the optimal objective function value


# Print the optimal path to a text file, for validation
file.close()
file = open("output.txt", "w+")
file.write(str(N) + "\n")
for i in range(len(edges)):
    if(pulp.value(x[i]) == 1):
        file.write(str(edges[i][0]) + " " + str(edges[i][1]) + "\n")

file.write("-1\n")

for i in range(1,N+1):
    if(pulp.value(f[i]) == 1):
        file.write(str(i) + "\n")

file.close()