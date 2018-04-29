__author__ = 'Антон'
nodes = []
with open('in.txt') as txt:
    N = int(txt.readline())
    M = int(txt.readline())
    data=[[1 for i in range(M+2)] for j in range(N+2)]
    for i in range(1,N+1):
        for j in range(1,M+1):
            data[i][j]=(int(txt.read(2)))
            if data[i][j] is 0:
                nodes.append([i,j])
    start = [int(txt.read(2)),int(txt.read(2))]
    end = [int(txt.read(2)), int(txt.read(2))]

k = len(nodes)

visited = [False for i in range(k)]

way = []
p = [-1, 1, 0, 0, 0, 0, -1, 1]
result = []

def maze_search(v):
    global result
    way.append(v)
    if v == end:
        result = [i for i in way]
        return result
    visited[nodes.index(v)]=True
    for j in range(4):
        temp = [v[0]+p[j], v[1]+p[j+4]]
        if data[temp[0]][temp[1]] == 0:
            if visited[nodes.index(temp)]:
                continue
            else:
                maze_search(temp)
    way.pop()

maze_search(start)
with open("out.txt",mode='w') as txt:
    if result != []:
        txt.write('Y'+'\n')
        for i in result:
            txt.write(str(i[0])+' '+str(i[1])+'\n')
    else:
        txt.write('N')