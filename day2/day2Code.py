
scores_lookup = {
	"X": 1,
	"Y": 2,
	"Z": 3,
}

key_beats_value = {
	"A": "Z",
	"B": "X",
	"C": "Y",
	"X": "C",
	"Y": "A",
	"Z": "B",
}

key_loses_to_value = {v:k for k,v in key_beats_value.items()}

equivalents = {
	"A": "X",
	"B": "Y",
	"C": "Z"
}


def read_input():
	with open('./day2Input.txt', 'r') as f:
		data = f.readlines()

	# split to tuples
	return [tuple(x.strip().split(' ')) for x in data]



def part1():
	data = read_input()

	score = 0
	for p1, p2 in data:
		# increment score by what p2 played
		score += scores_lookup[p2]

		# test for win condition
		if p1 == key_beats_value[p2]:
			# p2 wins because p1 played what is beaten by p2
			score += 6

		# test for draw condition
		elif p2 == equivalents[p1]:
			# this is a draw
			score += 3

	print(f"Final score is {score}")


def part2():
	# X = need to lose, Y = need to draw, Z = need to win

	data = read_input()

	score = 0
	for p1, p2 in data:
		
		if p2 == 'X':
			# this must be a loss -- just add the value of whatever loses to p1's play
			score += scores_lookup[key_beats_value[p1]]

		elif p2 == 'Y':
			# this must be a draw -- add the value of p1's play (since it's the same as p2's play) + 3 for the draw
			score += (scores_lookup[equivalents[p1]] + 3)

		elif p2 == 'Z':
			# this must be a win -- add value of whatever beats p1's play + 6 for the win
			score += (scores_lookup[key_loses_to_value[p1]] + 6)

	print(f"Final score is {score}")



if __name__ == "__main__":
	part1()
	part2()