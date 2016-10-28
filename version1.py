# Object oriented
# one candidate per generation
# Single character mutation with no granularity
# asexual reproduction
# user-defined target
# larger characterset
# Horrible fitness function
# Candidates have fixedf length

# This is the first solution generated for the project, with my later usability and readability improvements added.
# It should match version0 in performance (in theory) very closely, but is a much nicer template for later improvements.

#IMPORTS
import random
import string
import os
from ConfigParser import SafeConfigParser
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import re
import unicodedata

#SETUP AND API KEYS
parser = SafeConfigParser()
parser.read('keys.ini')

PLOT_KEY = (parser.get('keys','PLOT_KEY'))
PLOT_USER = (parser.get('keys','PLOT_USER'))
plotly.tools.set_credentials_file(username=PLOT_USER, api_key=PLOT_KEY)
gen_list = []
fit_list = []

#ORGANISM CLASS
class Organism(object):
#Organisms have dna, which can be evolved to create more viable dna

    def __init__(self, dna):
        self.dna = dna
        self.fitness = self.calc_fitness(target)

    def mutate(self):
        # Create a new candidate from the old candidate by changing one random character to another random character
        charpos = random.randint(0, len(self.dna) - 1)
        candidate = Organism(self.dna[0:charpos]+random.choice(string.printable[:-5])+self.dna[charpos+1:len(self.dna)])
        return candidate

    
    def calc_fitness(self, target):
        # Calculate fitness by seeing how many characters match up with characters in the source
        fitval = 0
        for i in range(0, len(self.dna)):
            if (self.dna[i] != target[i]):
                fitval += 1
        return(fitval)
#For sanitizing filenames
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', unicode(value)).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    return value


# Create records file
f = open(os.path.join("records", "temp1.txt") ,'w')

#Take input 
target = raw_input("Enter Evolution Target: ")
source = Organism(''.join([random.choice(string.printable[:-5]) for n in xrange(len(target))]))

parent = source
print "source: "+parent.dna
print "target: "+target


print >>f, "source: "+parent.dna+" "+str(len(parent.dna))
print >>f, "target: "+target+" "+str(len(target))

random.seed()
i = 0

while True:
   i += 1
   child = parent.mutate()

   if child.fitness < parent.fitness:
      parent = child
      print >>f, ("%5i %5i %14s" % (i, child.fitness, child.dna))
      gen_list.append(i)
      fit_list.append(child.fitness)
      
   if child.fitness == 0:
      print ("Evolution Complete")
      print (str(i) +" Generations Required")
      break

#Graphing
trace1 = go.Scatter(
    x=gen_list,
    y=fit_list,
    name = 'Evolving '+'<b>'+target+'</b> with v1', # Style name/legend entry with html tags
    connectgaps=True
)

data = [trace1]
layout = go.Layout(
    title='Version 1: Fitness v Generation',
    xaxis=dict(
        title='Generation',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Fitness',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=data, layout=layout)

graph = py.plot(fig, filename="g1"+slugify(target+source.dna), auto_open=False)

#Generate report
html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Evolving Strings: Version1</h1>

        <!-- *** Section 1 *** -->
        <h2>Graph of '''+target+'''</h2>
        <p>Started with '''+source.dna+''', '''+str(i)+''' generations required.</p>

        <iframe width="900" height="800" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + graph + '''.embed?width=800&height=550"></iframe>
        
    </body>
</html>'''



g = open(os.path.join("reports","r1"+slugify(target+source.dna)+".html") ,'w')
g.write(html_string)
f.close()
os.rename(f.name, os.path.join("records","g1"+slugify(target+source.dna)+".txt"))
g.close()