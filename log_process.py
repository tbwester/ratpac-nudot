import re

with open("gqe_log.txt") as f:
    lines = f.readlines()
    
datastr = 'd\tweight\thits\n'

for i in range(len(lines)):
    dist = re.search("d=\d+.0", lines[i])
    weight = re.search("W: \d+.\d+", lines[i])
    hits = re.search("H: \d+", lines[i])
    datastr += dist.group(0)[2:] + '\t' + weight.group(0)[3:] + '\t' + \
                hits.group(0)[3:] + '\n'

with open("gqe_data.txt", "w") as f:
    f.write(datastr)
