from itertools import zip_longest
from math import ceil

def read_input():
	with open('./day14Input.txt', 'r') as f:
		data = f.readlines()


	# parse the input into a list of lists, with each sub-list containing points as tuples

	parsed = []
	for row in data:
		row = row.split(' -> ')
		parsed.append([tuple([int(y) for y in x.split(',')]) for x in row])


	return parsed


def make_grid_part1(data):
	# from the input line segments, create a grid/matrix object to use for simulating the sand
	# grid will be a dictionary, keyed on (i, j) where (0,0) is the at the left and top


	grid = {}

	for row in data:
		# list of points
		n = len(row) # number of points
		# if there are n points, then there are n-1 line segments to produce
		# iterate through with point1 = row[i], and point2 = row[i+1]

		for i in range(n-1):
			point1 = row[i]
			point2 = row[i+1]

			# draw a line segment from point1 to point2, inclusive of the endpoints

			# get x-coords and y-coords
			xcoords = [x for x in range(min(point1[0], point2[0]), max(point1[0], point2[0]) + 1)]
			ycoords = [y for y in range(min(point1[1], point2[1]), max(point1[1], point2[1]) + 1)]

			# make list of points in the line
			fill_value = xcoords[0] if len(xcoords)==1 else ycoords[0] #identify which direction is static
			line_points = [z for z in zip_longest(xcoords, ycoords, fillvalue=fill_value)]


			# file the points in the grid -- but in (row, column) format
			for line_point in line_points:
				grid[(line_point[1], line_point[0])] = "#"

	# fill in the rest of the grid, just to help when figuring out if sand is falling off the grid
	# get grid size
	mini = min([point[0] for point in grid.keys()])
	maxi = max([point[0] for point in grid.keys()])
	minj = min([point[1] for point in grid.keys()])
	maxj = max([point[1] for point in grid.keys()])


	for i in range(0, maxi+1):
		for j in range(minj, maxj+1):
			if not grid.get((i,j), None):
				grid[(i,j)] = '.'

	return grid


def make_grid_part2(data):
	# from the input line segments, create a grid/matrix object to use for simulating the sand
	# grid will be a dictionary, keyed on (i, j) where (0,0) is the at the left and top


	grid = {}

	for row in data:
		# list of points
		n = len(row) # number of points
		# if there are n points, then there are n-1 line segments to produce
		# iterate through with point1 = row[i], and point2 = row[i+1]

		for i in range(n-1):
			point1 = row[i]
			point2 = row[i+1]

			# draw a line segment from point1 to point2, inclusive of the endpoints

			# get x-coords and y-coords
			xcoords = [x for x in range(min(point1[0], point2[0]), max(point1[0], point2[0]) + 1)]
			ycoords = [y for y in range(min(point1[1], point2[1]), max(point1[1], point2[1]) + 1)]

			# make list of points in the line
			fill_value = xcoords[0] if len(xcoords)==1 else ycoords[0] #identify which direction is static
			line_points = [z for z in zip_longest(xcoords, ycoords, fillvalue=fill_value)]


			# file the points in the grid -- but in (row, column) format
			for line_point in line_points:
				grid[(line_point[1], line_point[0])] = "#"


	# add the "infinite" floor to the grid
	# find highest i coord
	floor_depth = max([x[0] for x in grid.keys()]) + 2

	# bounds
	minj = min([x[1] for x in grid.keys()])
	maxj = max([x[1] for x in grid.keys()])

	# how far out to go in each direction from min and max j coords
	# have to go at least the floor depth out from the center of the pile
	# because 1:1 ratio of length/height in the pyramid, so if we go floor_depth
	# out from the edge of the pile, we'll be just fine
	N = floor_depth

	# add floor
	for k in range(minj - N, maxj + N):
		grid[(floor_depth, k)] = "#"



	# fill in the rest of the grid, just to help when figuring out if sand is falling off the grid
	# get grid size
	mini = min([point[0] for point in grid.keys()])
	maxi = max([point[0] for point in grid.keys()])
	minj = min([point[1] for point in grid.keys()])
	maxj = max([point[1] for point in grid.keys()])


	for i in range(0, maxi+1):
		for j in range(minj, maxj+1):
			if not grid.get((i,j), None):
				grid[(i,j)] = '.'


	return grid


def get_next(grid, current):
	# get the next position

	if grid.get((current[0]+1, current[1]), '') == '.':
		# available position
		next = (current[0]+1, current[1])

	elif grid.get((current[0]+1, current[1]), '') in ['o', '#']:
		# directly below is occupied

		if grid.get((current[0]+1, current[1]-1), '') == '.':
			# can move down and left
			next = (current[0]+1, current[1]-1)

		elif grid.get((current[0]+1, current[1]+1), '') == '.':
			# can move down and right
			next = (current[0]+1, current[1]+1)

		elif not grid.get((current[0]+1, current[1]-1), ''):
			# movement would be off grid
			next = None

		elif not grid.get((current[0]+1, current[1]+1), ''):
			# movement would be off grid
			next = None

		else:
			# if get to here, then bottom and both diagonals are not available, and neither diagonals are out of bounds
			# so the sand settles at current
			next = current

			return next


	elif not grid.get((current[0]+1, current[1]), ''):
		# directly below is off-grid
		next = None

	if next:
		# recursively get next position
		next = get_next(grid=grid, current=next)

	return next


def evolve(grid, current):
	# evolve a unit of sand

	# recursively move the sand through the grid
	final = get_next(grid, current)

	if final:
		# sand had a final resting spot -- put it in the grid
		grid[final] = 'o'

	return grid


def simulate_sand(grid, start=(0,500)):

	while True:

		#print(len([v for v in grid.values() if v == 'o']))

		newgrid = evolve(grid=grid.copy(), current=start)

		# test for souce blocked -- part 2:
		if newgrid[start] == 'o':
			# source is blocked
			return newgrid

		# otherwise, keep going

		# test for similarity -- part 1
		if newgrid == grid.copy():
			# we got back the same grid
			return newgrid

		else:
			# set grid to newgrid and continue
			grid = newgrid.copy()


def part1():

	data = read_input()

	grid = make_grid_part1(data)

	grid = simulate_sand(grid=grid)

	# print number of sand units
	print(f"\nThe number of sand units in the grid is {len([x for x in grid.values() if x == 'o'])}")


def part2():
	# there is a floor
	# j coordinate = 2 + highest j coordinate of any point in the grid
	# accumulate sand on the floor, and simulate until the starting point becomes blocked

	data = read_input()
	grid = make_grid_part2(data)

	# now run simulation
	grid = simulate_sand(grid=grid)

	#analyze_grid(grid=grid)

	print(f"\nThe number of sand units in the grid is {len([x for x in grid.values() if x == 'o'])}")


if __name__ == "__main__":
	#part1()
	part2()