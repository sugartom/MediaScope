#def dist(fa, fb):
#import vect_dis
import multi_query_lib
import operator
import sys
def sortByColumn(bigList, *args):
    bigList.sort(key=operator.itemgetter(*args), reverse = True)
    
def dist(f1, f2):
    f1_len = len(f1)
    f2_len = len(f2)
    if f1_len != f2_len:
        print "length not equal, please check!"
        return sys.float_info.max
    else:
        t_sum1 = sum(f1)
        t_sum2 = sum(f2)
        Result = 0
        if t_sum1 == 0 or t_sum2 == 0:
            Result = 100
        elif t_sum1 == 0 and t_sum2 == 0:
            Result = 0
        else:
            tc1 = 0
            tc2 = 0
            tc3 = 0
            for i in range(f1_len):
                tc1 = tc1 + 1.0*f1[i]*f2[i]/(t_sum1*t_sum2)
                tc2 = tc2 + 1.0*f1[i]*f1[i]/(t_sum1*t_sum1)
                tc3 = tc3 + 1.0*f2[i]*f2[i]/(t_sum2*t_sum2)
            Result = (100 - 100 * tc1/(tc2+tc3-tc1))
    return max(0, Result)
    
def assign(M, X):
    LM = len(M)
    LX = len(X)
    H = [None]*LX
    Center = [None]*LM
    CVal = [None]*LM
    for i in range(LM):
        Center[i] = []
        CVal[i] = []
    for i in range(LX):
        H[i] = [None]*LM
        
        for j in range(LM):
            H[i][j] = dist(X[i], M[j])
        #print H[i]
        ind = (H[i]).index(min(H[i]))
        #print ind
        Center[ind].append(i)
        CVal[ind].append(H[i][ind])
        
    return Center, CVal
import copy
def update(X, Center):
    M = [None]*len(Center)
    print Center
    for i in range(len(Center)):
        M[i] = []
        M[i] = copy.deepcopy(X[Center[i][0]])
        for j in range(1,len(Center[i])):
            for k in range(len(X[Center[i][0]])):
                M[i][k] = M[i][k] + X[Center[i][j]][k]
        for j in range(len(X[0])):
            M[i][j] = M[i][j]/len(Center[i])
    return M

def criter(M1,M2, acc):
    flag = 0
    for i in range(len(M1)):
        if dist(M1[i], M2[i]) > acc:
            flag = 1
            break
    if flag == 1:
        return False
    return True

def kmeans(X, K, iters, id2user, data, SZ, deadline):
    M = [None]*K
    if K > len(X):
        print "wrong k, check it"
        return {}
    for i in range(K):
        M[i] = copy.deepcopy(X[i])
    #    print M[i]
    #print len(M)
    acc = 1
    
    count = 0
    flag = 0
    Center = None
    CVal = None
    while count < iters:
        Center, CVal = assign(M,X)
        M1 = update(X, Center)
        if criter(M,M1,acc):
            flag = 1
            break
        else:
            M = copy.deepcopy(M1)
        count = count + 1
    if flag == 1:
        print "converged !!"
    vl = []
    for i in range(K):
        ids = []
        for j in Center[i]:
            if id2user[j] not in ids:
                ids.append(id2user[j])
        vl.append([len(ids), sum(CVal[i])/len(CVal[i]), i])
    sortByColumn(vl, 0)
    fresult = copy.deepcopy(vl[0])
    for i in range(1,len(vl)):
        if vl[i][0] == fresult[0]:
            if vl[i][1] < fresult[1]:
                fresult[1] = vl[i][1]
                fresult[2] = vl[i][2]
        else:
            break
            
    result = {}
    
    perc = []
    for k in range(len(Center[fresult[2]])):
        #perc.append( CVal[fresult[2]][k]/SZ[Center[fresult[2]][k]])
        perc.append( CVal[fresult[2]][k])
    sperc = sum(perc)
    for k in range(len(Center[fresult[2]])):
        pid = Center[fresult[2]][k]
        if data[pid][0] not in result:
            result[data[pid][0]] = ''
        result[data[pid][0]]  += str(data[pid][1]) + ':' + str(int(perc[k]*1000/sperc)) + ':' + deadline + '|'
    for i in result:
	print "key"
	print i
        result[i] = result[i][:-1]   
    return result

def call_kmeans(data, deadline, K=6):
#    print "data="+str(data)
    if (len(data) == 0):
        return ([], [])
    dist = [None]*len(data)
    SZ = [0]*len(data)
    name = data[0][0]
    id2user = []
    X = [None]*len(data)
    ct = 0
    for i in range(len(data)):
        dist[i] = [0]*len(data)
        if data[i][0] == name:
            id2user.append(ct)
        else:
            ct = ct + 1
            id2user.append(ct)
            name = data[i][0]
        SZ[i] =int( data[i][6])
        f1 = data[i][2].split('|')
#jyr
        f1_ = multi_query_lib.get_feature(f1[0]).split(' ')
#        _f1 = copy.deepcopy(f1_)
        for jj in range(len(f1_)):
            f1_[jj] = float(f1_[jj])
        X[i] = copy.deepcopy(f1_)
    iters = 1000
   # print  X
   # print len(X)
   # print K
    return kmeans(X, K, iters, id2user, data, SZ, deadline), None
#import random
"""
X = [None]*100
for i in range(100):
    X[i] = []
    for j in range(20):
        X[i].append(int(10*random.random()))
kmeans(X,5,1)
"""
