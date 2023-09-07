# IMPLEMENTED ALGORITHM FOR SUBLINEAR MINIMUM SPANNING TREE
# Based on Section 3.2. of [CS10] 
# This implementation should be adjusted for a minimum spanning forest in the future

import sys
import random

DEBUG = False
USING_EXAMPLE = True

# random.seed(123)

if USING_EXAMPLE:
	N = 10
	maxWeight = 3
	maxQueries = 5
else:
	N = int(sys.stdin.readline()) # read number of nodes from the input
	maxWeight = int(sys.stdin.readline()) # read the largest weight of the graph
	maxQueries = int(sys.stdin.readline()) # maximum number of allowed queries

def getNeighbors(node):
	if USING_EXAMPLE:
		# Outputs for example.png (as found in example.txt)
		example_outputs = ["2 8 3 9 1", "2 3 1 4 3", "2 4 2 5 1", "4 1 1 4 2 6 3 7 3", "4 1 3 2 2 3 2 5 1", "3 2 1 4 1 8 3", "2 3 3 7 2", "4 3 3 6 2 8 3 9 1", "3 0 3 5 3 7 3", "2 0 1 7 1"]
		line = example_outputs[node].split()


	else:
		# ask kattis for the next node
		print(node)
		
		sys.stdout.flush()
		# read the answer we get from kattis
		line = sys.stdin.readline().split()
	# the answer has the form 'numNeighbors neighbor1 weight1 neighbor2 weight2 ...'
	# we want to have a list of the form:
	#[ (neighbor1, weight1), (neighbor2, weight2) , ...]
	return [ (int(line[i]), int(line[i+1]) ) for i in range(1, len(line), 2)]


# BFS performs a BREADTH-FIRST-SEARCH starting from 'root', and ignoring all edges of weight higher than 'w'
# If the BFS is terminated (fully explored) before visiting 'cap' nodes, we return 1
# If we have not terminated after 'cap' nodes, we return 0
def BFS(root, w, cap):
	nodes_checked = 0
	
	# Do BFS here but only expand along nodes that have weight at most w
	# Return 0 if nodes_checked reaches cap
	# Else return 1
	queue = [root]
	visited = [root]

	while queue:
		if nodes_checked >= cap:
			# We exceeded the cap X, thus b_i = 0
			if DEBUG:
				print("Failed to find full component (b_i = 0)")
			return 0


		m = queue.pop(0)
		adjacents = getNeighbors(m)
		nodes_checked += 1

		for neighbour in adjacents:
			if neighbour[0] not in visited and neighbour[1] <= w:
				visited.append(neighbour[0])
				queue.append(neighbour[0])

	# BFS terminated naturally, thus we return b_i = 1
	if DEBUG:
		print("Fully explored component (b_i = 1)")
	return 1


# Returns the approximate number of connected components in the graph of weight w 
# We only consider the edges in the graph that have weight less than or equal to w
# 
def approxConnectedComps(N, w, s):
	if DEBUG:
		print("Estimating components of size", w, "with", s, "different roots")
	b_sum = 0
	
	for i in range(s):
		# Picks a random node from the whole graph
		u_i = random.randrange(N) 

		# Choose X according to Pr[X ≥ k] = 1/k
		# Hint: If you pick a random Y uniformly from the interval [0,1] then P[Y <= t] = t for 0 <= t <= 1
		# By using t = 1/k and inverting the random variable we satisfy the requirement
		Y = random.uniform(0, 1)
		X = round(1 / Y) 
		
		# Run BFS ignoring all edges with weight greater than w, and a cap of checking X nodes
		if DEBUG:
			print("Time for BFS with cap", X)
		b_sum += BFS(u_i, w, X)

	return N/s * b_sum


c_estimators = []

for i in range(1, maxWeight):
	if DEBUG:
		print("Running first for components of weight", i)
	# Estimate the number of components in the graph with weight i
	
	# This is a temporary estimation. We allow at most maxQueries/W node-visits for each weight
	# This ensures the total number of queries W * s = maxQueries does not exceed the allowed amount
	queries = maxQueries/maxWeight
	# Instead of division by 2 we should divide by E[X], with X defined in the function above
	s = round(queries / 2) 
	s = (s if s>0 else 1) 

	c_estimators.append(approxConnectedComps(N, i, 60000))
	if DEBUG:
		print("Estimated number of components with weight", i, "is", c_estimators[-1])


if DEBUG:
	print(c_estimators)

MST_weight = N - maxWeight + sum(c_estimators)

# print the answer
print('end ' + str(MST_weight))
sys.stdout.flush()


if USING_EXAMPLE:
	if MST_weight > 0.9*15 and MST_weight < 1.1*15:
		print("Succesful 1.1-approximation")
	else:
		print("Failed to make a 1.1-approximation")
