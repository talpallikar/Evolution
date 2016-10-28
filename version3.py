# Object oriented
# N candidates per generation
# Single character mutation with some granularity
# asexual reproduction
# user-defined target
# larger characterset
# More granular fitness function
# Candidates have fixed length

# This is the third solution generated for the project, with my later usability and readability improvements added.
# It spawns a gene pool of candidates and selects the best candidates for reproduction.
# This models an entire community instead of a single individual

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

random.seed()

#CONSTANTS
POOLSIZE = 20 #Size of the genepool

# Organism Class
class Organism(object):
#Organisms have dna, which can be evolved to create more viable dna

    def __init__(self, dna):
        self.dna = dna
        self.fitness = self.calc_fitness(target)

    def mutate(self):
        # the candidate to produce a child
        charpos = random.randint(0, len(self.dna) - 1)
        parts = list(self.dna)
        parts[charpos] = chr(ord(parts[charpos]) + random.randint(-1,1))
        return Organism(''.join(parts)) 

    def calc_fitness(self, target):
        # Calculate the fitness of the candidate
        fitval = 0
        for i in range(0, len(self.dna)):
            fitval += (ord(target[i]) - ord(self.dna[i])) ** 2
        return(fitval)
    
    def dump(self, generation, location):
        print >>location, "%6i %6i %15s" % (
            generation,
            self.fitness,
            self.dna
        )
        # print "%6i %6i %15s" % (
        #     generation,
        #     self.fitness,
        #     self.dna
        # )
        
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

#Create records file
f = open(os.path.join("temp3.txt") ,'w')





#Take input
target = raw_input("Enter Evolution Target: ")
#source = "Vpe1ZjGeMo9v40N6Z"

print "target: "+target

print >>f, "target: "+target+" "+str(len(target))

#Create a genepool
genepool = []
for x in range(0, POOLSIZE-1):
    candidate = Organism(''.join([random.choice(string.printable[:-5]) for n in xrange(len(target))]))
    genepool.append(candidate)

#Evolve the genepool
generation = 0

while True:
    generation += 1
    genepool.sort(key=lambda candidate: candidate.fitness)
    for candidate in genepool:
        candidate.dump(generation, f)
    print >>f
    #print
    if generation == 1:
        source=genepool[0]
    
    if genepool[0].fitness == 0:
        # Target reached
        print ("Evolution Complete")
        print (str(generation) +" Generations of Size: "+str(POOLSIZE)+" Required")
        break

    parent = genepool[0]

    child = parent.mutate()
    if child.fitness < genepool[-1].fitness:
        genepool[-1] = child
        gen_list.append(generation)
        fit_list.append(child.fitness)

#Graphing

trace1 = go.Scatter(
    x=gen_list,
    y=fit_list,
    name = 'Evolving '+'<b>'+target+'</b> with v3', # Style name/legend entry with html tags
    connectgaps=True
)

data = [trace1]
layout = go.Layout(
    title='Version 3: Fitness v Generation',
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

graph = py.plot(fig, filename="r3p"+str(POOLSIZE)+slugify(target+source.dna), auto_open=False)

#Generate report
html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Evolving Strings: Version 3</h1>

        <!-- *** Section 1 *** -->
        <h2>Graph of '''+target+'''</h2>
        <p>Started with '''+source.dna+''', '''+str(generation)+''' generations of size: '''+str(POOLSIZE)+''' required.</p>

        <iframe width="900" height="800" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + graph + '''.embed?width=800&height=550"></iframe>
        
    </body>
</html>'''

g = open(os.path.join("reports","r3p"+str(POOLSIZE)+slugify(target+source.dna)+".html") ,'w')
g.write(html_string)
g.close()
f.close()
os.rename(f.name, os.path.join("records","g3p"+str(POOLSIZE)+slugify(target+source.dna)+".txt"))