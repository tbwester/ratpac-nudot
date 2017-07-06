#!/usr/bin/python

import os,sys
import ROOT as rt
rt.gSystem.Load('libRATEvent')
from ROOT.RAT import DSReader
import numpy as np

reader = DSReader("/home/twester/ratpac-nudot/output.root");

nevents = reader.GetTotal()

f = open('log.txt', 'a')
totalpe = 0
pmtlist = []
hitcounts = []
for iev in xrange(0,nevents):
    dsroot = reader.NextEvent()
    mc = dsroot.GetMC()
    npes = mc.GetNumPE()
    npmts = mc.GetMCPMTCount()
    #for i in range(0, npmts):
    if npmts > 0:
        pmtid = mc.GetMCPMT(0).GetID() 
        if not pmtid in pmtlist:
            pmtlist.append(pmtid)
            hitcounts.append(1)
        else:
	    index = 0
            for i in range(0, len(pmtlist)):
                if pmtid == pmtlist[i]:
                    index = i
                    break
            hitcounts[index] += 1
    totalpe += npes
    #print "Event ",iev
    #print "  nPEs=",npes," npmts=",npmts," list: ",pmtlist

line = str(sys.argv[1]) + '\t' + str(pmtlist) + '\t' + str(hitcounts) + '\t' + str(totalpe) + '\n'
f.write(line)
f.close()
#print str(totalpe) + "/" + str(nevents)
