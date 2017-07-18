import sys
import numpy as np

filepath = sys.argv[1]

def interpolate(x):
    foundpts = False
    x1 = y1 = x2 = y2 = 0
    for i in range(len(weights)):
        if weights[i][0] > x and i != 0:
            x1 = weights[i-1][0]
            y1 = weights[i-1][1]
            x2 = weights[i][0]
            y2 = weights[i][1]
            foundpts = True
            break

    if not foundpts:
        # we are outside the interpolate curve
        return 0.0 #weights[-1][1]

    return y1 + (x - x1) * ( ( y2 - y1) / (x2 - x1) )

weights = np.genfromtxt(filepath + "pltweights.txt", \
        names=["r", "weight", "hits"])

total = 0
count = 0
rlist = []
n = 100000
while count < n:
    x = np.random.uniform() * 3.
    y = np.random.uniform() * 3.

    if np.sqrt(x**2 + y**2) > 3:
        continue

    count += 1
    intf = interpolate(np.sqrt(x**2 + y**2))

    rlist.append(intf)
    total += intf

avg_whits = total / float(n)
print avg_whits
