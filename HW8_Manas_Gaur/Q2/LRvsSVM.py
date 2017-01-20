import json
import numpy
fSVMp=open('HW8_Q2_svm_predictions.txt','r')
fLRp=open('HW8_Q2_LR_predictions.txt','r')
fdata=open('HW8_Q2_training_tweets.txt','r')

tuples=[]
for line in fSVMp.readlines():
    tuples.append(json.loads(line))

SVMp=[]
for svmi,svmp in tuples:
    SVMp.append(svmp)

tuples=[]
for line in fLRp.readlines():
    tuples.append(json.loads(line))

LRp=[]
for lri,lrp in tuples:
    LRp.append(lrp)

tuples=[]
for line in fdata.readlines():
    tuples.append(json.loads(line))

data=[]
for datai,datav,text in tuples:
    data.append(datav)

#print data
#print LRp
c_LR=0
c_SVM=0
data=numpy.asarray(data)
LRp=numpy.asarray(LRp)
SVMp=numpy.asarray(SVMp)
for i in range(0,len(data)-1):
    if data[i]==LRp[i]:
        c_LR=c_LR+1
    if data[i]==SVMp[i]:
        c_SVM=c_SVM+1

print "SVM accuracy:", float(float(c_SVM)/2000)
print "LR accuracy:", float(float(c_LR)/2000)
