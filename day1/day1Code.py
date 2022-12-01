def read_input():
	with open('./day1Input.txt', 'r') as f:
		data = f.readlines()

	return [x.strip() for x in data]


def process_input():
	# process input to a dictionary, and then just return a sorted array of calorie values
	data = read_input()

	elf_calories = {}

	elf_counter = 1 # start counting at 1
	for line in data:
		if line == '':
			# divider line -- increment elf_counter to next elf
			elf_counter += 1
		else:
			# line has some data for the current elf
			
			if elf_counter not in elf_calories:
				# initialize calorie count for this elf if it hasn't been set yet
				elf_calories[elf_counter] = int(line)
			else:
				# add calories to count for current elf
				elf_calories[elf_counter] += int(line)

	calories_sorted = sorted(elf_calories.values(), reverse = True)

	return calories_sorted


def part1and2():
	# compute total calories per elf and save in a dictionary

	calories_sorted = process_input()

	# max is just the first element
	max_calories = calories_sorted[0]

	#for elf_index, calories in elf_calories.items():
	#	if calories == max_calories:
	#		print(f"Elf {elf_index} has the most calories with {calories} calories")


	# or do it faster and just print the max, since the puzzle doesn't care about the index
	print(f"Elf carrying the most calories has {max_calories} calories")

	# do part 2 here to avoid sorting again - sum elements 0, 1, 2
	sum_top_3 = sum(calories_sorted[0:3])
	print(f"Top 3 elf payloads sum to {sum_top_3} calories")



if __name__ == "__main__":
	part1and2()