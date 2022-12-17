from operator import itemgetter

def read_input():
	with open('./day15Input.txt', 'r') as f:
		data = f.readlines()


	coords = []

	for line in data:
		sensor, beacon = line.strip().split(":")

		sensor = sensor.strip().replace('Sensor at ', '')
		sensor_x, sensor_y = sensor.split(',')

		sensor_x = int(sensor_x.strip()[2:])
		sensor_y = int(sensor_y.strip()[2:])

		beacon = beacon.strip().replace('closest beacon is at ', '')
		beacon_x, beacon_y = beacon.split(',')

		beacon_x = int(beacon_x.strip()[2:])
		beacon_y = int(beacon_y.strip()[2:])

		coords.append([(sensor_x, sensor_y), (beacon_x, beacon_y)])


	distances = {}
	areas = {}

	sensors=[]
	beacons=[]

	for pair in coords:
		sensor, beacon = pair

		sensors.append(sensor)
		beacons.append(beacon)

		distance = manhattan_distance(beacon, sensor)
		distances[sensor] = distance

		# determine the area we should monitor -- for each sensor, get its xmin, xmax, ymin, ymax as
		# sensor position +/- its manhattan distance to closest beacon
		# each area is [xmin, xmax, ymin, ymax]
		areas[pair[0]] = [pair[0][0]-distance, pair[0][0] + distance, pair[0][1] - distance, pair[0][1] + distance]


	return sensors, beacons, distances


def manhattan_distance(point1, point2):
	return abs(point2[0]-point1[0]) + abs(point2[1]-point1[1])


def part1():
	sensors, beacons, distances = read_input()

	# for each row, determine whether each point is within the characteristic Manhattan distance of each of the sensors
	# if it is for at least 1 sensor, then a beacon cannot be positioned there
	# otherwise, a beacon could be there (but we don't know)

	# determine overall area to consider
	global_xmin = min([t[0] for t in areas.values()])
	global_xmax = max([t[1] for t in areas.values()])
	global_ymin = min([t[2] for t in areas.values()])
	global_ymax = max([t[3] for t in areas.values()])

	# now for a given row, consider the points in range(xmin, xmax+1) and compute whether it is within the Manhattan distance of at least 1 point

	M = 2000000
	#M = 10
	count=0

	print(len([(t, M) for t in range(global_xmin, global_xmax+1) if sum([1 if manhattan_distance((t,M), sensor) <= distances[sensor] else 0 for sensor in sensors]) >= 1 and (t,M) not in beacons]))


def compute_row_coverage(row, sensors, distances):
	# compute the coverage of a single row -- row is an int, sensors is list of sensor positions, and distances is dict of manhattan distances per sensor

	# create the list of coverage tuples
	coverage_tuples = []

	for sensor in sensors:
		d = abs(row - sensor[1]) # distance between row and sensor -- if 0, we're in its row
		ds = distances[sensor]
		if d > ds:
			# not close enough -- this sensor doesn't contribute anything to coverage
			continue
		else:
			# this sensor contributes coverage - compute it
			coverage = tuple([sensor[0] - (ds-d), sensor[0] + (ds-d)])
			coverage_tuples.append(coverage)

	# sort the coverage_tuples by tuple[0]
	coverage_tuples = sorted(coverage_tuples, key=itemgetter(0))

	# resolve the tuples to determine if full coverage from min to max or not
	# initialize the two indexes tracking which tuples we are comparing
	i=0
	j=1

	while True:
		try:
			first = coverage_tuples[i]
			second = coverage_tuples[j]

			if second[0]<=first[1] and second[1]<=first[1]:
				# second is subset of first -- increment j and do next comparison
				j+=1
				continue

			elif second[0] <= first[1]:
				# the two elements overlap -- no gap in coverage
				# set i to j, and set j to j+1
				i=j
				j+=1

			else:
				# no overlap -- there is a gap!
				return False, first[1]+1

		except IndexError:
			# finished the row
			break

	# if get here, we scanned the whole row and found no gap
	return True, None


def part2(minrow=0, maxrow=20):
	# find the hole in the coverage

	# for each row, get the list of ranges for each sensor. For example, if sensor is located at (5,5) and has characteristic Manhattan distance 3,
	# and we want to look at row 5, then the range of coverage for this sensor in row 5 is [2, 3, 4, 5, 6, 7, 8] or range(5-3, 5+3+1)
	# and actually to avoid using iterators, we don't need the range -- just tuple(2, 8) describing the endpoints
	# to look at another row, e.g. row 8, which is abs(8-5) = 3 distance away, then the coverage positions within row 8 become (5-(3-3), 5+(3-3)) or (5, 5)
	# indicating that since the entire Manhattan characteristic distance was spent getting to row 8, there is no horizontal expansion of coverage

	# if row is not within the Manhattan distance for a given sensor, then don't compute its coverage

	sensors, beacons, distances = read_input()

	for i in range(minrow, maxrow):
		row_covered, index = compute_row_coverage(i, sensors, distances)

		if not row_covered:
			# found the row with the hole in it
			break


	print(f'Position of hole with beacon is {index, i} and the frequency is {4000000*index + i}')


if __name__ == "__main__":
	#part1()
	part2(maxrow=4000000)