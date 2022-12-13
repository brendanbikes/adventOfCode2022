import ast

def read_input():
	with open('./day13Input.txt', 'r') as f:
		data = f.readlines()


	return [ast.literal_eval(x) for x in data if len(x) > 1]


def compare_lists(left, right):
	# compare 2 lists to determine if they are in correct order

	i = 0
	while True:
		# iterate through list values
		try:

			if isinstance(left[i], int) and isinstance(right[i], int):
				# both are integers
				if left[i] < right[i]:
					# proper arrangement
					return True
				elif left[i] > right[i]:
					# improper arrangement
					return False
				else:
					# left[i] == right[i], need to continue checking
					pass


			elif isinstance(left[i], list) and isinstance(right[i], list):
				# both are lists
				order_tf = compare_lists(left[i], right[i])
				if order_tf is not None:
					return order_tf

			elif isinstance(left[i], list) and isinstance(right[i], int):
				# left is list, right is int
				# make right into a list, and compare lists
				order_tf = compare_lists(left[i], [right[i]])
				if order_tf is not None:
					return order_tf


			elif isinstance(left[i], int) and isinstance(right[i], list):
				# left is int, right is list
				# make left a list
				order_tf = compare_lists([left[i]], right[i])
				if order_tf is not None:
					return order_tf


		except IndexError as e:
			# one of the lists ran out of items -- determine which one
			if len(left) < len(right):
				return True
			elif len(left) > len(right):
				return False
			else:
				# len(left) == len(right)
				return None

		# increment
		i+=1


def part1():

	data = read_input()

	# for each pair of packets, compare first (left) to second (right)

	# array for true/false values for pairs
	pairs = []

	for i in range(int(len(data)/2)):
		# first packet is 2*i
		# second packet is 2*i + 1

		left = data[2*i]
		right = data[2*i+1]

		order_tf = compare_lists(left, right)
		pairs.append(order_tf)


	print(sum([z+1 for z in range(len(pairs)) if pairs[z]]))


def part2():
	# sort all the packets, including 2 additional divider packets
	# then find the indices of the divider packets
	# this is basically tailor-made for bubble sort

	data = read_input()

	# add the divider packets
	first_divider = [[2]]
	second_divider  = [[6]]
	data.append(first_divider)
	data.append(second_divider)


	# initialize
	n_swaps = 1

	# as long as at least 1 swap was performed last round, need to do another sweep
	while n_swaps > 0:
		# reset swaps each round
		n_swaps = 0

		for i in range(len(data)-1):
			left = data[i]
			right = data[i+1]

			order_tf = compare_lists(left, right)

			if not order_tf:
				#swap the positions of left and right in data
				data[i] = right
				data[i+1] = left

				n_swaps += 1

	# find indices of divider packets
	first_ind = data.index(first_divider) + 1
	second_ind = data.index(second_divider) + 1

	# get result
	print(first_ind * second_ind)



if __name__ == "__main__":
	part1()
	part2()