

# make a dictionary of stacks/lists because the input format sucks
stacks = {
	1: ['S', 'L', 'W'],
	2: ['J', 'T', 'N', 'Q'],
	3: ['S', 'C', 'H', 'F', 'J'],
	4: ['T', 'R', 'M', 'W', 'N', 'G', 'B'],
	5: ['T', 'R', 'L', 'S', 'D', 'H', 'Q', 'B'],
	6: ['M', 'J', 'B', 'V', 'F', 'H', 'R', 'L'],
	7: ['D', 'W', 'R', 'N', 'J', 'M'],
	8: ['B', 'Z', 'T', 'F', 'H', 'N', 'D', 'J'],
	9: ['H', 'L', 'Q', 'N', 'B', 'F', 'T']
}


def read_input():
	with open('./day5Input.txt', 'r') as f:
		data = f.readlines()


	instructions = []

	for row in data:
		if row[0] != 'm':
			# not an instruction
			continue
		else:
			# instruction
			instructions.append(row.strip())

	return instructions


def parse_instruction(instruction):
	instruction = instruction.replace('move ', '').replace('from ', '').replace('to ', '').split(' ')
	return [int(x) for x in instruction]


def operate(stacks, f, t):
	# move 1 box from FROM stack to TO stack

	stacks[t] = stacks[t] + [stacks[f][-1]]
	stacks[f] = stacks[f][0:-1]

	return stacks


def operate_part2(stacks, n, f, t):
	# move n boxes from FROM stack to TO stack

	stacks[t] = stacks[t] + stacks[f][-n:]
	stacks[f] = stacks[f][0:len(stacks[f])-n]

	return stacks

def print_message(stacks):
	# get the top crates in each stack
	msg = ''
	for i in range(len(stacks)):
		msg += stacks[i+1][-1]


	print(msg)


def part1(stacks):
	instructions = read_input()

	for instruction in instructions:
		n, f, t = parse_instruction(instruction)

		# f = number of operations
		# f = from stack
		# t = to stack

		#instruction is of form [a, b, c] where a,b,c are ints
		# move a units from stack b to stack c

		for i in range(n):
			stacks = operate(stacks, f, t)


	print_message(stacks)


def part2(stacks):
	# different operator -- crates moved in multiples
	instructions = read_input()

	for instruction in instructions:
		n, f, t = parse_instruction(instruction)

		stacks = operate_part2(stacks, n, f, t)


	print_message(stacks)


if __name__ == "__main__":
	part1(stacks.copy())
	part2(stacks.copy())