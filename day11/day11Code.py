from collections import deque, OrderedDict
from math import floor
from numpy import prod


def read_input():
	with open('./day11Input.txt', 'r') as f:
		data = f.readlines()

	return [x.strip() for x in data]


def parse_input():
	# parse the input into some initial conditions and constants we need
	data = read_input()

	# make some initial data structures we know we'll need
	# monkey dictionary -- keyed by monkey_number, and has properties:
	# "items" (a deque), operator (for equation new = old * operator),
	# "test" - number for "test: divisible by {test}"
	# "test_true": monkey_number to throw to if true
	# "test_false": monkey_number to throw to if false

	monkeys = OrderedDict()

	for line in data:
		pieces = line.split(':')

		if pieces[0][0:6] == "Monkey":
			# start of new monkey
			monkey_number = int(pieces[0][7])
			monkeys[monkey_number] = {}

			# also initialize a history property, storing all the items a monkey has inspected
			# each time a monkey inspects an item, this is appended to
			monkeys[monkey_number]["history"] = []

		elif pieces[0] == "Starting items":
			# starting items queue
			items = [int(y.strip()) for y in [x for x in line.split(':')][1].split(',')]

			monkeys[monkey_number]["items"] = deque(items)

		elif pieces[0] == "Operation":
			# operator and operator number
			operator = pieces[1][11]
			operator_number = pieces[1][13:]

			if operator_number == "old":
				pass
			else:
				operator_number = int(operator_number)

			monkeys[monkey_number]["operator"] = operator
			monkeys[monkey_number]["operator_number"] = operator_number

		elif pieces[0] == "Test":
			# test_num
			test_num = int(pieces[1].split(' ')[-1])
			monkeys[monkey_number]["test_num"] = test_num

		elif pieces[0] == "If true":
			# target_monkey if true
			target_monkey_true = int(pieces[1][-1])
			monkeys[monkey_number]["target_monkey_true"] = target_monkey_true

		elif pieces[0] == "If false":
			# target_monkey if false
			target_monkey_false = int(pieces[1][-1])
			monkeys[monkey_number]["target_monkey_false"] = target_monkey_false


	return monkeys


def part1():
	monkeys = parse_input()

	n = 10000

	# run the simulation
	for n in range(n):
		# do n rounds
		for monkey in monkeys.keys():
			# get current items to inspect - this is a deque, and the monkeys inspect the leftmost item first
			#items = monkeys[monkey]["items"]

			while monkeys[monkey]["items"]:
				item = monkeys[monkey]["items"].popleft()

				# add item to inspection history
				monkeys[monkey]["history"].append(item)

				# do the inspection - compute new worry level
				operator = monkeys[monkey]["operator"]
				operator_number = monkeys[monkey]["operator_number"]

				if operator_number == "old":
					operator_number = item

				if operator == "+":
					item = item + operator_number

				elif operator == "*":
					item = item * operator_number


				# modify the worry level - divide by 3 and round down to nearest integer
				item = floor(item / 3)

				# run monkey's test of worry level, and append to other monkeys' deques
				test_num = monkeys[monkey]["test_num"]
				if item % test_num == 0:
					target_monkey = monkeys[monkey]["target_monkey_true"]
				else:
					target_monkey = monkeys[monkey]["target_monkey_false"]

				monkeys[target_monkey]["items"].append(item)


			# this monkey has finished

		# 1 round has finished

	# all rounds have finished



	# identify the two most active monkeys, and multiply their activity levels together

	monkey_activity_levels = [len(monkeys[monkey]["history"]) for monkey in monkeys.keys()]
	print(monkey_activity_levels)
	monkey_business = prod(sorted(monkey_activity_levels, reverse=True)[0:2])

	print(f'The level of monkey business is {monkey_business}')




def part2():
	# in part 2, worry levels aren't divided by 3, and so 
	n=10000


	# need to find some way of computing modified worry levels that retains the same properties

	monkeys = parse_input()

	# run the simulation
	for n in range(n):
		# do n rounds
		for monkey in monkeys.keys():
			# get current items to inspect - this is a deque, and the monkeys inspect the leftmost item first
			#items = monkeys[monkey]["items"]

			while monkeys[monkey]["items"]:
				item = monkeys[monkey]["items"].popleft()

				# add item to inspection history
				monkeys[monkey]["history"].append(item)

				# do the inspection - compute new worry level
				operator = monkeys[monkey]["operator"]
				operator_number = monkeys[monkey]["operator_number"]

				if operator_number == "old":
					operator_number = item

				if operator == "+":
					item = item + operator_number

				elif operator == "*":
					item = item * operator_number

				# what if we mod the worry level by the product of all test numbers? - this preserves the relative properties
				# of whether the number is divisible by any of the individual numbers, while ensuring the worry level is bounded

				item = item % prod([props["test_num"] for props in monkeys.values()])

				# run monkey's test of worry level, and append to other monkeys' deques
				test_num = monkeys[monkey]["test_num"]
				if item % test_num == 0:
					target_monkey = monkeys[monkey]["target_monkey_true"]
				else:
					target_monkey = monkeys[monkey]["target_monkey_false"]

				monkeys[target_monkey]["items"].append(item)



	monkey_activity_levels = [len(monkeys[monkey]["history"]) for monkey in monkeys.keys()]
	print(monkey_activity_levels)
	monkey_business = prod(sorted(monkey_activity_levels, reverse=True)[0:2])

	print(f'The level of monkey business is {monkey_business}')


if __name__ == "__main__":
	part1()
	part2()