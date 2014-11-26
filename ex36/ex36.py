from sys import exit

def galley_room():
	print "You are in the galley of a ship."
	print "There are doors to your left, right, and front."
	print "Which door do you take?"
	
	direction = raw_input("> ")

	if direction == "left":
		print "left"
		port()
	elif direction == "right":
		print "right"
		starboard()
	elif direction == "front":
		print "front"
		forward()
	else:
		reason = "You can't go that way!"
		dead(reason)

def port():
	cable = 'adamantium cable'
	cannister = 'compressed air cannister'
	spear = 'adamantium spear'
	tube = 'narrow hallow tube'
	
	inventory = [] # empty inventory list, max is three
	
	inventory_count = len(inventory) # initialize inventory size

	print """
	Portside.
	There are a number of items here:
	%s
	%s
	%s
	%s
	Which do you choose?""" % (cable, cannister, spear, tube)
	
	while inventory_count < 4:
		print inventory
		choice = raw_input("> ")
		
		if choice == "cable" or (choice in cable):
			if cable in inventory:
				print "You have it already!"
			else:	
				print "Taken. What else?"
				inventory.append(cable)
		elif choice == "cannister" or (choice in cannister):
			if cannister in inventory:
				print "You have it already!"
			else:
				print "Taken. What else?"
				inventory.append(cannister)
		elif choice == "spear" or (choice in spear):
			if spear in inventory:
				print "You have it already!"
			else:
				print "Taken. What else?"
				inventory.append(spear)
		elif choice == "tube" or (choice in tube and choice != "all"):
			if tube in inventory:
				print "You have it already!"
			else:
				print "Taken. What else?"
				inventory.append(tube)
		elif choice == "all" and inventory_count == 0:
			temp_list = [cable, cannister, spear, tube]
			print "%s, %s, %s, %s taken" % (cable, cannister, spear, tube)
			for i in temp_list:
				inventory.append(i)
		elif choice == "drop all":
			inventory = []
		else:
			print "You don't see %s around here!" % choice
		
		inventory_count = len(inventory)

	print "Your inventory is full! Choose a direction to go!"

	direction = raw_input('> ')
	
	if len(direction) != "":		
		if direction == "starboard":
			galley_room()
		else:
			reason = "You can't go that way!"
			dead(reason)
	else:
		reason = "That's not a direction!"
		dead(reason)

#def inventory_selector(item, inventory_list, max_item):
#	inventory_count = len(inventory_list)
#	if len(max_item) == 0:
#		max_item = inventory_count
#		
#	while inventory_count < max_item:
#		print inventory
#		choice = raw_input("> ")
#
#		for item in inventory_list:
#
#			if choice == "cable" or (choice in cable):
#				if cable in inventory:
#				print "You have it already!"
#			else:	
#				print "Taken. What else?"
#				inventory.append(cable)
#		elif choice == "cannister" or (choice in cannister):
#			if cannister in inventory:
#				print "You have it already!"
#			else:
#				print "Taken. What else?"
#				inventory.append(cannister)
#		elif choice == "spear" or (choice in spear):
#			if spear in inventory:
#				print "You have it already!"
#			else:
#				print "Taken. What else?"
#				inventory.append(spear)
#		elif choice == "tube" or (choice in tube and choice != "all"):
#			if tube in inventory:
#				print "You have it already!"
#			else:
#				print "Taken. What else?"
#				inventory.append(tube)
#		elif choice == "all" and inventory_count == 0:
#			temp_list = [cable, cannister, spear, tube]
#			print "%s, %s, %s, %s taken" % (cable, cannister, spear, tube)
#			for i in temp_list:
#				inventory.append(i)
#		elif choice == "drop all":
#			inventory = []
#		else:
#			print "You don't see %s around here!" % choice
#		
#		inventory_count = len(inventory)

def starboard():
	print "Starboardside"
	print "Nothing here! Choose a direction to go!"

	direction = raw_input('> ')
	
	if len(direction) != "":		
		if direction == "port":
			galley_room()
		else:
			reason = "You can't go that way!"
			dead(reason)
	else:
		reason = "That's not a direction"
		dead(reason)


def dead(reason):
	print reason, """
	You have destroyed the universe!
	Try again? Y/N"""
	choice = raw_input('> ')

	if choice == 'Y':
		start()
	else:
		exit(0)

	
def start():
	print "You stand in the middle of a small white room.  A console with a red button and blue button is in front of you. Which do you press?"

	user_input = raw_input("> ")

	if user_input == "blue":
		galley_room()
	elif user_input == "red":
		reason = "You chose %s" % user_input
		dead(reason) # destroyed the world
	else:
		print "What does that mean?"
		dead()

start()
