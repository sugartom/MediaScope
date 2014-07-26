import random
import operator
import sys, copy,math
def sortByColumn(bigList, *args):
    bigList.sort(key=operator.itemgetter(*args), reverse = True)

def sortByColumn2(bigList, *args):
    bigList.sort(key=operator.itemgetter(*args))



def Runtime_deadline(FTask, Deadline, EarlyDL):
    timespend = 0.0
    
    credit_earned = 0
    id_got = []
    tid_got = []
    flag = 0
    while timespend < MD:
        tmptask = copy.deepcopy(FTask)
        flag = 0
        for dl in EarlyDL:
            if timespend < Deadline[dl[1]][0] or timespend > dl[0]:
                continue
            else:
                sortByColumn(FTask[dl[1]], 0)
                for i in range(len(FTask[dl[1]])):
                    arr = FTask[dl[1]][i]
                    if arr[0] == -1:
                        break
                    if arr[2] <= dl[0] - timespend:
                        timespend = timespend + arr[2]
                        credit_earned = credit_earned + arr[0]
                        FTask[dl[1]][i][0] = -1
                        id_got.append(arr[1])
                        tid_got.append(dl[1])
                        flag = 1
                        break
            if flag == 1:
                break
        if FTask == tmptask:
            timespend = timespend + 0.1

#    print FTask
#    print id_got
#    print tid_got
#    print credit_earned
    return credit_earned


def Runtime_maxslotcredit(Credit, FD, FSize, Deadline, MD, slot):
    timespend = 0.0
    newcredit = copy.deepcopy(Credit)
    credit_earned = 0
    id_got = []
    tid_got = []
    flag = 0
    while timespend < MD:
        sortByColumn(newcredit, 0)
        #print newcredit
        tmpcredit = copy.deepcopy(newcredit)
        tmptime = 0
        tmpearn = 0
        flag = 0
        flag2 = 0
        tpid = 0
        for i in range(len(newcredit)):
            dl_id = FD[newcredit[i][1]]
            rg_id = newcredit[i][1]
            #print dl_id
            if Deadline[dl_id][1] <= timespend:
                newcredit[i][0] = -1
            elif Deadline[dl_id][0] > timespend:
                continue
            else:
                if FSize[rg_id] > Deadline[dl_id][1] - timespend:
                    continue
                else:
                    if newcredit[i][0] == -1:
                        #flag = 1
                        break
                    if flag == 0:
                        tmptime = FSize[rg_id]
                        tmpearn = newcredit[i][0]
                        tpid = i
                        flag = 1
                    if Deadline[dl_id][1] <= timespend + slot:
                        timespend = timespend + FSize[rg_id]
                        credit_earned = credit_earned + newcredit[i][0]
                        newcredit[i][0] = -1
                        id_got.append(rg_id)
                        tid_got.append(dl_id)
                        flag2 = 1
                        break
        if flag == 1 and flag2 == 0:
            timespend = timespend + tmptime
            credit_earned = credit_earned + tmpearn
            newcredit[tpid][0] = -1
            print "slot not good"
        if tmpcredit == newcredit:
            timespend = timespend + 0.1
        #if flag == 1:
        #    break
#    print newcredit
#    print id_got
#    print tid_got
#    print credit_earned
#    print MD
#    print timespend
    return credit_earned


