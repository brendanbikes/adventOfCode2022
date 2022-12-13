import numpy as np
from string import ascii_lowercase

def read_input():
	with open('./day12Input.txt', 'r') as f:
		data = f.readlines()

	data = [x.strip() for x in data]

	array = []

	for row in data:
		array.append([x for x in row])

	return np.array(array)


def recur(grid, end, paths=[], current_path=[], shortest_path_length=None):
	# take in a grid, and recursively traverse it exhaustively from start to end, finding all paths

	if shortest_path_length and len(current_path) > shortest_path_length:
		# not worth pursuing -- toss it out
		return paths, shortest_path_length

	# get neighbor candidates for the current node
	current = current_path[-1]
	neighbors = get_candidates(grid=grid, current_path=current_path)

	if current == end:
		# hooray! we've reached the end -- return the path, and update shortest_path_length
		paths.append(current_path)
		shortest_path_length = len(current_path)

		return paths, shortest_path_length

	for neighbor in neighbors:
		paths, shortest_path_length = recur(grid=grid, end=end, paths=paths, current_path=current_path + [neighbor], shortest_path_length=shortest_path_length)

	# if code reaches here, i.e. no candidate neighbors, we've reached a dead end
	# since no loops are allowed; just return paths without filing the current path
	return paths, shortest_path_length


def get_candidates(grid, current_path):
	# get the candidate next (i,j) tuples for advancing
	# doesn't allow going backwards

	# extract current node
	current = current_path[-1]
	current_height = grid[current[0]][current[1]]

	# if we are at the start, current height is a
	if current_height == "S":
		current_height = "a"

	# get index of current height in letter string
	ind = ascii_lowercase.find(current_height)

	# find valid height values for current position
	valid_heights = ascii_lowercase[:ind+2] # can go many steps down, but only 1 up

	# construct neighbors
	i = current[0] # row position
	j = current[1] # column position
	left_neighbor = (i, j-1)
	right_neighbor = (i, j+1)
	top_neighbor = (i-1, j)
	bottom_neighbor = (i+1, j)

	neighbors = [left_neighbor, right_neighbor, top_neighbor, bottom_neighbor]

	# the conditions here are a little funky, to filter out cases where the i,j indices are beyond the range of the grid
	filtered = []
	for neighbor in neighbors:
		if neighbor[0] in range(0, grid.shape[0]) and neighbor[1] in range(0, grid.shape[1]):
			# not outside of bounds -- do this first so we don't get IndexError later
			if neighbor not in current_path:
				# not in current path
				# get neighbor height
				neighbor_height = grid[neighbor[0]][neighbor[1]]
				neighbor_height = "z" if neighbor_height == "E" else neighbor_height

				if neighbor_height in valid_heights:
					# candidate is not too high
					# if all these checks pass, neighbor is valid candidate
					filtered.append(neighbor)

	return filtered


def part1():
	grid = read_input()

	# find index of start position
	x = np.where(grid == "S")
	start = (x[0][0], x[1][0])

	# find index of terminus
	x = np.where(grid == "E")
	end = (x[0][0], x[1][0])

	paths, shortest_path_length = recur(grid=grid, end=end, current_path=[start])

	# find the shortest path
	#shortest_path_length = sorted([len(path) for path in paths])[0]

	# minus 1 here, because it's the # of steps, not # of points visited
	print(f'The length of the shortest path is {shortest_path_length-1}')


if __name__ == "__main__":
	part1()