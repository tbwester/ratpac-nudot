// ====================================================
//
// gqe.C
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
#include <stdlib.h>

#include "TH1.h"
#include "TFile.h"
#include "TMath.h"
#include "TNtuple.h"

typedef std::vector<double> dblvec;
double weight(double r, std::vector<dblvec> &weightvec);

int gqe() {
  //Create NTuple for photon data 
  //TNtuple *ntuple = new TNtuple("dph","photon data",
  //    "x0:y0:z0:x1:y1:z1:px0:py0:pz0:px1:py1:pz1:hit:steps:xr:yr:zr:pxr:pyr:pzr:xh:yh:zh");

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

  RAT::DSReader reader("/home/twester/ratpac-nudot/output.root");
  int nevents = reader.GetTotal();
  std::cout << "Got " << nevents << " events.\n";
  
  RAT::DS::Root *ds = reader.NextEvent();

  //Define ntuple variables
  float xh, yh, zh;
  bool hit;
  float wpe_total = 0; // weighted pe total
  while (ds != 0) {
    // create track navigation interface
    RAT::TrackNav nav(ds);

    RAT::TrackCursor c = nav.Cursor(false);
    RAT::TrackNode *n = c.Here();
    n = c.FindNextTrack();
    while (n != 0) {
      // get final tracknode parameters. could be the same as rayleigh scattering parameters
      n = c.GoTrackEnd();
      n->GetVolume() == "pvPMT00" ? hit = true : hit = false;
      if (hit) {
          n = c.GoPrev();
          xh = n->GetEndpoint()[0];
          yh = n->GetEndpoint()[1];
          zh = n->GetEndpoint()[2];
          double dist = TMath::Sqrt(xh*xh + yh*yh);
          wpe_total += weight(dist, weights);
      }
      else {
          xh = 0.0;
          yh = 0.0;
          zh = 0.0;
      }
      n = c.FindNextTrack();
    }
    ds = reader.NextEvent();
  }
  std::ofstream outfile;
  outfile.open("/home/twester/ratpac-nudot/gqe_log.txt");
  
  //int nhits = ntuple->Draw("hit>>hist","hit==1","goff"); 
  //outfile << nhits << std::endl;

  std::cout << "Weighted Hits: " << wpe_total << std::endl;

  //TFile* fout = new TFile("/home/twester/ratpac-nudot/ntuple.root", "RECREATE");
  //ntuple->Write();
  //fout->Close();
  return 0;
};


double weight(double r, std::vector<dblvec> &weightvec) {
  double x1, y1, x2, y2;  
  bool foundpts = false;
  //Assume weightvec is sorted
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
  //Just in case we are slightly outside the plate, just use 5%
  if (!foundpts) {
    return 0.06;
  }
  //std::cout << "(" << x1 << ", " << y1 << ") (" << x2 << ", " << y2 << ")\n";
  //Linear interpolate between two closest points in weightvec
  return y1 + (r - x1) * ( (y2 - y1) / (x2 - x1) );

}
