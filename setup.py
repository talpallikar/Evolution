import os

os.mkdir("records")
os.mkdir("reports")
f = open("keys.ini" ,'w')

usernm = raw_input("input plotly user: ")
apikey = raw_input("input plotly api key: ")

f.write("[keys]")
f.write("PLOT_USER = "+usernm)
f.write("PLOT_KEY = "+apikey)
f.close()