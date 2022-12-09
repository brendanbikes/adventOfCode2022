


def read_input():
	with open('./day9Input.txt', 'r') as f:
		data = f.readlines()

	return [x.split(' ') for x in data]



def is_adjacent(head, tail):
	# tests whether 2 position tuples (x,y), (p,q) are adjacent
	# 2 points are adjacent if abs(x-p) <= 1 and abs(y-q) <= 1 (i.e. only ever at most 1 position away, in either/both directions)

	if abs(head['x']-tail['x']) <= 1 and abs(head['y']-tail['y']) <= 1:
		return True
	else:
		return False



def move_tail(head, tail, tail_positions):
	if head == tail:
		# skip - they are already superimposed
		return tail

	elif head['x'] == tail['x']:
		# head and tail in a vertical line
		tail, tail_positions = move_tail_vert(head, tail, tail_positions)

	elif head['y'] == tail['y']:
		# head and tail in horizontal line
		tail, tail_positions = move_tail_horiz(head, tail, tail_positions)

	elif abs(head['x']-tail['x']) == 2 and abs(head['y']-tail['y']) == 2:
		# new movement -- move tail closer by 1 in both directions
		tail, junk = move_tail_vert(head, tail, set())
		tail, junk = move_tail_horiz(head, tail, set())

	else:
		print(head, tail)
		# head and tail diagonal - do 2-part movement
		# this shouldn't get stuck in a loop, because the move_tail_diag realigns head and tail in a line
		tail, tail_positions = move_tail_diag(head, tail, tail_positions)
		tail, tail_positions = move_tail(head, tail, tail_positions)

	return tail, tail_positions


def move_tail_diag(head, tail, tail_positions):
	# first part of diagonal movement to realign
	if abs(head['x'] - tail['x']) == 1:
		# only difference of 1 in the x-direction, and difference of 2 in the y-direction
		# so set x-coord of tail to that of the head, and move the tail 1 closer in the y-direction as we did above
		tail['x'] = head['x']

	elif abs(head['y'] - tail['y']) == 1:
		tail['y'] = head['y']

	return tail, tail_positions


def move_tail_vert(head, tail, tail_positions):
	# head and tail are in a vertical line (x coords the same) -- move the tail 1 closer on the y axis
	if tail['y'] < head['y']:
		# head above tail
		tail['y'] += 1

	elif tail['y'] > head['y']:
		# tail above head
		tail['y'] -= 1

	tail_positions.add((tail['x'], tail['y']))

	return tail, tail_positions


def move_tail_horiz(head, tail, tail_positions):
	# head and tail are in horizontal line (y coords the same) -- move taile 1 closer on the x axis
	if tail['x'] < head['x']:
		# head to the right of tail
		tail['x'] += 1

	elif tail['x'] > head['x']:
		# head to the left of tail
		tail['x'] -= 1

	tail_positions.add((tail['x'], tail['y']))

	return tail, tail_positions
		



def part1():
	# follow instructions and count the # of (i,j) positions the tail visited at least once -- keep a set

	commands = read_input()

	# initialize starting positions
	head = {'x': 0, 'y': 0}
	tail = {'x': 0, 'y': 0}

	tail_positions = set()
	tail_positions.add((tail['x'], tail['y']))

	for direction, num in commands:
		for i in range(int(num)):
			# repeat this command num times

			# move head
			if direction == "R":
				# move right 1
				head['x'] += 1

			elif direction == "L":
				# move left 1
				head['x'] -= 1

			elif direction == "U":
				# move up 1
				head['y'] += 1

			elif direction == "D":
				# move down 1
				head['y'] -= 1


			# test for adjacency
			if is_adjacent(head, tail):
				# adjacent -- don't need to move tail
				pass

			else:
				# not adjacent -- need to move tail according to head position
				tail, tail_positions = move_tail(head, tail, tail_positions)

			print(f'\nhead position: {head}')
			print(f'tail position: {tail}')


	# count number of positions the tail visited
	print(f'The number of visited positions is {len(tail_positions)}')


def part2():
	# simulate a rope with n nodes
	commands = read_input()

	n = 10

	# initialize starting positions
	positions = {i: {'x': 0, 'y': 0} for i in range(n)}


	tail_positions = set()
	tail_positions.add((positions[0]['x'], positions[0]['y']))


	# for each command, it needs to propagate down the chain
	# i.e. at first the "head" and "tail" are nodes 0 and 1,
	# but then they are nodes 1 and 2, then 2 and 3, etc.

	for direction, num in commands:
		print(direction, num)
		for i in range(int(num)):
			# repeat this command num times

			# move head
			if direction == "R":
				# move right 1
				positions[9]['x'] += 1

			elif direction == "L":
				# move left 1
				positions[9]['x'] -= 1

			elif direction == "U":
				# move up 1
				positions[9]['y'] += 1

			elif direction == "D":
				# move down 1
				positions[9]['y'] -= 1


			# now deal with chaining - there are N-1 pairs of nodes to deal with
			for j in range(n-1,0,-1):
				print(j)
				print(positions)
				head = positions[j]
				tail = positions[j-1]

				# test for adjacency
				if is_adjacent(head, tail):
					pass

				else:
					tail, junk = move_tail(head, tail, set())

				# update positions dict
				positions[j-1] = tail

			# once we've dealt with all pairs of nodes, the position of the tail can be logged
			tail_positions.add((positions[0]['x'], positions[0]['y']))

	print(f'The number of visited positions is {len(tail_positions)}')


if __name__ == "__main__":
	#part1()
	part2()
