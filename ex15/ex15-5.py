print "Enter filename:" 

filename = raw_input("> ")

print "Here's your file %r:" % filename

txt = open(filename)

print txt.read()
