import numpy as np
from scipy.spatial.distance import pdist, squareform
#import matplotlib.pyplot as plt
import operator
import multi_query_lib



def sortByColumn(bigList, *args):
    bigList.sort(key=operator.itemgetter(*args), reverse = True)

def minimum_spanning_tree(X, copy_X=True):
    """X are edge weights of fully connected graph"""
    if copy_X:
        X = X.copy()
    print X.shape[0], X.shape[1]

    if X.shape[0] != X.shape[1]:
        raise ValueError("X needs to be square matrix of edge weights")
    n_vertices = X.shape[0]
    spanning_edges = []
    
    # initialize with node 0:                                                                                         
    visited_vertices = [0]                                                                                            
    num_visited = 1
    # exclude self connections:
    diag_indices = np.arange(n_vertices)
    X[diag_indices, diag_indices] = np.inf
    
    while num_visited != n_vertices:
        new_edge = np.argmin(X[visited_vertices], axis=None)
        # 2d encoding of new_edge from flat, get correct indices                                                      
        new_edge = divmod(new_edge, n_vertices)
        new_edge = [visited_vertices[new_edge[0]], new_edge[1]]                                                       
        # add edge to tree
        spanning_edges.append(new_edge)
        visited_vertices.append(new_edge[1])
        # remove all edges inside current tree
        X[visited_vertices, new_edge[1]] = np.inf
        X[new_edge[1], visited_vertices] = np.inf                                                                     
        num_visited += 1
    return np.vstack(spanning_edges)
import copy
def opt_mst(diff, SZ, CP, id2user):
    opt_weight = 0
    opt_list = []
    N = len(SZ)
    sm = None
    for ind in range(N):
        t_cp = copy.deepcopy(CP)
        LST = []
        LST.append(ind)
        td = copy.deepcopy(diff[ind])
        if SZ[ind] > CP[id2user[ind]]:
            continue
        t_cp[id2user[ind]] = t_cp[id2user[ind]] - SZ[ind]
        flag1 = 0
        while 1:
            count = 0
            flag = 0
            while 1:
                mt = max(td)
                if mt == 0 :
                    flag1 = 1
                    break
                tmp_id = td.index(mt)
                if SZ[tmp_id] > t_cp[id2user[tmp_id]]:
                    td[tmp_id] = 0
                else:
                    t_cp[id2user[tmp_id]] = t_cp[id2user[tmp_id]] - SZ[tmp_id]
                    LST.append(tmp_id)
                    
                    for x in range(N):
                        td[x] = min(td[x], diff[tmp_id][x])
                    break
#                count = count + 1
#                if count == N -1 :
#                    flag = 1
#                    break
#            if flag == 1:
#                print "no solution for " + str(ind)
#                continue
            if flag1 == 1:
                print "got the tree"
                break
        P_dis = []
        if len(LST) <= 1:
            print "no solution for " + str(ind)
            continue
        print "LST"
        print LST
        print diff[LST[0]][LST[1]]
        for x in range(0, len(LST)-1):
            for y in range(x+1, len(LST)):
                P_dis.append(diff[LST[x]][LST[y]])
#        print "P_dis"
#        print P_dis
        SF = squareform(P_dis)
        edge_list = minimum_spanning_tree(SF)
        tmp_weight = 0
        for edge in edge_list:
            ii,jj = edge
            tmp_weight = tmp_weight+ SF[ii][jj]
        if tmp_weight > opt_weight:
            opt_weight = tmp_weight
            opt_list = copy.deepcopy(LST)
            sm = copy.deepcopy(SF)
    
    Priority = []
    ps = []
    print opt_list
    for x in range(len(sm)):
    #    Priority.append([sum(sm[x]),x])
	if SZ[opt_list[x]] == 0:
            ps.append(0)
        else:
            ps.append(sum(sm[x]))
    for x in range(len(ps)):
        Priority.append([ps[x]/sum(ps), opt_list[x]])
    sortByColumn(Priority, 0)
    return Priority

