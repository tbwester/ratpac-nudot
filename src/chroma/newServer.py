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
        aphoton = phits.photon.add()
        aphoton.count = 1
        for x in xrange (0, aphoton.count):
            aphoton.PMTID = pmt_id
            aphoton.Time = random.uniform(0,30)
            aphoton.KineticEnergy = random.uniform(2.61*(10**-6),3.22*(10**-6))
            #converted to MeV
            aphoton.posX = random.uniform(-1,1)
            aphoton.posY = random.uniform(-1,1)
            aphoton.posZ = random.uniform(-1,1)
            aphoton.momX = ((aphoton.KineticEnergy/3.0)
                                 **0.5)
            aphoton.momY = ((aphoton.KineticEnergy/3.0)
                                 **0.5)
            aphoton.momZ = ((aphoton.KineticEnergy/3.0)
                                 **0.5)
            aphoton.polX = random.uniform(0,((1/3.0)**.5))
            aphoton.polY = random.uniform(0,((1/3.0)**.5))
            aphoton.polZ = ((1 - aphoton.polX**2 -
                                  aphoton.polY**2)**.5)
            aphoton.trackID = random.randint(0,25)
            aphoton.origin = 4
    return phits


def Server():
    print "opened"
    #need to get PMT_Count here
    num_pmts = int(socket.recv())
    socket.send(b"")
    print "got num. of pmts: ",num_pmts

    # get data for chroma
    msg = socket.recv()
    mychromadata = ratchromadata_pb2.ChromaData()
    mychromadata.ParseFromString(msg)
    print mychromadata, "\n"
    print "message size: ",mychromadata.ByteSize()
    phits = MakePhotons(num_pmts)
    socket.send(b"")
    socket.recv()
    print "making some fake photons\n"
    print phits
    #ship em
    socket.send(phits.SerializeToString())    

Server()
