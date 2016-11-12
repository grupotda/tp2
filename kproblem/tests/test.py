import sys
def cmp(a,b):
    return a[0] < b[0]

for i in range(len(sys.argv)-1):
    f = open(sys.argv[i+1])
    o = open(sys.argv[i+1] + "_times","w+")
    f.readline()
    f.readline()
    x = []
    for i in range(100):
        f.readline()
        n = int(f.readline().split()[1])
        c = int(f.readline().split()[1])
        print f.readline()
        time = int(f.readline().split()[1])
        f.readline()
        f.readline()
        x.append((c,time))
    x.sort()
    for i in x:
        o.write(str(i[0]) + " " + str(i[1]) + "\n")
