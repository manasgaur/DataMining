import Orange
import urllib

print " Association rule mining for the Mushroom data set"
url='http://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data'
f = open('data2.basket', 'w')
data = urllib.urlopen(url)
for item in data:#2.readlines():
    f.write(item + '\n')
f.close()

# Load data from the text file: data.basket
data2 = Orange.data.Table("data2.basket")


# Identify association rules with supports at least 0.3
rules = Orange.associate.AssociationRulesSparseInducer(data2, support = 0.6, confidence=0.6)
print len(rules)

# print out rules
f2=open("rules.txt",'w')
print "%4s %4s  %s" % ("Supp", "Conf", "Rule")
for r in rules[:]:
    f2.write(str(r.support))
    f2.write("\t")
    f2.write(str(r.confidence))
    f2.write("\t")
    f2.write(str(r))
    f2.write("\n")#print "%4.1f %4.1f  %s" % (r.support, r.confidence, r)

rule = rules[0]
f3=open("otherrules.txt","w")
for idx, d in enumerate(data2):
    print 'User {0}: {1}'.format(idx, data2[idx])
    for r in rules:
        if r.applies_left(d) and not r.applies_right(d):
            #print "%4.1f %4.1f  %s" % (r.support, r.confidence, r)
             f3.write(str(r.support))
             f3.write("\t")
             f3.write(str(r.confidence))
             f3.write("\t")
             f3.write(str(r))
             f3.write("\n")