from sys import argv

script, count, increment = argv
def ex33_5(count, increment):
	i = 0
	numbers = []

	for i in range(0, count, increment):
		print "At the top i is %d" % i
		numbers.append(i)

		i = i + increment
		print "Numbers now: ", numbers
		print "At the bottom i is %d" % i
	
	print "The numbers: "

	for num in numbers:
		print num

ex33_5(int(count),int(increment))
