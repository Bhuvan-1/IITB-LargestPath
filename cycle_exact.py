import pulp


def solve(idx, edges, ADJ, N):
    Lp_prob = pulp.LpProblem('Problem', pulp.LpMaximize)


    ################################################### Create problem Variables, constraints, objective

    ############# Variables

    # A decision variable per edge
    x = []
    for i in range(len(edges)):
        x.append(pulp.LpVariable("x"+str(i), lowBound=0, upBound=1, cat='Integer'))


    # A variable per vertex, number of visits
    n = [0]
    for i in range(1,N+1):
        # n.append(pulp.LpVariable("n"+str(i), lowBound=0, upBound=2, cat='Integer'))   # Type 2 problem
        n.append(pulp.LpVariable("n"+str(i), lowBound=0, upBound=1, cat='Integer'))     # Type 1 problem


    ###########  Objective function
    Lp_prob += pulp.lpSum(x[i] * edges[i][2] for i in range(len(edges)))



    ###########  Constraints


    ## the selcted edge is removed
    Lp_prob += x[idx] == 0

    # Constraint 1: Each vertex must have 2 OR 0 edges
    for i in range(1,N+1):

        if( i in [edges[idx][0], edges[idx][1]]  ):
            Lp_prob += pulp.lpSum(x[j] for j in ADJ[i]) == 2*n[i] - 1       #end points
        else:
            Lp_prob += pulp.lpSum(x[j] for j in ADJ[i]) == 2*n[i]           # other vertices


    #################################################

    # Solve the , silently disabling the calculation log.
    status = Lp_prob.solve(pulp.PULP_CBC_CMD(msg=0))

    ## Check if the problem is feasible
    if(status == -1):
        return -1
    else:
        return pulp.value(Lp_prob.objective)


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
file.close()


for i in range(1,N+1):
    if(i not in ADJ):
        ADJ[i] = []




#################################################
# Solve the problem
ans = 0
for idx in range(len(edges)):
    Z = solve(idx, edges, ADJ, N)
    if(Z != -1):
        ans = max(ans, Z + edges[idx][2])


print("Optimal solution: ", ans)