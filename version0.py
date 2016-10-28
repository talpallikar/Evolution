# No objects
# one candidate per generation
# Single character mutation with no granularity
# asexual reproduction
# defined target
# letter based source
# Horrible fitness function
# Candidates have fixed length

# This file is here to represent the first real solution produced for this project (before it became associated with the Modes class). 
# The variable and method names have been modified both for readability and to more closely resemble subsequent solutions, 
# but the algorithms used remain the same.

import random
import string

f = open(os.path.join("records","genealogy0.txt") ,'w')

target = "the"
source = ''.join([random.choice(string.ascii_letters) for n in xrange(len(target))])

print "source: "+source
print "target: "+target

print >>f, "source: "+source+" "+str(len(source))
print >>f, "target: "+target+" "+str(len(target))

# Calculate fitness by seeing how many characters match up with characters in the source
def fitness(source, target):
   fitval = 0
   for i in range(0, len(source)):
      if (source[i] != target[i]):
          fitval += 1
   return(fitval)

# Create a new candidate from the old candidate by changing one random character to another random character
def mutate(source):
   charpos = random.randint(0, len(source) - 1)
   candidate = source[0:charpos]+random.choice(string.ascii_letters)+source[charpos+1:len(source)]
   return candidate

random.seed()
fitval = fitness(source, target)
i = 0

while True:
   i += 1
   m = mutate(source)
   fitval_m = fitness(m, target)
   if fitval_m < fitval:
      fitval = fitval_m
      source = m 
      print >>f, ("%5i %5i %14s" % (i, fitval_m, m))
   if fitval == 0:
      print ("Evolution Complete")
      print (str(i) +" Generations Required")
      break
      
