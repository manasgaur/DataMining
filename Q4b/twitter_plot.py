import pandas as pd
from pandas.tools.plotting import parallel_coordinates
import json
from matplotlib import pyplot as p
from wordcloud import WordCloud
from scipy.stats import gaussian_kde
import numpy

f=open('/Users/manasgaur/Desktop/objective.txt','r')
lines=f.readlines()
objective=[]
for line in lines:
    objective.append(float(line.strip('\n')))

subjective=[]
f2=open('/Users/manasgaur/Desktop/subjective.txt','r')
lines=f2.readlines()
for line in lines:
    subjective.append(float(line.strip('\n')))

#print objective
for l in range(len(objective)):
    if objective[l] == 0.0 :
        objective[l]=0.000001

#print objective
for l in range(len(subjective)):
    if subjective[l] == 0.0 :
        subjective[l]=0.000001

senti=[objective, subjective]
df=pd.DataFrame(senti)
correlate=df.corr()
p.figure()
p.matshow(correlate)
p.show()

# this line reads the whole text
#text=open('tweet_text.txt').read()

# generate an image of word cloud
#wc=WordCloud().generate(text)
#p.figure()
#p.imshow(wc)
#p.axis('off')
#p.show()


density=gaussian_kde(objective)
p.plot(objective,density(objective))
p.show()

density=gaussian_kde(subjective)
p.plot(subjective,density(subjective))
p.show()

# designing the scatter plot
color=[numpy.random.rand(1), numpy.random.rand(1)]
p.scatter(objective, subjective, c=['red', 'blue'])
p.show()

plotdata = pd.read_csv('labelled_data.csv', sep=',')
parallel_coordinates(plotdata, 'label')
p.show()