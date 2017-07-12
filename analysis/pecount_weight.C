#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <stdlib.h>

#include "TH2.h"
#include "TFile.h"
#include "TMath.h"

typedef std::vector<double> dblvec;

double weight(double r, std::vector<dblvec> &weightvec);

int pecount_weight(float len=0) {
/*
  //Fill weight vector
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
*/
  std::ofstream outfile;
  //outfile.open("/home/twester/ratpac-nudot/bo_src_log.txt", std::ios_base::app);
  outfile.open("/home/twester/ratpac-nudot/analysis/weights.txt", std::ios_base::app);

  RAT::DSReader reader("/home/twester/ratpac-nudot/output.root");
  
  int nevents = reader.GetTotal();

  stringstream ss;
  ss << len;
  //TH2F* h = new TH2F(ss.str().c_str(),ss.str().c_str(),100,-200,200,200,-200,200);
  TH2F* h = new TH2F(ss.str().c_str(),ss.str().c_str(),200,-800,800,200,-800,800);
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
        //std::cout << npmts << "\t" << PMTID << std::endl;
        int phs = pmt->GetMCPhotonCount();
        /*
        for (int j = 0; j < phs; j++) {
            RAT::DS::MCPhoton* theph = pmt->GetMCPhoton(j);
            float x = theph->GetPosition()[0];
            float y = theph->GetPosition()[1];
            float z = theph->GetPosition()[2];
            double r = TMath::Sqrt(x*x + y*y);
            h->Fill(y, z);
            wpetotal += weight(r, weights);
            //h->Fill(theph->GetPosition()[0], theph->GetPosition()[1]);
            //std::cout << theph->GetLambda() << std::endl;
        }
        */
        PMTID == 0 ? petotalplate += phs : petotal += phs;//npes;
    }
    //petotal += npes;
    //std::cout <<  "Event " << iev << std::endl;
    //std::cout << "  nPEs=" << npes << " npmts=" << npmts << std::endl;

  }
  std::cout << "writing to files\n";
  outfile << len << "," << (double)petotalplate / (double)nevents << "\n"; 
  //TFile* fout = new TFile("here.root","UPDATE");
  //h->Write();
  //fout->Close();
  return 0;
};

double weight(double r, std::vector<dblvec> &weightvec) {
  //std::cout << "made it here: " << r << std::endl;
  double x1, y1, x2, y2;  
  bool foundpts = false;
  //Assume weightvec is sorted
  for (size_t it; it != weightvec.size(); it++) {
    if (weightvec[it][0] > r && it != 0) {
      x1 = weightvec[it-1][0];
      y1 = weightvec[it-1][1];
      x2 = weightvec[it][0];
      y2 = weightvec[it][1];
      foundpts = true;
      break;
    }
  }
  //Just in case we are slightly outside the plate, just use 5%
  if (!foundpts) {
    return 0.077;
  }
  //std::cout << "(" << x1 << ", " << y1 << ") (" << x2 << ", " << y2 << ")\n";
  //Linear interpolate between two closest points in weightvec
  return y1 + (r - x1) * ( (y2 - y1) / (x2 - x1) );

}