def Runtime_maxunitslotcredit(Credit, FD, FSize, Deadline, MD, slot):
    timespend = 0.0
    newcredit = copy.deepcopy(Credit)
    for i in range(len(newcredit)):
        newcredit[i][0] = float(newcredit[i][0]/FSize[i])
    credit_earned = 0
    id_got = []
    tid_got = []
    flag = 0
    while timespend < MD:
        sortByColumn(newcredit, 0)
        #print newcredit
        tmpcredit = copy.deepcopy(newcredit)
        tmptime = 0
        tmpearn = 0
        flag = 0
        flag2 = 0
        tpid = 0
        for i in range(len(newcredit)):
            dl_id = FD[newcredit[i][1]]
            rg_id = newcredit[i][1]
            #print dl_id
            if Deadline[dl_id][1] <= timespend:
                newcredit[i][0] = -1
            elif Deadline[dl_id][0] > timespend:
                continue
            else:
                if FSize[rg_id] > Deadline[dl_id][1] - timespend:
                    continue
                else:
                    if newcredit[i][0] == -1:
                        #flag = 1
                        break
                    if flag == 0:
                        tmptime = FSize[rg_id]
                        tmpearn = Credit[newcredit[i][1]][0]
                        tpid = i
                        flag = 1
                    if Deadline[dl_id][1] <= timespend + slot:
                        timespend = timespend + FSize[rg_id]
                        credit_earned = credit_earned + Credit[newcredit[i][1]][0]
                        newcredit[i][0] = -1
                        id_got.append(rg_id)
                        tid_got.append(dl_id)
                        flag2 = 1
                        break
        if flag == 1 and flag2 == 0:
            timespend = timespend + tmptime
            credit_earned = credit_earned + tmpearn
            newcredit[tpid][0] = -1
            print "slot not good"
        if tmpcredit == newcredit:
            timespend = timespend + 0.1
    return credit_earned

def Runtime_maxunitcredit(Credit, FD, FSize, Deadline, MD):
    timespend = 0.0
    newcredit = copy.deepcopy(Credit)
    for i in range(len(newcredit)):
        newcredit[i][0] = float(newcredit[i][0]/FSize[i])
    credit_earned = 0
    id_got = []
    tid_got = []
    flag = 0
    while timespend < MD:
        sortByColumn(newcredit, 0)
        #print newcredit
        tmpcredit = copy.deepcopy(newcredit)
        for i in range(len(newcredit)):
            dl_id = FD[newcredit[i][1]]
            rg_id = newcredit[i][1]
            #print dl_id
            if Deadline[dl_id][1] <= timespend:
                newcredit[i][0] = -1
            elif Deadline[dl_id][0] > timespend:
                continue
            else:
                if FSize[rg_id] > Deadline[dl_id][1] - timespend:
                    continue
                else:
                    if newcredit[i][0] == -1:
                        flag = 1
                        break
                    timespend = timespend + FSize[rg_id]
                    credit_earned = credit_earned + Credit[newcredit[i][1]][0]
                    newcredit[i][0] = -1 
                    id_got.append(rg_id)
                    tid_got.append(dl_id)
                    break
        if tmpcredit == newcredit:
            timespend = timespend + 0.1
#        if flag == 1:
#            break
#    print newcredit
#    print id_got
#    print tid_got
#    print credit_earned
#    print MD
#    print timespend
    return credit_earned

def suitable(timespend, dl, fsize, confl_List):
    
    if len(confl_List) == 0 :
        confl_List.append([dl-fsize, dl])
        return True
    sortByColumn2(confl_List, 0)
    interval = []
    interval.append(confl_List[0][0]- timespend)
#    print interval
    for i in range(len(confl_List)-1):
        interval.append(confl_List[i+1][0] - confl_List[i][1])
    #print confl_List
    #print interval
    if dl < confl_List[0][0]:
        confl_List.append([dl-fsize, dl])
        return True
    if dl > confl_List[-1][1]:
        #print dl
        #print confl_List
        if dl - fsize >= confl_List[-1][1]:
            confl_List.append([dl-fsize,dl])
            return True
        else:
            #print dl, fsize
            #print confl_List
            for i in range(len(confl_List)-1, -1, -1):
                if interval[i] >= fsize:
                    confl_List[i][0] = confl_List[i][0] - fsize
                    return True
            return False
                    
    flag0 = 0
    tpid = 0
    for i in range(len(confl_List)):
        if dl >= confl_List[i][0] and dl <= confl_List[i][1]:
            #print confl_List
            #print fsize, dl
            #print interval
            if fsize <= interval[i]:
                confl_List[i][0] = confl_List[i][0] - fsize
                return True
            else:
                for j in range(i-1, -1, -1):
                    if interval[j] >= fsize:
                        #print i, j, fsize, dl
                        #print confl_List
                        #print interval
                        
                        confl_List[j][0] = confl_List[j][0] - fsize
                        return True
            break
        else:
            if i < len(confl_List) - 1:
                if dl > confl_List[i][1] and dl < confl_List[i+1][0]:
                    #flag0 = 1
                    if dl - confl_List[i][1] >= fsize:
                        confl_List.append([dl- fsize,dl])
                    else:
                        for k in range(i, -1, -1):
                            if interval[k] >= fsize:
                                confl_List[k][0] = confl_List[k][0] - fsize
                                return True
                    break
                
    return False
                
