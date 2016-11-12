from random import randint as randint
import sys

def gen(n):
    l = []
    for i in range(n):
        l.append([])
        for j in range(n):
            l[i].append(randint(1,500))
    for i in range(n):
        l[i][i] = 0
    return l

n = int(sys.argv[1])
l = gen(n)
out = open(sys.argv[2],"w+")
for i in range(n):
    line = ""
    for j in range(n):
        line += str(l[i][j]) + " "
    line = line.strip()
    out.write(line + "\n")

