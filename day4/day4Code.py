




def read_input():
	with open('./day4Input.txt', 'r') as f:
		data = f.readlines()

	ranges = []

	for row in data:
		first, second = row.strip().split(',')

		first_low, first_high = first.split('-')
		second_low, second_high = second.split('-')

		first_range = range(int(first_low), int(first_high)+1)
		second_range = range(int(second_low), int(second_high)+1)

		ranges.append([first_range, second_range])

	return ranges



def part1():
	ranges = read_input()

	# for each pair of ranges, check if either range wholly contains the other
	contains_count = 0

	for first_range, second_range in ranges:
		if set(first_range).issubset(set(second_range)) or set(second_range).issubset(set(first_range)):
			# one of the ranges is a subset of the other
			contains_count += 1

	print(f"The number of assignment pairs where one range fully contains the other is {contains_count}")


def part2():
	#count all overlaps

	ranges = read_input()

	overlaps_count = 0

	for first_range, second_range in ranges:
		if not set(first_range).isdisjoint(set(second_range)):
			overlaps_count += 1

	print(f"The number of overlapping pairs is {overlaps_count}")



if __name__ == "__main__":
	part1()
	part2()