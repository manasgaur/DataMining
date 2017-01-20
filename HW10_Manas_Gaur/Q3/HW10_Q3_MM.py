from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pylab as pl
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.cluster import KMeans
from hmmlearn import hmm
import matplotlib.pyplot as plt
import json

data=[]
X=[]
for lines in open("HW10_Q3_training.txt").readlines():#"/Users/manasgaur/Downloads/HW10_Q2_sequencedata.txt").readlines():
    data.append(json.loads(lines))

vocab=dict()
#print data
for terms in data:
    #print terms
    #terms=str(terms)
    for term in terms:
        if vocab.has_key(term):
            vocab[term]+=1
        else:
            vocab[term]=1

vocab = {term: idx for idx, (term, freq) in enumerate(vocab.items())}
print vocab
for text in data:
    x = [0] * len(vocab)
    #text=str(text)
    #terms = [term for term in text.split() if len(term) > 2]
    for term in text:
        if vocab.has_key(term):
            x.append((vocab[term]))
    X.append(x)
print X
#print ctr
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
        self.transmat = self.transmat * \
                        np.transpose(np.outer(np.ones([ns,1]), 1./d))

    def predict(self, obs, steps):
        pred = []
        n = len(obs)
        if len(obs) > 0:
            s = obs[-1]
        else:
            s = np.argmax(np.random.multinomial(1,
                            self.startprob.tolist(), size = 1))
        for i in range(steps):
            s1 = np.random.multinomial(1, self.transmat[s,:].tolist(),
                                       size = 1)
            pred.append(np.argmax(s1))
            s = np.argmax(s1)
        return pred

mm=markovmodel()
label = {0: 'Washington D.C.', 1: 'New York City', 2: 'Seattle', 4: 'Philapedia', 3: 'Boston'}
print "the training file output"
mm.fit(X)
pred=mm.predict([],5)
print [label[s] for s in pred]

#print len(Y)

Test=[]
for items in open("HW10_Q3_testing.txt").readlines():
    Test.append(json.loads(items))

X=[]
testfile=open("HW10_Q3_predictions.txt","a")
for text in Test:
    x = [0] * len(vocab)
    #text=str(text)
    #terms = [term for term in text.split() if len(term) > 2]
    for term in text:
        if vocab.has_key(term):
            x.append((vocab[term]))
    X.append(x)
    mm.fit(X)
    pred=mm.predict([],5)
    for s in pred:
        testfile.write(label[s])
        testfile.write(",")
    testfile.write("\n")
testfile.close()





