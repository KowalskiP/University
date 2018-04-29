with open('in.txt') as txt:
    data = txt.readlines()

N = int(data[0])
GR = [[None for i in range(N)] for j in range(N)]
for i in range(N):
    temp = data[1+i].split(' ')

    j = 0
    if temp[j] == '0\n':
        continue
    while temp[j] != '0\n':
        GR[int(temp[j])-1][i] = int(temp[j+1])
        # GR[i][int(temp[j])-1] = int(temp[j+1])
        j += 2

print(GR)

s = int(data[-2]) - 1
t = int(data[-1]) - 1
print(s)
print(t)

S = []
F = [i for i in range(N)]
S.append(s)
F.remove(s)
dm = [-1 for i in range(N)]
dm[s] = 100000


def MAX(G):
    z = -1000
    j = 0
    for i in range(len(G)):
        print(G[i])
        print('dm ' + str(dm[G[i]]))
        if z < dm[G[i]]:
            j = G[i]
            z = dm[G[i]]
    return j

print(S)
print(F)
print(dm)
# суммы на минимум
# минимум на максимум
for i in range(N):
    if i != s and GR[s][i] is not None:
        dm[i] = GR[s][i]
print(dm)
for w in range(len(F)):
    for v in range(len(S)):
        if GR[v][w] is not None:
            dm[w] = min(dm[v], GR[v][w])
print(dm)
for k in range(N-1):
    print(F)
    print('k ' + str(k))
    w = MAX(F)
    print('w ' + str(w))
    F.remove(w)
    for v in F:
        if GR[w][v] is None:
            continue
        print(dm)
        print('v ' + str(v))
        print(dm[v])
        print(dm[w])
        print(GR[w][v])
        if min(dm[w], GR[w][v]) < dm[v]:
            dm[v] = min(dm[w], GR[w][v])
        print(dm[v])
print(dm)
