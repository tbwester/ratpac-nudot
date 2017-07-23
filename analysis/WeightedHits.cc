// ====================================================
//
// WeightedHits.cc
// Thomas Wester July 2017
// 
// gets weighted hits on the tpb plate from the source
// to plate simulation based on the plate to PMT 
// simulation which puts the weights in weights.txt.
//
// ====================================================

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <stdlib.h>

#include "TH1.h"
#include "TFile.h"
#include "TMath.h"
#include "TNtuple.h"
#include "TDatime.h"
#include "TRandom.h"

#include "helper.hh" /* rweight, datetime, vecfromfile */

typedef std::vector<double> dblvec;

TNtuple* GetPhotonInfo(string filepath);

void WeightedHits(string filepath) {
    TRandom3 r;
    r.SetSeed(time(NULL));

    stringstream ifilename;
    ifilename << filepath << "weights.txt";
    std::vector<dblvec> weights = vecfromfile(ifilename.str().c_str());

    //Fill ntuple with values from output.root file
    TNtuple* ntp = GetPhotonInfo(filepath);

    TH1F* hwh = new TH1F("hwh", "weighted hit dist", 100, 0, 1);
    float x, y, xh, yh;
    ntp->SetBranchAddress("x0", &x);
    ntp->SetBranchAddress("y0", &y);
    ntp->SetBranchAddress("xh", &xh);
    ntp->SetBranchAddress("yh", &yh);

    //All photons start from the same point, so use the first event
    ntp->GetEntry(0);
    double srcr = TMath::Sqrt(x*x + y*y);

    double whits = 0.0;
    for (int i = 0; i < ntp->GetEntries(); i++) {
        ntp->GetEntry(i);
        double pltr = TMath::Sqrt(xh*xh + yh*yh);
        double weightedhit = rweight(pltr, weights);
        //std::cout << weightedhit << " ";
        hwh->Fill(weightedhit);
        whits += weightedhit;
    }

    std::cout << "r " << srcr << "\thits " << whits 
              << "\ttotal " << ntp->GetEntries() << std::endl;

    //Append numbers to text file
    stringstream ofilename;
    ofilename << filepath << "pltweights.txt";
    std::ofstream outfile;
    outfile.open(ofilename.str().c_str(), std::ios_base::app);
    outfile << srcr << "," << whits << "," << ntp->GetEntries() << std::endl;
    outfile.close();

    stringstream of2;
    of2 << filepath << "ntuple_" << int(srcr * 100.) << ".root";
    TFile* myfile = new TFile(of2.str().c_str(), "RECREATE");
    ntp->Write();
    hwh->Write();
    myfile->Close();
}

TNtuple* GetPhotonInfo(string filepath) {
    //Create NTuple for photon data 
    TNtuple *ntuple = new TNtuple("dph","photon data","x0:y0:z0:xh:yh:zh:pz0");

    stringstream rootfilename;
    rootfilename << filepath << "../output.root";
    RAT::DSReader reader("~/ratpac-nudot/output.root");
    int nevents = reader.GetTotal();

    RAT::DS::Root *ds = reader.NextEvent();

    //Define ntuple variables
    float x0, y0, z0, xh, yh, zh;
    float pz0;
    bool hit = false;
    while (ds != 0) {
        // create track navigation interface
        RAT::TrackNav nav(ds);

        RAT::TrackCursor c = nav.Cursor(false);
        RAT::TrackNode *n = c.Here();
        n = c.FindNextTrack();
        while (n != 0) {
            x0 = n->GetEndpoint()[0];
            y0 = n->GetEndpoint()[1];
            z0 = n->GetEndpoint()[2];
            pz0 = n->GetMomentum()[2] / n->GetKE();
            //get final tracknode parameters

            n = c.GoTrackEnd();
            n->GetVolume() == "pvPMT00" ? hit = true : hit = false;
            if (hit) {
                // photon propagates once inside the PMT volume
                // go back one step to get the hit position on the plate
                n = c.GoPrev();
                xh = n->GetEndpoint()[0];
                yh = n->GetEndpoint()[1];
                zh = n->GetEndpoint()[2];
                std::vector<float> fillvec = {x0, y0, z0, xh, yh, zh, pz0}; 
                ntuple->Fill(&fillvec[0]);
            }
            n = c.FindNextTrack();
        }
        ds = reader.NextEvent();
    }
    return ntuple;
}
