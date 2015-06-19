import sys
import zmq
import ratchromadata_pb2
import photonHit_pb2
import random

context = zmq.Context().instance()

socket =context.socket(zmq.REP)
socket.bind("tcp://*:5554")
def MakePhotons(num_pmts):
    phits = photonHit_pb2.PhotonHits()
    pmt_id = 0
    for x in xrange (0,num_pmts):
        pmt_id += 1
        phits.photon.add()
        phits.photon.count = random.randint(0,25)
        for x in xrange (0, phits.photon.count):
            phits.photon.PMTID = pmt_id
            phits.photon.Time = random.uniform(0,30)
            phits.photon.KineticEnergy = random.uniform(2.61*(10**-6),3.22*(10**-6))
            #converted to MeV
            phits.photon.posX = random.uniform(-1,1)
            phits.photon.posY = random.uniform(-1,1)
            phits.photon.posZ = random.uniform(-1,1)
            phits.photon.momX = ((phits.photon.KineticEnergy/3.0)
                                 **0.5)
            phits.photon.momY = ((phits.photon.KineticEnergy/3.0)
                                 **0.5)
            phits.photon.momZ = ((phits.photon.KineticEnergy/3.0)
                                 **0.5)
            phits.photon.polX = random.uniform(0,((1/3.0)**.5))
            phits.photon.polY = random.uniform(0,((1/3.0)**.5))
            phits.photon.polZ = ((1 - phits.photon.polX**2 -
                                  phits.photon.polY**2)**.5)
            phits.photon.trackID = random.randint(0,25)
            phits.photon.origin = random.randint(0,2)
    return phits
def Server():
    print "opened"
    #need to get PMT_Count here
    num_pmts = int(socket.recv())
    socket.send(b"")
    print "got num. of pmts: ",num_pmts
    msg = socket.recv()
    print "message size: ",msg.ByteSize()
    print ParseFromString(msg), "\n"
    socket.send(b"")

    print "making some fake photons\n"
    phits = MakePhotons(num_pmts)
    #ship em
    socket.send(phits.SerializeToString())

Server()
