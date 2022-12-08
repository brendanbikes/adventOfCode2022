


def read_input():
	with open('./day8Input.txt', 'r') as f:
		data = f.readlines()

	# build grid as a list of lists so it's queryable as grid[i][j] where i is row, j is col

	grid = []
	for row in data:
		row = row.strip()
		nums = [int(x) for x in row]
		grid.append(nums)

	return grid



def part1():
	# count visible trees
	# a tree is visible if no other tree between it and the edge is taller
	# trees on the edge -- i=0, j=0, i=max, j=max -- are visible
	# so only need to test trees where i in (1,max-1), j in (1, max-1)


	grid = read_input()

	#grid size
	N = len(grid[0])
	M = len(grid)

	# initialize visible trees as all the trees on the edge - top row, bottom row, left side minus 2, and right side minus 2
	# (to avoid double counting at the corners)

	visible_trees = 2*N + 2*M - 4


	for i in range(1,M-1):
		for j in range(1,N-1):
			height = grid[i][j]
			# test if tree at i,j is visible in at least 1 cardinal direction
			# get each group of neighbors and test height
			left_neighbors = grid[i][0:j]
			right_neighbors = grid[i][j+1:]
			top_neighbors = [grid[x][j] for x in range(0,i)]
			bottom_neighbors = [grid[x][j] for x in range(i+1,M)]

			if max(left_neighbors) < height or max(right_neighbors) < height or max(top_neighbors) < height or max(bottom_neighbors) < height:
				# tree is visible
				visible_trees+=1

	print(f'The count of visible trees is {visible_trees}')


	# count number of trees visible from each tree in each direction, multiply those, and find the max

	visibility_scores = {}

	for i in range(0,M):
		for j in range(0,N):
			height = grid[i][j]
			visibility_score = 1

			# get neighbors, and tally up how many are visible -- count until you reach one that's at least as tall
			# we do have to consider trees on the edge -- the loop ranges are expanded
			# also, these groups are defined as lists radiating out from i,j
			left_neighbors = list(grid[i][0:j])[::-1]
			right_neighbors = grid[i][j+1:]
			top_neighbors = list(grid[x][j] for x in range(0,i))[::-1]
			bottom_neighbors = [grid[x][j] for x in range(i+1,M)]

			#breakpoint()


			for group in [left_neighbors, right_neighbors, top_neighbors, bottom_neighbors]:
				if group:
					# account for possibility of no neighbors in a direction -- on edge of grid
					visible_trees = 0
					for tree in group:
						# tree is guaranteed to be visible, if we didn't break the loop on the last one
						visible_trees += 1
						
						if tree >= height:
							# tree too tall to continue -- break out of this loop to continue the outer loop
							break

				else:
					# no neighbors in 1 direction -- edge
					visible_trees = 0

				# update score
				visibility_score *= visible_trees

			#breakpoint()
							

			# file the tree visibility
			visibility_scores[(i,j)] = visibility_score

	max_vis_score = max(visibility_scores.values())
	print(f'Maximum visibility score is {max_vis_score}')



if __name__ == "__main__":
	part1()