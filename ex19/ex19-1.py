# here we define a function called cheese_and_crackers
# it takes to arguments, "cheese_count" and "boxes_of_crackers"
def cheese_and_crackers(cheese_count, boxes_of_crackers):
	# print statements to output arguments
	# note %d is used to output integers, check below with an example
	print "You have %d cheeses!" % cheese_count
	print "You have %d boxes of crackers!" % boxes_of_crackers
	print "Man that's enough for a party!"
	print "Get a blanket.\n"


print "We can just give the function numbers directly:"
# arguments are just integers
cheese_and_crackers(20, 30)

# the code below doesn't handle the way I though it would
# since the expected type is %d in the print statements
# I thought that user_arg* as just raw input would be interpreted
# as an integer in the function
# Just so it would work I converted the raw input to float and then int
# so that that script wouldn't crash
print """Arguments are assumed to be integers.\n
Enter two non-integer values below and see what happens\n
"""
user_arg1 = int(float(raw_input("arg1: ")))
user_arg2 = int(float(raw_input("arg2: ")))
cheese_and_crackers(user_arg1, user_arg2)

# use variables described in script
print "OR, we can use variables from our script:"
amount_of_cheese = 10
amount_of_crackers = 50

cheese_and_crackers(amount_of_cheese, amount_of_crackers)

# use numbers with math operations
print "We can even do math inside too:"
cheese_and_crackers(10 + 20, 5 + 6)

# use numbers with variables combined using math operations
print "And we can combine the two, variable and math:"
cheese_and_crackers(amount_of_cheese + 100, amount_of_crackers + 1000)