def call_mst(data, deadline):
    print "data="+str(data)
    if (len(data) == 0):
        return ([], [])
    dist = [None]*len(data)
    SZ = [0]*len(data)
    name = data[0][0]
    id2user = []
    ct = 0
    for i in range(len(data)):
        dist[i] = [0]*len(data)
        if data[i][0] == name:
            id2user.append(ct)
        else:
            ct = ct + 1
            id2user.append(ct)
            name = data[i][0]
        SZ[i] = int(data[i][6])
        for j in range(len(data)):
            dist[i][j] = (multi_query_lib.pair_dist(data[i], data[j]))
    CP = []
    for i in range(ct+1):
        CP.append(int(deadline)*max(SZ))
    Priority = opt_mst(dist, SZ, CP, id2user)
    result = {}
    
    for i in range(len(Priority)):
        pid = Priority[i][1]
        if data[pid][0] not in result:
            result[data[pid][0]]  = ''
        result[data[pid][0]]  += str(data[pid][1]) + ':' + str(int(Priority[i][0]*1000)) + ':' + deadline + '|'
     
    for i in result:
        result[i] = result[i][:-1]
        
    return result, None
    
def opt_mst2(diff, SZ,CP, id2user):
    opt_weight = 0
    opt_list = []
    N = len(SZ)
    for ind in range(1,pow(2,N)):
        sz_t = CP
        B = str(bin(ind))
        B = B[2:]
        L = len(B)
        flag = 0
        LST = []
        for i in range(L):
            if B[i] == '1':
                sz_t[id2user[L-1-i]] = sz_t[id2user[L-1-i]] - SZ[L-1-i]
                if sz_t[id2user[L-1-i]] < 0:
                    flag = 1
                    break
                LST.append(L-1-i)
        if flag == 1:
            continue
        P_dis = []
        for x in range(0, len(LST)-1):
            for y in range(x+1, len(LST)):
                P_dis.append(diff[LST[x]][LST[y]])
        #print "hello p"
        #print P_dis
        if len(P_dis) == 0:
            continue
        SF = squareform(P_dis)
        
        edge_list = minimum_spanning_tree(SF)
        tmp_weight = 0
        for edge in edge_list:
            ii,jj = edge
            tmp_weight = tmp_weight+ SF[ii][jj]
        if tmp_weight > opt_weight:
            opt_weight = tmp_weight
            opt_list = LST
    users = [None]*len(SZ)
    print opt_list
#    for i in opt_list:
#        users[id2user[i]] 
import random
def main():
    L = 5
    CP = []
    id2user = []
    SZ = []
    count = 0
#    diff = []
    for i in range(L):
        CP.append(100*random.random())
        N = int(5*random.random())
        for j in range(N):
            id2user.append(i)
            SZ.append(20*random.random())
        count = count + N
    diff = [0]*count
    for i in range(count):
        diff[i] = [0]*count
        
    for i in range(0, count-1):
        for j in range(i + 1, count):
            diff[i][j] = (5*random.random())
            diff[j][i] = diff[i][j]
            
            
    print count
    print diff
   # dif = squareform(diff)
    #print dif[0][2]
    opt_mst(diff, SZ,CP, id2user)
"""
def test_mst():
    P = np.random.uniform(size=(50, 2))
    print len(P)
    print "=="
#    print P
    print "=="
    Z= pdist(P)
    print Z
    X = squareform(Z)
    print len(X)
    print "=="
#    for i in X:
#    	print len(i)
#    	print i
    	
#    print X
    edge_list = minimum_spanning_tree(X)
    plt.scatter(P[:, 0], P[:, 1])
    
    for edge in edge_list:
        print edge
        i, j = edge
        plt.plot([P[i, 0], P[j, 0]], [P[i, 1], P[j, 1]], c='r')
    plt.show()

if __name__ == "__main__":
    main()
"""
