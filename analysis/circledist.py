import numpy as np

weights = np.genfromtxt("gqe_data.txt", names=["d", "weight", "hits", "r"], skip_header=1)

def interpolate(x):
    foundpts = False
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    for i in range(len(weights)):
        if weights[i][3] > x and i != 0:
            x1 = weights[i-1][3]
            y1 = weights[i-1][1]
            x2 = weights[i][3]
            y2 = weights[i][1]
            foundpts = True
            break

    if not foundpts:
        return weights[-1][1]

    return y1 + (x - x1) * ( ( y2 - y1) / (x2 - x1) )

total = 0
count = 0
rlist = []
n = 100000
while count < n:
    x = np.random.uniform() * 3.
    y = np.random.uniform() * 3.
    #theta = np.random.uniform() * 2. * np.pi

    if np.sqrt(x**2 + y**2) > 3:
        continue

    count += 1

    #x = r * np.cos(theta)
    #y = r * np.sin(theta)

    intf = interpolate(np.sqrt(x**2 + y**2))

    rlist.append(intf)
    total += intf

print total / float(n)

"""
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_yscale("log", nonposy='clip')
binwidth=5
ax.hist(rlist, bins=np.arange(min(weights["weight"]), max(weights["weight"]) + binwidth, binwidth))

plt.savefig("hist.pdf")
"""
