#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <stdlib.h>

#include "TH2.h"
#include "TFile.h"
#include "TMath.h"

typedef std::vector<double> dblvec;

int PlateCount(string filepath, float len=0) {

  std::ofstream outfile;
  stringstream ofilename;
  ofilename << filepath << "weights.txt";
  outfile.open(ofilename.str().c_str(), std::ios_base::app);

  stringstream rootfilename;
  rootfilename << filepath << "../../output.root";
  RAT::DSReader reader(rootfilename.str().c_str());
  
  int nevents = reader.GetTotal();

  stringstream ss;
  ss << len;
  int petotal = 0;
  int petotalplate = 0;
  double wpetotal = 0.0;
  for (int iev=0; iev<nevents; iev++) {
    RAT::DS::Root* dsroot = reader.NextEvent();
    RAT::DS::MC* mc = dsroot->GetMC();
    int npes = mc->GetNumPE();
    int npmts = mc->GetMCPMTCount();
    for (int i = 0; i < npmts; i++) {
        RAT::DS::MCPMT* pmt = mc->GetMCPMT(i);
        int PMTID = pmt->GetID();
        int phs = pmt->GetMCPhotonCount();
        PMTID == 0 ? petotalplate += phs : petotal += phs;//npes;
    }
  }
  std::cout << "writing to files\n";
  outfile << len << "," << (double)petotalplate / (double)nevents << "\n"; 
  return 0;
};
