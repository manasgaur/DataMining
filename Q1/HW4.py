# this file contains HW4 solutions
import numpy
import math
from matplotlib import pyplot as p

data=[3, 8, 3, 4, 3, 6, 4, 8, 9, 1, 3, 5, 10, 1, 2, 3, 4, 5, 2, 8]

#for l in range(len(data)):
 #   print data[l]

mean_data = numpy.mean(data)
data.sort()
median_data = numpy.median(data)
stddev_data = numpy.std(data)
var_data = math.pow(stddev_data,2)
mad=numpy.median(numpy.absolute(data-median_data))
print 'Mean:', mean_data
print 'Median:', median_data
print 'Standard Deviation:', stddev_data
print 'Variance:',var_data
print 'MAD:', mad

