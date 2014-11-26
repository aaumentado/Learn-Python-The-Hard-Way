# more printing stuff

tabby_cat = "\tI'm tabbed in."
persian_cat = "I'm split\non a line."
backslash_cat = "I'm \\ a \\ cat."

fat_cat = """
I'll do a list:
\t* Cat food
\t* Fishies
\t* Catnip\n\t* Grass
"""

print tabby_cat
print persian_cat
print backslash_cat
print fat_cat

#this is some extra code

#print "This is some extra output regarding escape codes:"

#while True:
#	for i in ["/","-","|","\\","|"]:
#		print "%s\r" % i,

print "This is a statement using '%r' for output: %r " % ('%r',"\\")
print "This is a statement using '%s' for output: %s" % ('%s',"\\")
print "This is a statement using '%s' for output: %s" % ('%s',"%r")
