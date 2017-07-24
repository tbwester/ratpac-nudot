// ====================================================
//
// helper.hh
// Thomas Wester July 2017
// 
// Helper functions for analysis scripts
//
// ====================================================

#ifndef _HELPER_HH
#define _HELPER_HH

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <stdlib.h>

#include "TMath.h"
#include "TDatime.h"

typedef std::vector<double> dblvec;

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

TNtuple* GetPhotonInfo(string filepath) {
    //Create NTuple for photon data 
    TNtuple *ntuple = new TNtuple("dph","photon data","x0:y0:z0:xh:yh:zh:pz0");

    stringstream rootfilename;
    rootfilename << filepath << "../../output.root";
    RAT::DSReader reader(rootfilename.str().c_str());
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

string datetime() {
    //Return string of format YYYYMMDD-HHMMSS
    TDatime t;
    stringstream ss;
    ss << t.GetDate() << "-" << t.GetTime();

    return ss.str();
}

#endif
