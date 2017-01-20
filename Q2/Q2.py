import numpy
import math
from matplotlib import pyplot as p
# plotting the histogram plot
data2 = [1, 1, 20, 3, 3, 6, 7, 7, 7, 8, 3, 8, 8, 8, 12, 15, 15, 16, 18, 6]
#p.hist(data2, bins=10)

#p.figure()
fig = p.figure()
p.hist(data2, bins=10)
fig.savefig('bin10.png',dpi=fig.dpi)

fig = p.figure()
p.hist(data2, bins=5)
fig.savefig('bin5.png',dpi=fig.dpi)
#p.close()

