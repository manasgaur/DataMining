from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pylab as pl
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.cluster import KMeans
from hmmlearn.hmm import GaussianHMM
import matplotlib.pyplot as plt
import json

class markovmodel:
    #transmat: None
    def __init__(self, transmat = None, startprob = None):
        self.transmat = transmat
        self.startprob = startprob
    # It assumes the state number starts from 0
    def fit(self, X):
        ns = max([max(items) for items in X]) + 1
        self.transmat  = np.zeros([ns, ns])
        self.startprob = np.zeros([ns])
        for items in X:
            n = len(items)
            self.startprob[items[0]] += 1
            for i in range(n-1):
                self.transmat[items[i], items[i+1]] += 1
        self.startprob = self.startprob / sum(self.startprob)
        n = self.transmat.shape[0]
        d = np.sum(self.transmat, axis=1)
        for i in range(n):
            if d[i] == 0:
                self.transmat[i,:] = 1.0 / n
        d[d == 0] = 1
        self.transmat = self.transmat * np.transpose(np.outer(np.ones([ns,1]), 1./d))

    def predict(self, obs, steps):
        pred = []
        n = len(obs)
        if len(obs) > 0:
            s = obs[-1]
        else:
            s = np.argmax(np.random.multinomial(1, self.startprob.tolist(), size = 1))
        for i in range(steps):
            s1 = np.random.multinomial(1, self.transmat[s,:].tolist(), size = 1)
            pred.append(np.argmax(s1))
            s = np.argmax(s1)
        return pred

# X: sequence of observations
# y: sequence of latent states
def estimate_parameters(X, y):
    mm = markovmodel()
    mm.fit(y)
    data = dict()
    for i in range(len(y)):
        for s, x in zip(y[i], X[i]):
            if data.has_key(s):
                data[s].append(x)
            else:
                data[s] = [x]
    ns = len(data.keys())
    means = np.array([[np.mean(data[s])] for s in range(ns)])
    covars = np.tile(np.identity(1), (ns, 1, 1))
    for s in range(ns):
        covars[s, 0] = np.std(data[s])
    return mm.startprob, mm.transmat, means, covars

data=[]
Z=[]
for lines in open("/Users/manasgaur/Downloads/HW10_Q4_trainingdata.txt").readlines():
    data.append(json.loads(lines))

vocab=dict()

for terms,val in data:
    x2=[]
    for item, val2 in val:
        x=[]
        x.append(val2)
        x2.append(x)
        if vocab.has_key(item):
            vocab[item]+=1
        else:
            vocab[item]=1
    Z.append(x2)

vocab = {term: idx for idx, (term, freq) in enumerate(vocab.items())} # formation of the labels
label = {idx: term for idx, (term, freq) in enumerate(vocab.items())}
     #   print
    #terms=str(terms)
    #val,text=terms.partition(",")

#print val
Y=[]
#print vocab.get("Seattle")

for terms,val in data:
    #x=[0]*len(vocab)
    y=[]
    for item, val2 in val:
        if vocab.has_key(item):
            y.append(vocab.get(item))
        else:
            y.append(0)
    Y.append(y)

#for items in X:
 #   print items        """
startprob, transmat, means, covars = estimate_parameters(Z, Y)
model = GaussianHMM(5, "full", startprob, transmat)
model.means_  = means
model.covars_ = covars
#newY=model.predict(X)
#model.fit(Y,5)
#for x in Z:
 #   y = model.predict(x)
  #  print [label[s] for s in y]

testingdata=[]
for lines in open("HW10_Q4_testing.txt").readlines():
    testingdata.append(json.loads(lines))

NZ=[]
for terms in testingdata:
    x2=[]
    for item in terms:
        x=[]
        x.append(item)
        x2.append(x)
    NZ.append(x2)
print NZ
testfile=open("HW10_Q4_predictions.txt","w")
for x in NZ:
    y=model.predict(x)
    for s in y:
        testfile.write(label[s])
        testfile.write(",")
    testfile.write("\n")
testfile.close()