import numpy as np
import urllib
from matplotlib import pyplot as p
import json
import matplotlib.cm as cm
from matplotlib.colors import LogNorm
import pandas
from pandas.tools.plotting import parallel_coordinates
from pylab import pcolor, show, colorbar
from wordcloud import WordCloud
import PIL
from scipy.stats import gaussian_kde


url='http://archive.ics.uci.edu/ml/machine-learning-databases/balance-scale/balance-scale.data'

raw_data=urllib.urlopen(url)

dataset=np.loadtxt(raw_data,delimiter=',',usecols=[1,2,3,4])
#out=open('dataset.txt','w')
datalist=dataset.tolist()

#for i in datalist:
 #   json.dump(i,out)
 #   out.write('\n')
#print dataset
#print len(dataset)
#print dataset[1][3]
L=0
R=0
B=0
for i in range(len(dataset)):
    if dataset[i][0]*dataset[i][1] > dataset[i][2]*dataset[i][3]:
        L=L+1
    else :
        if dataset[i][0]* dataset[i][1] < dataset[i][2]* dataset[i][3]:
            R=R+1
        else :
            B=B+1

print 'L:',L
print 'R:',R
print 'B:',B
print np.mean(dataset)


rows=len(dataset)
col=1
newdata1=np.empty((rows,col))
newdata2=np.empty((rows,col))
#print newdata[0][1]
print "rows:", rows
print "cols:", col

for row in xrange(rows):
    var1=dataset[row][col-2]*dataset[row][col-1]
    var2=dataset[row][col]*dataset[row][col+1]
    t=[var1, var2]
    newdata1[row].fill(var1)
    newdata2[row].fill(var2)

newdata=[]
newdata=newdata1
newdata.sort()


fig = p.figure()
p.scatter(newdata,newdata2)
fig.savefig('scatter_plot.png',dpi=fig.dpi)

fig= p.figure()
p.hist(newdata,bins=10)
fig.savefig('hist_left.png',dpi=fig.dpi)

fig= p.figure()
p.hist(newdata2,bins=10)
fig.savefig('hist_right.png',dpi=fig.dpi)

fig = p.figure()
p.boxplot(newdata)
fig.savefig('boxplot_left.png',dpi=fig.dpi)

fig = p.figure()
p.boxplot(newdata2)
fig.savefig('boxplot_right.png',dpi=fig.dpi)

fig = p.figure()
p.boxplot(dataset)
fig.savefig('boxplot_complete.png',dpi=fig.dpi)

out1=open('newdata.txt','w')
out2=open('newdata2.txt','w')

nlist1=newdata.tolist()
nlist2=newdata2.tolist()

for item in nlist1:
    json.dump(item,out1)
    out1.write('\n')

for item in nlist2:
    json.dump(item,out2)
    out2.write('\n')


nlist1.sort()
nlist2.sort()
med1=np.median(nlist1)
med2=np.median(nlist2)
print 'median of left balance', med1
print 'median of right balance', med2

print 'standard deviation of left balance', np.std(nlist1)
print 'standard deviation of right balance',np.std(nlist2)

print 'minimum element in left balance', np.min(nlist1)
print 'maximum element in left balance', np.max(nlist1)

print 'minimum element in right balance', np.min(nlist2)
print 'maximum element in right balance', np.max(nlist2)

mad1=np.median(np.absolute(nlist1-med1))
mad2=np.median(np.absolute(nlist2-med2))

print 'median absolute deviation for left balance', mad1
print 'median absolute deviation for right balance', mad2


plotdata = pandas.read_csv('data.csv', sep=',')
fig=p.figure()
parallel_coordinates(plotdata, "label")
p.show
p.savefig('pc.png',dpi=fig.dpi)

#correlate=np.corrcoef(datalist)
#pcolor(correlate)
#colorbar()
#show()
df=pandas.DataFrame(datalist)
p.matshow(df.corr())

# separate program of wordcloud using twitter data
data=pandas.read_csv('data.csv',index_col=2)
data_norm=(data-data.mean())/(data.max()-data.min())
fig,ax=p.subplots()
heatmap=ax.pcolor(data_norm,cmap=p.cm.Blues, alpha=0.8)
p.show()
# density plots
#toplot=[nlist1, nlist2]
#density=scipy.stats.binomial(toplot)
#print toplot
#p.plot(toplot,density(toplot))
#p.show()
#print newdata[0][1]
    #newdata[i]=[[,[dataset[i][2]*dataset[i][3]]]

#print newdata[1]
#sorted(newdata[:][1])
#print np.median(newdata)



#values = np.loadtxt(raw_data, delimiter=',', usecols=[1,2,3,4])
#labels = np.loadtxt(raw_data, delimiter=',', usecols=[0])
#print labels
#print '\t'
#print values

#X=dataset[:,0:7]
#Y=dataset[:,8]

