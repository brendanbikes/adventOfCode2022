from string import ascii_lowercase, ascii_uppercase


lookup = ascii_lowercase + ascii_uppercase

def read_input():
	with open('./day3Input.txt', 'r') as f:
		data = f.readlines()

	# split to lists of individual characters
	return [[*x.strip()] for x in data]



def part1():

	data = read_input()

	priority_sum = 0

	for sack in data:
		print(sack)
		#split sack in half
		n = len(sack)

		first = set(sack[0:int(n/2)])
		second = set(sack[int(n/2):])

		#find the intersection of the two - should be only 1 item
		common = list(first.intersection(second))[0]

		#find the priority based on which position in the lookup string corresponds to the common letter -- +1, since priority starts at 1
		priority = lookup.find(common) + 1

		priority_sum += priority

	print(f"The priority sum is {priority_sum}")


def part2():
	# groups of 3

	data = read_input()

	N = len(data)

	priority_sum = 0
	for i in range(0,int(N/3)):

		first = set(data[3*i])
		second = set(data[3*i+1])
		third = set(data[3*i+2])

		common = list(first.intersection(second).intersection(third))[0]

		priority = lookup.find(common) + 1

		priority_sum += priority

	print(f"The priority sum is {priority_sum}")


if __name__ == "__main__":
	part1()
	part2()