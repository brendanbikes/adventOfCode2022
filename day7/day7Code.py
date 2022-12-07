

def read_input():
	with open('./day7Input.txt', 'r') as f:
		data = f.readlines()

	return [x.strip() for x in data]


def recur(folders, parent, commands, command_start_index):
	command_index = command_start_index

	while command_index < len(commands):
		command = commands[command_index]
		# increment the current command index in case we need to recur
		command_index += 1
		
		# process the command
		if command[0] == "$":
			# this is an executed command
			if command[2:4] == "cd":
				# change directory code goes here -- this is where we recur (go down) or return (go up)

				if command.split(' ')[2] == '..':
					# return up 1 level -- but the current parent's file size needs to be added to the grandparent's file size upon return
					return folders, command_index, folders[parent]

				elif command.split(' ')[2] == '/':
					# special case -- we already started the process in the root folder, so this is meaningless -- skip it, after initializing root folder's current size
					folders[parent] = 0
					continue
				
				else:
					# recur down
					folder = command.split(' ')[2]
					path = '/'.join([parent, folder]) # make a full-path key to feed to parent
					folders, command_index, child_size = recur(folders=folders, parent=path, commands=commands, command_start_index = command_index)

					# upon emerge from the next level down, the total size of the stuff contained below needs to be returned up and added to the parent folder
					folders[parent] += child_size

		elif command[0:3] == "dir":
			# directory -- add it to the folders dictionary with size 0, since no files have been assigned to it yet
			folder = command.split(' ')[1]
			path = '/'.join([parent, folder]) # make a full-path key to feed to parent

			if folder not in folders.keys():
				folders[path] = 0

			else:
				# a folder is being listed again -- pass
				pass

		else:
			# only other possibility is that the first part of the output is numeric, giving the size of a file
			# so add the size of this file to the size attribute of the current parent directory
			file_size = command.split(' ')[0]
			folders[parent] += int(file_size)

	return folders, command_index, folders[parent]



def part1and2():
	data = read_input()


	# make a recursive function that walks the directories
	# when it reaches a directory that only contains files (i.e. a dead-end),
	# it returns with the total size of the contained files, indexed in a dictionary
	# keyed on the containing directory
	# the dictionary of {folder: size} is passed around, and each time a "dir blah"
	# command output is seen, that folder is added to the dictionary
	# we also need to keep track of where we are in the code as we go deeper

	folders = {}

	folders, command_index, child_size = recur(folders=folders, parent="root", commands=data, command_start_index=0)

	# total size of all folders of at least 100,000 in size
	print("Total size of dirs of at least 100,000: {}".format(sum([val for key, val in folders.items() if val <= 100000])))

	# find smallest directory possible to free up enough space to leave at least 30000000 of 70000000 empty
	total_space = 70000000
	desired_freespace = 30000000
	used_space = folders["root"]

	candidate = sorted([x for x in folders.values() if total_space - (used_space - x) >= desired_freespace])[0]
	print(f'Size of candidate directory for deletion: {candidate}')


if __name__ == "__main__":
	part1and2()