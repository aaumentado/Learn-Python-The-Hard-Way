def ex33_1(count):
	i = 0
	numbers = []

	while i < count:
		print "At the top i is %d" % i
		numbers.append(i)

		i = i + 1
		print "Numbers now: ", numbers
		print "At the bottom i is %d" % i
	
	print "The numbers: "

	for num in numbers:
		print num

print "Let's test the function."
ex33_1(10)
