import numpy
import math
from matplotlib import pyplot as p

# plotting the boxplot
dataset1 = [1,1,20,3,3,6,7,7,7,8,3,8,8,8,12,15,15,16,18,6]
fig = p.figure()
p.boxplot(dataset1)
fig.savefig('boxplot1.png',dpi=fig.dpi)

dataset2 = [9,10,11,12,12,15,16,16,16,17,17,18,18,18,18,22,25, 25, 26, 28]
fig = p.figure()
p.boxplot(dataset2)
fig.savefig('boxplot2.png',dpi=fig.dpi)