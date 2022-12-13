from string import ascii_lowercase
import numpy as np

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path


def read_input():
	with open('./day12Input.txt', 'r') as f:
		data = f.readlines()

	data = [x.strip() for x in data]

	array = []

	for row in data:
		array.append([x for x in row])

	return np.array(array)


def node_number(i, j, N):
	return i * N + j


def make_adjacency_matrix(grid):
	# from the grid, create A where A[(i,j), (k, l)] is cost (1) of moving from (i,j) to (k,l)

	# initialize A
	M = grid.shape[0]
	N = grid.shape[1]

	A = np.zeros((M*N, M*N))

	for i in range(M):
		for j in range(N):

			# construct node number
			nn = node_number(i, j, N)

			# set self-movement to 0
			A[nn][nn] = 0

			# viable neighbors
			# construct neighbors
			left_neighbor = (i, j-1)
			right_neighbor = (i, j+1)
			top_neighbor = (i-1, j)
			bottom_neighbor = (i+1, j)

			neighbors = [left_neighbor, right_neighbor, top_neighbor, bottom_neighbor]

			neighbors = [neighbor for neighbor in neighbors if neighbor[0] in range(0, grid.shape[0]) and neighbor[1] in range(0, grid.shape[1]) and ascii_lowercase.find(grid[neighbor[0]][neighbor[1]]) <= ascii_lowercase.find(grid[i][j]) + 1]

			for neighbor in neighbors:
				# is movement from (i,j) to (k,l) possible?
				if ascii_lowercase.find(grid[neighbor[0]][neighbor[1]]) <= ascii_lowercase.find(grid[i][j]) + 1:
					#movement possible

					# make node number
					neighbor_nn = node_number(neighbor[0], neighbor[1], N)
					A[nn, neighbor_nn] = 1

	return A



def part1():
	grid = read_input()

	# handle start and end letters
	start = np.where(grid == "S")
	end = np.where(grid == "E")

	# edit the grid
	grid[grid == "S"] = "a"
	grid[grid == "E"] = "z"

	# make starting node number
	start_nn = node_number(start[0][0], start[1][0], grid.shape[1])

	# make end node number
	end_nn = node_number(end[0][0], end[1][0], grid.shape[1])

	A = make_adjacency_matrix(grid)

	graph = csr_matrix(A)

	dist_matrix, predecessors = shortest_path(csgraph=graph, directed=True, indices=start_nn, return_predecessors=True)

	print(end_nn)
	current = end_nn
	while current != start_nn:
		print(predecessors[current])
		current = predecessors[current]

	print(dist_matrix[end_nn])


def part2():
	# shortest path among all starting points where elevation is "a"

	grid = read_input()

	# get y-dim of grid
	N = grid.shape[1]

	# handle start and end letters
	end = np.where(grid == "E")

	end_nn = node_number(end[0][0], end[1][0], N)

	# edit grid
	grid[grid == "S"] = "a"
	grid[grid == "E"] = "z"

	# make A
	A = make_adjacency_matrix(grid)

	# get all start points
	starts = np.where(grid == "a")
	start_nns = [node_number(start_node[0], start_node[1], N) for start_node in zip(starts[0], starts[1])]

	# get number of nodes
	num_nodes = len(starts[0])

	# make graph
	graph = csr_matrix(A)


	dist_matrix, predecessors = shortest_path(csgraph=graph, directed=True, indices=start_nns, return_predecessors=True)

	shortest_path_lengths = [dist_matrix[i][end_nn] for i in range(len(start_nns))]

	shortest_overall_path = sorted(shortest_path_lengths)[0]

	print(f'Overall shortest path length is {shortest_overall_path}')


if __name__ == "__main__":
	#part1()
	part2()