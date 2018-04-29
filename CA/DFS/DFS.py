__author__ = 'Антон'
nodes = []
with open('in.txt') as txt:
    N = int(txt.readline())
    M = int(txt.readline())
    data=[[1 for i in range(M+2)] for j in range(N+2)]
    for i in range(1,N+1):
        for j in range(1,M+1):
            data[i][j]=(int(txt.read(2)))
    start = [int(txt.read(2)),int(txt.read(2))]
    end = [int(txt.read(2)), int(txt.read(2))]

def m_search(v):
    result.append(v)
    data[v[0]][v[1]] = 2
    while len(result)>0:
        if result[len(result)-1] == end:
            break
        f = False
        for i in range(4):
            temp = [result[len(result)-1][0]+p[i],result[len(result)-1][1]+p[i+4]]
            if data[temp[0]][temp[1]] == 0:
                result.append(temp)
                data[temp[0]][temp[1]] = 2
                f = True
                break
        if not f:
            result.pop()

p = [-1, 1, 0, 0, 0, 0, -1, 1]
result = []

m_search(start)
with open("out.txt",mode='w') as txt:
    if result != []:
        txt.write('Y'+'\n')
        for i in result:
            txt.write(str(i[0])+' '+str(i[1])+'\n')
    else:
        txt.write('N')