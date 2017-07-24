/*
 * PlateCount.cc
 * Thomas Wester
 * Get the number of hits from photons at the TPB plate which hit the PMT
 */

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <stdlib.h>

#include "TH2.h"
#include "TFile.h"
#include "TMath.h"

#include "helper.hh"

typedef std::vector<double> dblvec;

void PlateCount(string filepath, int simsize=0, float len=0) {
    std::ofstream outfile;
    stringstream ofilename;
    ofilename << filepath << "weights.txt";
    outfile.open(ofilename.str().c_str(), std::ios_base::app);

    //Fill ntuple with values from output.root file
    TNtuple* ntp = GetPhotonInfo(filepath);
    int petotalplate = ntp->GetEntries();

    std::cout << "writing to files\n";
    outfile << len << "," << (double)petotalplate / (double)simsize << "\n"; 

    stringstream rootfilename;
    rootfilename << filepath << "PMTHits_r" << (int)len * 1000. << ".root";
    TFile* ofile = new TFile(rootfilename.str().c_str(), "RECREATE");
    ntp->Write();

    delete ntp;
}
