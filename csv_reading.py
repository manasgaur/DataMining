import csv
import numpy as np
import matplotlib.pyplot as plt
xaxis=[]
yaxis=[]
with open('/Users/manasgaur/Desktop/counts.csv','r') as f:
    reader=csv.reader(f)
    for row1,row2 in reader:
        xaxis.append(int(row1))
        yaxis.append(int(row2))

xaxis_arr=np.asarray(xaxis)
yaxis_arr=np.asarray(yaxis)
yaxis_arr=yaxis_arr/1000

plt.bar(xaxis_arr,yaxis_arr)
plt.xlabel('number of reviews')
plt.ylabel('number of products getting that number of reviews')

plt.show()

