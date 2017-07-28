//============================================
//
// PlateCount.cc
// Thomas Wester
//
// Generate the efficiency curve for the PMT
// plate. Save the ntuple of hit positions
// and directions.
//
//============================================

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <stdlib.h>

#include "TH2.h"
#include "TFile.h"
#include "TMath.h"

#include "helper.hh" /* GetPhotonInfo */

void PlateCount(string filepath, int simsize=0, float len=0) {
    std::ofstream outfile;
    stringstream ofilename;
    ofilename << filepath << "weights.txt";
    outfile.open(ofilename.str().c_str(), std::ios_base::app);

    //Fill ntuple with values from output.root file
    TNtuple* ntp = GetPhotonInfo(filepath);
    int petotalplate = ntp->GetEntries();

    std::cout << "writing to files\n";

    //Write ratio for this particular plate position
    outfile << len << "," << (double)petotalplate / (double)simsize << "\n"; 

    stringstream rootfilename;
    rootfilename << filepath << "PMTHits_r" << (int)len * 1000. << ".root";
    TFile* ofile = new TFile(rootfilename.str().c_str(), "RECREATE");
    ntp->Write();

    delete ntp;
}
