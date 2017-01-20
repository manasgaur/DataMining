from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pylab as pl
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt
import json

tuples=[]
lst=[]
X=[]
Y=[]
label=[]
data=dict()
for line in open("HW10_Q1_training.txt").readlines():
    tuples.append(json.loads(line))

#print len(tuples)
for a,b in tuples:
    #Y.append(a)
    for term in b:
        if data.has_key(term):
            data[term]=data[term]+1
        else:
            data[term]=1

data = {term: idx for idx, (term, freq) in enumerate(data.items())}
print data

for a,b in tuples:
    x=[0]*len(data)
    #Y.append(a)
    for term in b:
        if data.has_key(term):
            x[data[term]]+=1
    X.append(x)
    Y.append(a)
    #X,Y=line.split()

print len(X)
print len(Y)

clf=svm.SVC(kernel="linear", C=1.0)
clf.fit(X,Y)
#print clf.predict(X)

test=[]
Test=[]
for line in open("HW10_Q1_testing.txt").readlines():
    Test.append(json.loads(line))
for line in Test:
    y=[0]*len(data)
    for term in line:
        #print term
        if data.has_key(term):
            y[data[term]]+=1
    test.append(y)

#print test

result=clf.predict(test)
f2=open("HW10_Q1_predictions.txt",'w')
for i in result:
    f2.write(str(i))
    f2.write("\n")
f2.close()
