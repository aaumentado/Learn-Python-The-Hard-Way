from sys import argv

script, line_number = argv

print "Enter filename:" 

filename = raw_input("> ")

print "Here's your file %r:" % filename

txt = open(filename)

str1 = txt.readline()
str2 = txt.readline()
str3 = txt.readline()

print str1
