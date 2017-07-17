// ====================================================
//
// WeightedHits.cc
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

typedef std::vector<double> dblvec;

// Data functions
TNtuple* GetPhotonInfo();
double rweight(double r, std::vector<dblvec> weightvec);

// Helper functions
string datetime(); 

void WeightedHits() {
    //Fill weight vector from file
    std::vector<dblvec> weights;
    std::ifstream ifile;
    ifile.open("/home/twester/ratpac-nudot/analysis/weights.txt");
    string line;
    while (ifile >> line) {
        //Split string at comma
        dblvec v;
        stringstream ss(line);
        string d;
        while (getline(ss, d, ',')) {
            v.push_back(std::atof(d.c_str()));
        }
        weights.push_back(v);
    }

    //Fill ntuple with values from output.root file
    TNtuple* ntp = GetPhotonInfo();

    float x, y, xh, yh;
    ntp->SetBranchAddress("x0", &x);
    ntp->SetBranchAddress("y0", &y);
    ntp->SetBranchAddress("xh", &xh);
    ntp->SetBranchAddress("yh", &yh);

    //All photons should be starting from the same point, so grab the first
    ntp->GetEntry(0);

    //Get the source position, in radius, of this run
    double r = TMath::Sqrt(x*x + y*y);

    double whits = 0.0;
    for (int i = 0; i < ntp->GetEntries(); i++) {
        ntp->GetEntry();
        double r = TMath::Sqrt(xh*xh + yh*yh);
        whits += rweight(r, weights);
    }

    std::cout << "r " << r << "\thits " << whits 
              << "\ttotal " << ntp->GetEntries() << std::endl;

}

TNtuple* GetPhotonInfo() {
    //Create NTuple for photon data 
    TNtuple *ntuple = new TNtuple("dph","photon data","x0:y0:z0:xh:yh:zh");


    RAT::DSReader reader("/home/twester/ratpac-nudot/output.root");
    int nevents = reader.GetTotal();

    RAT::DS::Root *ds = reader.NextEvent();

    //Define ntuple variables
    float x0, y0, z0, xh, yh, zh;
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
            // get final tracknode parameters. could be the same as rayleigh scattering parameters

            n = c.GoTrackEnd();
            n->GetVolume() == "pvPMT00" ? hit = true : hit = false;
            if (hit) {
                // photon propagates once inside the PMT volume
                // go back one step to get the hit position on the plate
                n = c.GoPrev();
                xh = n->GetEndpoint()[0];
                yh = n->GetEndpoint()[1];
                zh = n->GetEndpoint()[2];
                std::vector<float> fillvec = {x0, y0, z0, xh, yh, zh}; 
                ntuple->Fill(&fillvec[0]);
            }
            n = c.FindNextTrack();
        }
        ds = reader.NextEvent();
    }
    return ntuple;
}


double rweight(double r, std::vector<dblvec> weightvec) {
    double x1, y1, x2, y2;  
    bool foundpts = false;
    //Assume weightvec is sorted ascending
    for (size_t it = 0; it != weightvec.size(); it++) {
        if (weightvec[it][0] > r && it != 0) {
            x1 = weightvec[it-1][0];
            y1 = weightvec[it-1][1];
            x2 = weightvec[it][0];
            y2 = weightvec[it][1];
            foundpts = true;
            break;
        }
    }
    //Just in case we are slightly outside the plate, just use 6%
    if (!foundpts) {
        return weightvec[weightvec.size() - 1][1];
    }
    //Linear interpolate between two closest points in weightvec
    return y1 + (r - x1) * ( (y2 - y1) / (x2 - x1) );
}

string datetime() {
    TDatime t;
    stringstream ss;
    ss << t.GetDate() << "-" << t.GetTime();

    return ss.str();
}
