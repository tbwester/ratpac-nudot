import sys
import re

filepath = sys.argv[1]

# get log file lines
with open(filepath+"gqe_log.txt") as f:
    lines = f.readlines()
    
# string to be written to new file
datastr = 'd\tweight\thits\n'

# regex to get relevant numbers from log file
for i in range(len(lines)):
    dist = re.search("d=\d+", lines[i])
    weight = re.search("W: \d+.\d+", lines[i])
    hits = re.search("H: \d+", lines[i])
    try:
        datastr += dist.group(0)[2:] + '\t' + weight.group(0)[3:] + '\t' + \
                hits.group(0)[3:] + '\n'
    except:
        print lines[i]

# write datastr to file
with open(filepath+"gqe_data.txt", "w") as f:
    f.write(datastr)
