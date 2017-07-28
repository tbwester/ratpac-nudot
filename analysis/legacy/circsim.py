import sys
import numpy as np
import matplotlib.pylab as plt

#filepath = sys.argv[1]

weights = np.genfromtxt("gqe_data368.txt", names=["r", "weight", "hits"])

def interpolate(x):
    foundpts = False
    x1 = y1 = x2 = y2 = 0
    for i in range(len(weights)):
        if weights[i]["r"] > x and i != 0:
            x1 = weights[i-1][0]
            y1 = weights[i-1][1]
            x2 = weights[i][0]
            y2 = weights[i][1]
            foundpts = True
            break

    if not foundpts:
        return weights[-1][1]

    return y1 + (x - x1) * ( ( y2 - y1) / (x2 - x1) )

def sample_points(n, radius, sig):
    total = 0
    count = 0
    rlist = []
    pelist = []
    while count < n:
        ## Distribute as bvn
        x, y = np.random.multivariate_normal([0,0], [[sig,0], [0,sig]])

        ## Distribute uniform
        #x =  np.random.uniform() * radius
        #y =  np.random.uniform() * radius

        if np.sqrt(x**2 + y**2) > radius:
            continue

        count += 1
        ther = np.sqrt(x**2 + y**2)

        intf = interpolate(ther)

        rlist.append(ther)
        pelist.append(np.random.poisson(intf * 0.1503 * 1.34))
        total += intf

    fig = plt.figure()
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    #ax2.set_yscale("log", nonposy='clip')
    pe = "Mean PE: %.2f" % ((total / float(n)) * 0.1503 * 1.34)
    ax2.text(0.2, 0.7, pe, bbox=dict(facecolor='w'), transform=ax2.transAxes)
    binwidth1=0.01
    binwidth2=2
    ax1.hist(rlist, bins=np.arange(min(rlist), max(rlist) + binwidth1, binwidth1))
    ax2.hist(pelist, bins=np.arange(min(pelist), max(pelist) + binwidth2, binwidth2))
    ax2.plot([np.mean(pelist), np.mean(pelist)], [0, n**(1/3)], color='r')

    ax3.errorbar(weights["r"], weights["weight"], fmt="-", color='b')
    ax4.hist2d(pelist, rlist, bins=100)


    delta = 0.05 * max(pelist)
    ax2.set_xlim(min(pelist) - delta, max(pelist) + delta)
    ax4.set_xlim(min(pelist) - delta, max(pelist) + delta)

    ax1.set_xlabel("Source Position (cm)")
    ax2.set_xlabel("\# PE")
    ax3.set_xlabel("Source Position (cm)")
    ax3.set_ylabel("Weighted Hits")
    ax4.set_xlabel("\# PE")
    ax4.set_ylabel("Source Position (cm)")

    plt.tight_layout()
    plt.savefig("out/hist" + str(int(sig * 1000)) + ".png", transparent=False)

if __name__=="__main__":
    for i in np.arange(0.5, 0.8, 0.1):
        sample_points(50000, 0.3, i)
