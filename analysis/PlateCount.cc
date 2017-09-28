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

    stringstream ss;
    ss << filepath << "../../output.root";

    //Fill ntuple with values from output.root file
    RAT::DSReader reader(ss.str().c_str());

    int nevents = reader.GetTotal();
   
    int petotal = 0;
    for (int iev = 0; iev < nevents; iev++) {
        RAT::DS::Root* dsroot = reader.NextEvent();
        RAT::DS::MC* mc = dsroot->GetMC();
        int npes = mc->GetNumPE();
        int npmts = mc->GetMCPMTCount();
        petotal += npes;
    }

    std::cout << "writing to files\n";

    //Write ratio for this particular plate position
    outfile << len << "," << (double)petotal / (double)simsize << "\n"; 

}
