from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pylab as pl
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
import matplotlib.pyplot as plt
import json
import sys; sys.path.append('/Library/Python/2.7/site-packages/pattern')
from pattern.en import sentiment, positive

stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

tweets = []
for line in open('HW8_Q2_training_tweets.txt').readlines():
    tweets.append(json.loads(line))

# Extract the vocabulary of keywords
vocab = dict()
for tweet_id, class_label, text in tweets:
    for term in text.split():
        term = term.lower()
        if len(term) > 2 and term not in stopwords:
            if vocab.has_key(term):
                vocab[term] = vocab[term] + 1
            else:
                vocab[term] = 1

# Remove terms whose frequencies are less than a threshold (e.g., 20)
vocab = {term: freq for term, freq in vocab.items() if freq > 20}
# Generate an id (starting from 0) for each term in vocab
vocab = {term: idx for idx, (term, freq) in enumerate(vocab.items())}
print vocab

# Generate X and y
X = []
y = []
for tweet_id, class_label, tweet_text in tweets:
    x = [0] * len(vocab)
    terms = [term for term in tweet_text.split() if len(term) > 2]
    for term in terms:
        if vocab.has_key(term):
            x[vocab[term]] += 1
    y.append(class_label)
    X.append(x)
c_val=np.arange(0,2,1)
positive_tweets=[]
f1=open('mintweetsfile.txt','a')
f2=open('maxtweetsfile.txt','a')
# 10 folder cross validation to estimate the best w and b
for c in range(0,len(c_val)):
    svc = svm.SVC(kernel='linear',C=c_val[c])
    Cs = range(1, 20)
    clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs), cv = 10)
    clf.fit(X, y)

# predict the class labels of new tweets
    print clf.predict(X)
    tweets = []
    for line in open('HW8_Q2_testing_tweets.txt').readlines():
        tweets.append(json.loads(line))

# Generate X for testing tweets
    X = []
    for tweet_id, tweet_text in tweets:
        x = [0] * len(vocab)
        terms = [term for term in tweet_text.split() if len(term) > 2]
        for term in terms:
            if vocab.has_key(term):
                x[vocab[term]] += 1
        X.append(x)
    y = clf.predict(X)
    print clf.score(X,y)
    conf_score=[]
    conf_score=(clf.decision_function(X)).tolist()
    max_conf_score=conf_score
    min_conf_score=conf_score
    K=10
    for i in range(0,K-1):
        maxv=max_conf_score[0]
        max_i=0
        for j in range(1,len(max_conf_score)-1):
            if maxv<max_conf_score[j]:
                maxv=max_conf_score[j]
                max_i=j
        f2.write(str(tweets[max_i]))#sentiment(str(tweets[max_i])).assessments
        max_conf_score.remove(maxv)
    for i in range(0,K-1):
        min_i=0
        minv=min_conf_score[0]
        for j in range(1,len(min_conf_score)-1):
            if minv>min_conf_score[j]:
                minv=min_conf_score[j]
                min_i=j
        f1.write(str(tweets[min_i]))#sentiment(str(tweets[min_i])).assessments
        min_conf_score.remove(minv)
    positive_tweets.append(sum(y))
    print '\r\nAmong the total {1} tweets, {0} tweets are predicted as positive.'.format(sum(y), len(y))
'''f = open('svm_predictions.txt', 'w')
for idx, [tweet_id, tweet_text] in enumerate(tweets):
    f.write(json.dumps([tweet_id, y[idx]]) + '\r\n')
    if y[idx] == 1:
        print tweets[idx]
f.close()
'''
#print c_val
#print positive_tweets
# print 100 example tweets and their class labels
plt.plot(c_val.tolist(),positive_tweets)
plt.show()
    #print '\r\nAmong the total {1} tweets, {0} tweets are predicted as positive.'.format(sum(y), len(y))
