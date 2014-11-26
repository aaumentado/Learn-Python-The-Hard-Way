def ex33_3(count, increment):
	i = 0
	numbers = []

	while i < count:
		print "At the top i is %d" % i
		numbers.append(i)

		i = i + increment
		print "Numbers now: ", numbers
		print "At the bottom i is %d" % i
	
	print "The numbers: "

	for num in numbers:
		print num

