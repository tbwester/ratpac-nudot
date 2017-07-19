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

typedef std::vector<double> dblvec;

// Data functions
TNtuple* GetPhotonInfo();
double rweight(double r, std::vector<dblvec> weightvec);

// Helper functions
std::vector<dblvec> vecfromfile(string fname);
string datetime(); 

void WeightedHits(string ofilepath) {
    std::vector<dblvec> weights = vecfromfile(
            "/home/twester/ratpac-nudot/analysis/weights.txt");

    //Fill ntuple with values from output.root file
    TNtuple* ntp = GetPhotonInfo();

    float x, y, xh, yh;
    ntp->SetBranchAddress("x0", &x);
    ntp->SetBranchAddress("y0", &y);
    ntp->SetBranchAddress("xh", &xh);
    ntp->SetBranchAddress("yh", &yh);

    //All photons start from the same point, so use the first event
    ntp->GetEntry(0);

    //Get the source position, in radius, of this run
    double srcr = TMath::Sqrt(x*x + y*y);

    TH1F* hr = new TH1F("h", "pltr", 100, 0, 160);

    double whits = 0.0;
    for (int i = 0; i < ntp->GetEntries(); i++) {
        ntp->GetEntry(i);
        double pltr = TMath::Sqrt(xh*xh + yh*yh);
        hr->Fill(pltr);
        whits += rweight(pltr, weights);
    }

    std::cout << "r " << srcr << "\thits " << whits 
              << "\ttotal " << ntp->GetEntries() << std::endl;

    //Append numbers to text file
    stringstream ofilename;
    ofilename << ofilepath << "pltweights.txt";
    std::ofstream outfile;
    outfile.open(ofilename.str().c_str(), std::ios_base::app);
    outfile << srcr << "\t" << whits << "\t" << ntp->GetEntries() << std::endl;
    outfile.close();

    stringstream of2;
    of2 << ofilepath << "hist_" << int(srcr) * 10 << ".root";
    TFile* myfile = new TFile(of2.str().c_str(), "RECREATE");
    hr->Write();
    myfile->Close();
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
    //Finds point on weight curve given r and a vector of (x, y) pairs
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
    //Just in case we are outside the curve, return the last value
    if (!foundpts) {
        return weightvec[weightvec.size() - 1][1];
    }
    //Linear interpolate between two closest points on the curve
    return y1 + (r - x1) * ( (y2 - y1) / (x2 - x1) );
}

std::vector<dblvec> vecfromfile(string fname) {
    //Fill weight vector from file
    std::vector<dblvec> vec;
    std::ifstream ifile;
    ifile.open(fname);
    string line;
    while (ifile >> line) {
        //Split string at comma
        dblvec v;
        stringstream ss(line);
        string d;
        while (getline(ss, d, ',')) {
            v.push_back(std::atof(d.c_str()));
        }
        vec.push_back(v);
    }
    ifile.close();

    return vec;
}

string datetime() {
    //Return string of format YYYYMMDD-HHMMSS
    TDatime t;
    stringstream ss;
    ss << t.GetDate() << "-" << t.GetTime();

    return ss.str();
}
