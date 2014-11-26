# import ability to get and use command line arguments
from sys import argv

#set argv to values from command line
script, input_file = argv

# function that takes a file object and prints out all contents of object
def print_all(f):
	print f.read()

# function that goes back to position 0 of the file object
def rewind(f):
	f.seek(0)

# function that reads one line of the until end of file object is reached
# will print whatever you put in as an argument for line_count
def print_a_line(line_count, f):
	print line_count, f.readline()

# open input_file and stores as current_file object
current_file = open(input_file)


print "First let's print the whole file:\n"
# run function on current_file argument
print_all(current_file)

print "Now let's rewind, kind of like a tape."

rewind(current_file)


print "Let's print three lines:"

# initialize a variale current_line to 1 and use in the print_a_line
# function
current_line = 1
print_a_line(current_line, current_file)

current_line = current_line + 1 # increment current_line should be 2 now
print_a_line(current_line, current_file)

current_line = current_line + 1 # increment again, should be 3 now
print_a_line(current_line, current_file)
