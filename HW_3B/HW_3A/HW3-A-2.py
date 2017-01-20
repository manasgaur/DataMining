
R = {(1, False, False), (4, True, True), (6, True, True), (9, True, False), (10, False, True), (12, True, False), (13, True, False), (14, True, False), (15, True, True)}

M = {(2, True, False), (3, True, True), (6, True, True), (9, True, False), (14, True, False)}
M=M.intersection(R)
newR=R.difference(M)
print len(newR)
print len(M)
crawledREST_trueM=0
positiveM=0
REST_trueR=0
positivetweets=0
# Calculating API Recall
temp=[]
for l in range(len(M)):
    temp=M.pop()
    if temp[1]:
            crawledREST_trueM=crawledREST_trueM+1
    if temp[1]:
        if temp[2]:
            positiveM=positiveM+1
    if temp[2]:
        positivetweets=positivetweets+1

temp2=[]
for m in range(len(newR)):
    temp2=newR.pop()
    if temp2[1]:
        REST_trueR=REST_trueR+1
    if temp2[2]:
        positivetweets=positivetweets+1

total_REST=crawledREST_trueM+REST_trueR
print '**********Result of HW3-A-Question2**********'
print 'API_RECALL',float(crawledREST_trueM/float(total_REST))
print 'Quality Precision', float(positiveM/float(crawledREST_trueM))
print 'Quality Recall',float(positiveM/float(positivetweets))