def Runtime_greedyunitcredit(Credit, FD, FSize, Deadline, MD):
    timespend = 0.0
    newcredit = copy.deepcopy(Credit)
    for i in range(len(newcredit)):
        newcredit[i][0] = float(newcredit[i][0]/FSize[i])
    credit_earned = 0
    id_got = []
    tid_got = []
    flag = 0
    #sortByColumn(newcredit,0)
    ConflicList = []
    while timespend < MD:
        sortByColumn(newcredit, 0)
        #print newcredit
        tmpcredit = copy.deepcopy(newcredit)
        confl_List = []
        wait_list = []
        for i in range(len(newcredit)):
            dl_id = FD[newcredit[i][1]]
            rg_id = newcredit[i][1]
            #print dl_id
            if Deadline[dl_id][1] <= timespend:
                newcredit[i][0] = -1
            elif Deadline[dl_id][0] > timespend:
                continue
            else:
                
                if FSize[rg_id] > Deadline[dl_id][1] - timespend:
                    continue
                else:
                    if newcredit[i][0] == -1:
                        #flag = 1
                        break
                    if suitable(timespend, Deadline[dl_id][1], FSize[rg_id], confl_List):
                        wait_list.append(i)
        #print confl_List
        if len(wait_list) >0:
            newcredit[wait_list[-1]][0] = -1
            timespend = timespend + FSize[newcredit[wait_list[-1]][1]]
            credit_earned = credit_earned + Credit[newcredit[wait_list[-1]][1]][0]
            #break
        else:
        #if tmpcredit == newcredit:
            timespend = timespend + 0.1
    return credit_earned
    

def Runtime_maxcreditunitdeadline(Credit, FD, FSize, Deadline, MD):
    timespend = 0.0
    newcredit = copy.deepcopy(Credit)
    for i in range(len(newcredit)):
        newcredit[i][0] = float(newcredit[i][0]/FSize[i])
    credit_earned = 0
    id_got = []
    tid_got = []
    flag = 0
    while timespend < MD:
        sortByColumn(newcredit, 0)
        #print newcredit
        tmptime = 0
        tmpearn = 0
        tpid = 0
        tmpval= 0.0
        flag = 0
        tmpcredit = copy.deepcopy(newcredit)
        for i in range(len(newcredit)):
            dl_id = FD[newcredit[i][1]]
            rg_id = newcredit[i][1]
            #print dl_id
            if Deadline[dl_id][1] <= timespend:
                newcredit[i][0] = -1
            elif Deadline[dl_id][0] > timespend:
                continue
            else:
                if FSize[rg_id] > Deadline[dl_id][1] - timespend:
                    continue
                else:
                    if newcredit[i][0] == -1:
                    #    flag = 1
                        break
                    val = newcredit[i][0]* math.exp(-(float(Deadline[dl_id][1] - timespend))/7)
                    if val > tmpval:
                        tmpval = val
                        tmptime = FSize[rg_id]
                        tmpearn = Credit[newcredit[i][1]][0]
                        tpid = i
                        flag = 1
#                    timespend = timespend + FSize[rg_id]
#                    credit_earned = credit_earned + Credit[newcredit[i][1]][0]
                    
#                    newcredit[i][0] = -1 
#                    id_got.append(rg_id)
#                    tid_got.append(dl_id)
#                    break
        if flag == 1 :
            timespend = timespend + tmptime
            credit_earned = credit_earned + tmpearn
            newcredit[tpid][0] = -1
        if tmpcredit == newcredit:
            timespend = timespend + 0.1

    return credit_earned

