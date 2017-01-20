####################### importing some of the necessary libraries for the program ####################
import json
import string
import re
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pylab as pl
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from stop_words import get_stop_words
import pickle

############################ Processing Stage of the Data ###############################
Tweets=[]
for lines in open("train_neg_tweets.txt").readlines():
    Tweets.append(json.loads(lines))

print len(Tweets)

TT=open("total_tweets_train.txt","w")
#boolean_label={0:"False", 1:"True"}

for tweet in Tweets:
    TT.write(str(0))
    TT.write(",")
    result = re.sub(r"http\S+", "", tweet['text'])
    result= re.sub(' +',' ',result)
    #result=result.split()#strip(' \n\t')
    result=' '.join(result.split())
    result = result.replace(',', '')
    printable=set(string.printable)
    newtext=filter(lambda x: x in printable, result)
    TT.write("\"")
    TT.write(str(newtext))
    TT.write("\"")
    TT.write("\n")

Tweets=[]
for lines in open("train_pos_tweets.txt").readlines():
    Tweets.append(json.loads(lines))

for tweet in Tweets:
    TT.write(str(1))
    TT.write(",")
    result = re.sub(r"http\S+", "", tweet['text'])
    result= re.sub(' +',' ',result)
    result=' '.join(result.split())
    result = result.replace(',', '')
    printable=set(string.printable)
    newtext=filter(lambda x: x in printable, result)
    TT.write("\"")
    TT.write(str(newtext))
    TT.write("\"")
    TT.write("\n")
TT.close()
print " total_tweets_train.txt has been created"
######################## creating the list of stopwords and Users  ##################################

Tweets=[]
B=[]
for line in open("total_tweets_train.txt").readlines():
    B.append(line[0])
print B[0]
    #Tweets.append(json.loads(lines))

Tweets2=[]
for terms in open("train_neg_tweets.txt").readlines():
    Tweets2.append(json.loads(terms))

for terms in open("train_pos_tweets.txt").readlines():
    Tweets2.append(json.loads(terms))

stopwords=[]
c=0
#User_file= open("users_file.txt","w")
for t1 in Tweets2:
    if not (t1['text_items'][0] in stopwords):
        for items in t1['text_items'][0]:
            stopwords.append(items)
    '''
    users=[]
    for items in t1['text_items'][2]:
        items=items.encode('utf-8')
        items=items.replace("@","")
        users.append(items)
    if users:
        User_file.write(str(B[c]))
        User_file.write(",")
        User_file.write(str(users))
        User_file.write("\n")
        c=c+1
    else :
        c=c+1
    '''
#print len(stopwords)
stopwords=set(stopwords)
stopwords=list(stopwords)
print len(stopwords)
#User_file.close()
#print " User_file.txt has been created"

#################################### performing the classification process #############################################
#tuples=[]
vocab=dict()
tuples=[]
spanish_sw=get_stop_words('es')
spanish_sw=[x.encode('utf-8') for x in spanish_sw]
english_sw=get_stop_words('en')
english_sw=[x.encode('utf-8') for x in english_sw]
for lines in open("total_tweets_train.txt").readlines():
    val, text=lines.split(",")
    for term in text.split():
        term = term.lower()
        if len(term) >= 2 and (term not in spanish_sw or term not in english_sw) and term in stopwords:
            if vocab.has_key(term):
                vocab[term] = vocab[term] + 1
            else:
                vocab[term] = 1

# Remove terms whose frequencies are less than a threshold (e.g., 20)
vocab = {term: freq for term, freq in vocab.items() if freq > 100}
# Generate an id (starting from 0) for each term in vocab
vocab = {term: idx for idx, (term, freq) in enumerate(vocab.items())}
print vocab

Y=[]
X=[]
for lines in open("total_tweets_train.txt").readlines():
    x = [0] * len(vocab)
    val,text=lines.split(",")
    terms = [term for term in text.split()]
    for term in terms:
        if vocab.has_key(term):
            x[vocab[term]] += 1
    Y.append(val)
    X.append(x)

# random split getting 20 % accuracy
#X_test=X[len(X)-2000 : len(X)]
#Y_test=Y[len(Y)-2000 : len(Y)]

# split based on cross validation
X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X,Y,test_size=0.1, random_state=0)
#for items in X:
 #   print items
f = open('trained_LogR_classifier.pkl', 'w')
clf = LogisticRegression()
#Cs = range(1, 10)
#clf = GridSearchCV(estimator=clf, param_grid=dict(C=Cs), cv = 10)
clf.fit(X_train,Y_train)

print clf.score(X_test,Y_test)
f.write(pickle.dumps(clf))
f.close()
boolean_label={0:"False", 1:"True"}
Tweets=[]
"""
for lines in open("train_neg_tweets.txt").readlines():
    Tweets.append(json.loads(lines))
for lines in open("train_pos_tweets.txt").readlines():
    Tweets.append(json.loads(lines))
for items,tweets in zip(pred_output,Tweets):
    print tweets['embersId'], ":", boolean_label[int(items)]
"""
Tweets=[]
for items in open("testing_tweets_quiz_DM.txt","r"):
    Tweets.append(json.loads(items))

#boolean_label={0:"False", 1:"True"}
test_X=[]
for tweet in Tweets:
    x=[0]*len(vocab)
    result = re.sub(r"http\S+", "", tweet['text'])
    result= re.sub(' +',' ',result)
    #result=result.split()#strip(' \n\t')
    result=' '.join(result.split())
    result = result.replace(',', '')
    printable=set(string.printable)
    newtext=filter(lambda x: x in printable, result)
    terms = [term for term in newtext.split()]
    for term in terms:
        if vocab.has_key(term):
            x[vocab[term]] += 1
    test_X.append(x)

f=open("new_testing_file.txt","w")
for items in test_X:
    f.write(str(items))
    f.write("\n")

prediction=open("QUIZ_DM_Predictions_LogR.txt","w")
pred_output=clf.predict(test_X)
for items,tweets in zip(pred_output,Tweets):
    prediction.write(tweets['embersId'])
    prediction.write(":")
    prediction.write(boolean_label[int(items)])
    prediction.write("\n")
prediction.close()
print " QUIZ_DM_Predictions_LogR.txt has been created"


Tweets=[]
for items in open("/Users/manasgaur/Desktop/unlabeled_tweets.txt").readlines():
    Tweets.append(json.loads(items))

#boolean_label={0:"False", 1:"True"}
unlabeled_X=[]
for tweet in Tweets:
    result = re.sub(r"http\S+", "", tweet['text'])
    result= re.sub(' +',' ',result)
    #result=result.split()#strip(' \n\t')
    result=' '.join(result.split())
    result = result.replace(',', '')
    printable=set(string.printable)
    newtext=filter(lambda x: x in printable, result)
    terms = [term for term in newtext.split()]
    for term in terms:
        if vocab.has_key(term):
            x[vocab[term]] += 1
    unlabeled_X.append(x)

prediction=open("QUIZ_DM_Predictions_unlabeled_tweets_LogR.txt","w")
pred_output=clf.predict(unlabeled_X)
for items,tweets in zip(pred_output,Tweets):
    prediction.write(tweets['embersId'])
    prediction.write(":")
    prediction.write(boolean_label[int(items)])
    prediction.write("\n")
prediction.close()
print "QUIZ_DM_Predictions_unlabeled_tweets_LogR.txt has been created"