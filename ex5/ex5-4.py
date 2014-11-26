# this is example 5 from Learning Python The Hard Way

name = 'Albert M. Aumentado'
age = 28 # yup 
height = 70 # inches
height_cm = height*2.54 # in to cm conversion
weight = 229 # lbs
weight_kg = weight*0.45 # convert lbs to kg
eyes = 'Brown'
teeth = 'White'
hair = 'Black'

print "Let's talk about %s." % name
print "He's %d cm tall." % height_cm
print "He's %d kg heavy." % weight_kg
print "Actually that is pretty heavy."
print "He's got %s eyes and %s hair." % (eyes, hair)
print "His teeth are usually %s depending on the coffee." % teeth

# this line is tricky, try to get it exactly right
print "If I add %d, %d, and %d I get %d." % (age, height_cm, weight_kg, age + height_cm + weight_kg)