def Runtime_maxcredit(Credit, FD, FSize, Deadline, MD):
    timespend = 0.0
    newcredit = copy.deepcopy(Credit)
    credit_earned = 0
    id_got = []
    tid_got = []
    flag = 0
    while timespend < MD:
        sortByColumn(newcredit, 0)
        #print newcredit
        tmpcredit = copy.deepcopy(newcredit)
        for i in range(len(newcredit)):
            dl_id = FD[newcredit[i][1]]
            rg_id = newcredit[i][1]
            #print dl_id
            if Deadline[dl_id][1] <= timespend:
                newcredit[i][0] = -1
            elif Deadline[dl_id][0] > timespend:
                continue
            else:
                if FSize[rg_id] > Deadline[dl_id][1] - timespend:
                    continue
                else:
                    if newcredit[i][0] == -1:
                        flag = 1
                        break
                    timespend = timespend + FSize[rg_id]
                    credit_earned = credit_earned + newcredit[i][0]
                    newcredit[i][0] = -1
                    id_got.append(rg_id)
                    tid_got.append(dl_id)
                    break
        if tmpcredit == newcredit:
            timespend = timespend + 0.1
#        if flag == 1:
#            break
#    print newcredit
#    print id_got
#    print tid_got
#    print credit_earned
#    print MD
#    print timespend
    return credit_earned

NPhone = 10
MaxPhoto = 60
MinPhoto = 50
MaxCredit = 1001
MinCredit = 100
NTask = 15
start = 0.0
Credit = [None]*NPhone
Deadline = [None]*NTask
FSize = [None]*NPhone
FD = [None]*NPhone
FTask = [None]*NPhone
MaxDu = 7
MinDu = 3
MD = 0.0
EarlyDL = []
for i in range(NTask):
    Deadline[i] = [float(start), float(start+ random.randrange(MinDu,MaxDu))]
#    if Deadline[i][1] > MD:
#        MD = Deadline[i][1]
    start =float( start + random.randrange(0,4))
    EarlyDL.append([Deadline[i][1], i])
sortByColumn2(EarlyDL, 0)
MD = EarlyDL[-1][0]

for i in range(NPhone):
    numphot = random.randrange(MinPhoto,MaxPhoto)
    Credit[i] = [None]*numphot
    FTask[i] = [None]*NTask
    for k in range(NTask):
        FTask[i][k] = []
    FSize[i] = [0.0]*numphot
    FD[i] = [0]*numphot
    for j in range(numphot):
        Credit[i][j] = [random.randrange(MinCredit, MaxCredit), j]
        FSize[i][j] = random.uniform(1.2,1.6)
        FD[i][j] = j%NTask
        FTask[i][j%NTask].append([Credit[i][j][0],j, FSize[i][j]])
    

maxcredit_tot = 0
maxunitcredit_tot = 0
maxunitdeadline_tot = 0
earlydl_tot = 0
maxslotcredit_tot = 0
maxslotunitcredit_tot = 0
greedy = 0
#print Runtime_greedyunitcredit(Credit[0], FD[0], FSize[0], Deadline, MD)
print 'hello'
for i in range(NPhone):
    maxcredit_tot = maxcredit_tot +  Runtime_maxcredit(Credit[i], FD[i], FSize[i], Deadline, MD)
    maxunitcredit_tot = maxunitcredit_tot +  Runtime_maxunitcredit(Credit[i], FD[i], FSize[i], Deadline, MD)
    earlydl_tot = earlydl_tot + Runtime_deadline(FTask[i], Deadline, EarlyDL)
    maxslotcredit_tot = maxslotcredit_tot + Runtime_maxslotcredit(Credit[i], FD[i], FSize[i], Deadline, MD, 10)
    maxslotunitcredit_tot = maxslotunitcredit_tot + Runtime_maxunitslotcredit(Credit[i], FD[i], FSize[i], Deadline, MD, 10)
    maxunitdeadline_tot = maxunitdeadline_tot + Runtime_maxcreditunitdeadline(Credit[i], FD[i], FSize[i], Deadline, MD)
    greedy = greedy + Runtime_greedyunitcredit(Credit[i], FD[i], FSize[i], Deadline, MD)

print greedy
print maxunitcredit_tot
print maxunitdeadline_tot
print maxslotunitcredit_tot
print maxcredit_tot
print maxslotcredit_tot
print earlydl_tot

print EarlyDL
