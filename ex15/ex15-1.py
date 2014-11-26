# this adds the argv feature for getting input from the command line
from sys import argv

# this gets the command line arguments
script, filename = argv

# open file and store as object in variable txt
txt = open(filename)

print "Here's your file %r:" % filename

# read and print out contents of variable txt
print txt.read()

txt.close()

print "Type the filename again:"
# prompt user for input
file_again = raw_input("> ")

# open file and store as object in variable text_again
txt_again = open(file_again)

# read and print out contents of variable text_again
print txt_again.read()

txt_again.close()
