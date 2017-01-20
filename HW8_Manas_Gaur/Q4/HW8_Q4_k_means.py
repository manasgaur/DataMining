from sklearn.linear_model import LogisticRegression
from sklearn import svm
import pylab as pl
import numpy as np
from sklearn import cross_validation
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from math import log
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cdist
import json

stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]

tweets = []
for line in open('HW8_Q4_data.txt').readlines():
    tweets.append(json.loads(line))

# Extract the vocabulary of keywords
vocab = dict()
for tweet_id, tweet_text in tweets:
    for term in tweet_text.split():
        term = term.lower()
        if len(term) > 2 and term not in stopwords:
            if vocab.has_key(term):
                vocab[term] = vocab[term] + 1
            else:
                vocab[term] = 1

# Remove terms whose frequencies are less than a threshold (e.g., 15)
vocab = {term: freq for term, freq in vocab.items() if freq > 20}
# Generate an id (starting from 0) for each term in vocab
vocab = {term: idx for idx, (term, freq) in enumerate(vocab.items())}

# Generate X
X = []
for tweet_id, tweet_text in tweets:
    x = [0] * len(vocab)
    terms = [term for term in tweet_text.split() if len(term) > 2]
    for term in terms:
        if vocab.has_key(term):
            x[vocab[term]] += 1
    X.append(x)

# K-means clustering
# in this snippet just comment s_avg and S_list and uncomment the commented S_list.append(sum.... for Elbow method
# If you run the program as it is , it will use silhouette map based identification of K in KMeans
K_val=np.arange(2,50,1)
S_list=[]
for k in K_val:
    kmeans = KMeans(n_clusters = k)
    y=kmeans.fit_predict(X)
    #print len(y)
    s_avg=silhouette_score(np.asarray(X),y)
    S_list.append(s_avg)
    #S_list.append(sum(np.min(cdist(X, kmeans.cluster_centers_,'euclidean'),axis=1))/np.asarray(X).shape[0])

plt.plot(K_val.tolist(),S_list)
plt.show()

for K in K_val:
    km = KMeans(n_clusters = K, n_init = 100) # try 100 different initial centroids
    class_labels=km.fit_predict(np.asarray(X))
    s_avg=silhouette_score(np.asarray(X),class_labels)
    S_list.append(s_avg)
    cluster = []
    cluster_stat = dict()
# Print tweets that belong to cluster 2
    for idx, cls in enumerate(km.labels_):
        if cluster_stat.has_key(cls):
            cluster_stat[cls] += 1
        else:
            cluster_stat[cls] = 1
   # open('cluster-{0}.txt'.format(cls), 'a').write(json.dumps(tweets[idx]) + '\r\n')

#print 'basic information about the clusters that are generated by the k-means clustering algorithm: \r\n'
#print 'total number of clusters: {0}\r\n'.format(len(cluster_stat))
#for cls, count in cluster_stat.items():
#    print 'cluster {0} has {1} tweets'.format(cls, count)
S_arr=np.asarray(S_list)
newS=np.log10(S_arr)
plt.plot(K_val.tolist(),newS)
plt.show()
