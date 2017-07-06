#include <iostream>
#include <sstream>
#include <fstream>

#include "TH2.h"
#include "TFile.h"

int pecount(float len=0)
{
  std::ofstream outfile;
  outfile.open("/home/twester/ratpac-nudot/bo_src_log.txt", std::ios_base::app);

  RAT::DSReader reader("/home/twester/ratpac-nudot/output.root");
  
  int nevents = reader.GetTotal();

  stringstream ss;
  ss << len;
  TH2F* h = new TH2F(ss.str().c_str(),ss.str().c_str(),100,-200,200,100,-200,200);

  int petotal = 0;
  for (int iev=0; iev<nevents; iev++) {
    RAT::DS::Root* dsroot = reader.NextEvent();
    RAT::DS::MC* mc = dsroot->GetMC();
    int npes = mc->GetNumPE();
    int npmts = mc->GetMCPMTCount();
    for (int i = 0; i < npmts; i++) {
        RAT::DS::MCPMT* pmt = mc->GetMCPMT(i);
        int pes = pmt->GetMCPhotonCount();
        for (int j = 0; j < pes; j++) {
            RAT::DS::MCPhoton* thepe = pmt->GetMCPhoton(j);
            h->Fill(thepe->GetPosition()[0], thepe->GetPosition()[1]);
        }
    }
    petotal += npes;
    //std::cout <<  "Event " << iev << std::endl;
    //std::cout << "  nPEs=" << npes << " npmts=" << npmts << std::endl;

  }
  outfile << len << "\t" << petotal << "\n"; 
  TFile* fout = new TFile("here.root","UPDATE");
  h->Write();
  fout->Close();
  return 0;
};
