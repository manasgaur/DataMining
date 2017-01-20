 import numpy as np
 from matplotlib import pyplot as p
 from pattern.en import sentiment
 from scipy.stats import gaussian_kde
 
f=open('tweet_text.txt','r')
lines=f.readlines()

senti=[]
for line in lines:
     senti.append(sentiment(line))

for line in lines:
     print sentiment(line)

objective=[]
for l in range(len(senti)):
     objective.append(senti[l][0])

print len(objective)
subjective=[]
for l in range(len(senti)):
    subjective.append(senti[l][1])

objective.sort()
print len(objective)

subjective.sort()
print len(subjective)
print np.median(objective)

print np.median(subjective)

print np.mean(objective)
print np.mean(subjective)
print np.std(objective)
print np.std(subjective)

med_obj=np.median(objective, axis=None)
mad_obj=np.median(np.absolute(objective-med_obj),axis=None)
med_sub=np.median(subjective, axis=None)
mad_sub=np.median(np.absolute(subjective-med_sub),axis=None)
print mad_obj

print mad_sub

mad_obj=np.median((objective-med_obj),axis=None)
print mad_obj

p.figure()
p.hist(objective,bins=10)
p.show()
p.figure()
p.hist(subjective,bins=10)
p.show()

density=gaussian_kde(objective)
p.plot(objective,density(objective))
p.show()

density=gaussian_kde(subjective)
p.plot(subjective,density(subjective))
p.show()

f=open('subjective.txt','r')
lines=f.readlines()
label2=[]
for line in lines:
    if float(line.strip('\n'))>0.1 :
       label2.append('positive')
    elif float(line.strip('\n'))<0.1 :
       label2.append('negative')
    else:
       label2.append('neutral')

f=open('objective.txt','r')
lines=f.readlines()
label1=[]
for line in lines:
    if float(line.strip('\n'))>0.1 :
       label1.append('positive')
    elif float(line.strip('\n'))<0.1 :
       label1.append('negative')
    else:
       label1.append('neutral')