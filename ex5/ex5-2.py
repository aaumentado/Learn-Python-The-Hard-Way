# this is example 5 from Learning Python The Hard Way

name = 'Albert M. Aumentado'
age = 28 # yup 
height = 70 # inches
weight = 229 # lbs
eyes = 'Brown'
teeth = 'White'
hair = 'Black'

print "Let's talk about %r." % name
print "He's %r inches tall." % height
print "He's %r pounds heavy." % weight
print "Actually that is pretty heavy."
print "He's got %r eyes and %r hair." % (eyes, hair)
print "His teeth are usually %r depending on the coffee." % teeth

# this line is tricky, try to get it exactly right
print "If I add %r, %r, and %r I get %r." % (age, height, weight, age + height + weight)
