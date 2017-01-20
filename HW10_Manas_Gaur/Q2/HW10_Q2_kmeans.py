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
for lines in open("/Users/manasgaur/Downloads/HW10_Q2_sequencedata.txt").readlines():
    data.append(json.loads(lines))

vocab=dict()
#print data
for terms in data:
    print terms
    #terms=str(terms)
    for term in terms:
        print term
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
           x[vocab[term]]+=1
    X.append(x)

kmeans = KMeans(n_clusters = 3)
Y=kmeans.fit_predict(X)
clusters_file=dict()
for idx, cls in enumerate(kmeans.labels_):
    if clusters_file.has_key(cls):
        clusters_file[cls] += 1
    else:
        clusters_file[cls] = 1
    open('cluster-{1}.txt'.format(cls), 'a').write(json.dumps(data[idx]) + '\r\n')
