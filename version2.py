# Object oriented
# one candidate per generation
# Single character mutation with some granularity
# asexual reproduction
# user-defined target
# larger characterset
# More granular fitness function
# Candidates have fixed length

# This is the second solution generated for the project, with my later usability and readability improvements added.
# It added a better fitness function that allowed for more granular mutations to be relevant.
# Mutations were also adjusted to move only a single character a small distance at a time.

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
        fitval = 0
        for i in range(0, len(self.dna)):
            fitval += (ord(target[i]) - ord(self.dna[i])) ** 2
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

#Create records file
f = open(os.path.join("records", "temp2.txt") ,'w')

#Take input
target = raw_input("Enter Evolution Target: ")
parent = Organism(''.join([random.choice(string.printable[:-5]) for n in xrange(len(target))]))
source = parent

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
    name = 'Evolving '+'<b>'+target+'</b> with v2', # Style name/legend entry with html tags
    connectgaps=True
)

data = [trace1]
layout = go.Layout(
    title='Version 2: Fitness v Generation',
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

graph = py.plot(fig, filename="g2"+slugify(target+source.dna), auto_open=False)

#Generate report
html_string = '''
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
        <style>body{ margin:0 100; background:whitesmoke; }</style>
    </head>
    <body>
        <h1>Evolving Strings: Version2</h1>

        <!-- *** Section 1 *** -->
        <h2>Graph of '''+target+'''</h2>
        <p>Started with '''+source.dna+''', '''+str(i)+''' generations required.</p>

        <iframe width="900" height="800" frameborder="0" seamless="seamless" scrolling="no" \
src="''' + graph + '''.embed?width=800&height=550"></iframe>
        
    </body>
</html>'''

g = open(os.path.join("reports","r2"+slugify(target+source.dna)+".html") ,'w')
g.write(html_string)
f.close()
os.rename(f.name, os.path.join("records","g2"+slugify(target+source.dna)+".txt"))
g.close()