import matplotlib.pyplot as plt
import sys

f = open(sys.argv[1])
n = []
c = []
z = []
t = []
i = 0
for l in f:
    n.append(l.split()[0])
    if(l.split()[1] in c):
        print "ya estaba", i
    c.append(l.split()[1])
    z.append(l.split()[2])
    t.append(l.split()[3])
    i+=1
 
plt.plot(c,t,"r.")
plt.xlabel("C")
plt.ylabel("t [ms]")
ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_useOffset(False)
ax.get_xaxis().get_major_formatter().set_scientific(False)
plt.title("n = 200,r = 1000" )
plt.show()

