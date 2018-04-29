__author__ = 'Антон'
with open('in.txt') as txt:
    data = txt.readlines()

N = int(data[0])
GR = [[-1 for i in range(N)] for j in range(N)]
for i in range(N):
    temp = data[1+i].split(' ')
    temp = [i for i in temp if i != '']
    j = 0
    if temp[j] == '0\n':
        continue
    while temp[j] != '0\n':
        GR[int(temp[j])-1][i] = int(temp[j+1])
        j += 2


s = int(data[-2]) - 1
t = int(data[-1]) - 1

S = []
F = [i for i in range(N)]
S.append(s)
F.remove(s)
dm = [-1 for i in range(N)]


def MAX(G):
    max_dist = -1000
    u = 0
    for v in G:
        if max_dist < dm[v]:
            u = v
            max_dist = dm[v]
    return u

def WEIGHT(p):
    m = GR[p[0]][p[1]]
    for i in range(2,len(p)-1):
        if m> GR[p[i]][p[i+1]]:
            m = GR[p[i]][p[i+1]]
    return m

pred = [-1 for i in range(N)]

# суммы на минимум
# минимум на максимум
for i in range(N):
    if i != s and GR[s][i] >= 0:
        dm[i] = GR[s][i]
        pred[i] = s

for k in range(N-1):
    w = MAX(F)
    F.remove(w)
    for v in F:
        if min(dm[w], GR[w][v]) > dm[v]:
            dm[v] = min(dm[w], GR[w][v])
            pred[v] = w

with open("out.txt", 'w') as txt:
    if dm[t] == -1:
        txt.writelines('N')
    else:
        txt.writelines('Y\n')
        path = []
        v = t
        while v != s:
            path.append(v)
            v = pred[v]
        path.append(v)
        path.reverse()
        txt.writelines(' '.join(map(lambda x: str(x + 1), path)) + '\n')
        # print(' '.join(map(lambda x: str(x + 1), path)))
        txt.writelines(str(WEIGHT(path)))
        # print(WEIGHT(path))