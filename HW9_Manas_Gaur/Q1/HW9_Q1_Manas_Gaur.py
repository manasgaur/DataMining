import Orange
import urllib

raw_data = ["Captain America, Non-Stop, The Wolf of Wall Street",
            "Non-Stop, 300 Rise of an Empire, THOR",
            "Captain America, Frozen",
            "Captain America, Non-Stop, 300 Rise of an Empire",
            "Captain America, The Wolf of Wall Street, Frozen",
            "Non-Stop, The Wolf of Wall Street"]


# write data to the text file: data.basket
print " Association rule mining for the Mushroon data set"
#url='http://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.data'
f = open('data.basket', 'w')
#data = urllib.urlopen(url)
#raw_data2=open("sentiments.txt","r")
for item in raw_data:#2.readlines():
    f.write(item + '\n')
f.close()

# Load data from the text file: data.basket
data2 = Orange.data.Table("data.basket")


# Identify association rules with supports at least 0.3
rules = Orange.associate.AssociationRulesSparseInducer(data2, support = 0.3)
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
#f3=open("otherrules.txt","w")
for idx, d in enumerate(data2):
    print 'User {0}: {1}'.format(idx, data2[idx])
    for r in rules:
        if r.applies_left(d) and not r.applies_right(d):
            print "%4.1f %4.1f  %s" % (r.support, r.confidence, r)
            '''f3.write(str(r.support))
             f3.write("\t")
             f3.write(str(r.confidence))
             f3.write("\t")
             f3.write(str(r))
             f3.write("\n")#'''