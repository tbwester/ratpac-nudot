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
#include <string>
#include <stdlib.h>

#include "TH1.h"
#include "TFile.h"
#include "TMath.h"
#include "TNtuple.h"
#include "TDatime.h"

typedef std::vector<double> dblvec;
double weight(double r, std::vector<dblvec> &weightvec);
string datetime(); 

int gqe(string filepath="") {
  //Create NTuple for photon data 
  TNtuple *ntuple = new TNtuple("dph","photon data",
<<<<<<< HEAD
      "x0:y0:z0:px0:py0:pz0:hit:xh:yh:zh:xr:yr:zr:pxr:pyr:pzr");
=======
      "x0:y0:z0:px0:py0:pz0:hit:xh:yh:zh");
>>>>>>> 55ef32f0ea30b310fbca78c8b3e4159cf9141215

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
  float x0, y0, z0, x1, y1, z1;
  float px0, py0, pz0, px1, py1, pz1;
  float xh, yh, zh;
<<<<<<< HEAD
  float xr, yr, zr, pxr, pyr, pzr; //rayleigh positions
=======
>>>>>>> 55ef32f0ea30b310fbca78c8b3e4159cf9141215
  float steps;
  bool hit;
  float wpe_total = 0; // weighted pe total
  float npe_total = 0;
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
      px0 = n->GetMomentum()[0] / n->GetKE();
      py0 = n->GetMomentum()[1] / n->GetKE();
      pz0 = n->GetMomentum()[2] / n->GetKE();
      // get final tracknode parameters. could be the same as rayleigh scattering parameters
<<<<<<< HEAD
      n = c.GoNext();
      if (n->GetProcess() == "OpRayleigh") {
          xr = n->GetEndpoint()[0];
          yr = n->GetEndpoint()[1];
          zr = n->GetEndpoint()[2];
          pxr = n->GetMomentum()[0] / n->GetKE();
          pyr = n->GetMomentum()[1] / n->GetKE();
          pzr = n->GetMomentum()[2] / n->GetKE();
      }
      else {
          xr = 0.0;
          yr = 0.0;
          zr = 0.0;
          pxr = 0.0;
          pyr = 0.0;
          pzr = 0.0;
      }


=======
>>>>>>> 55ef32f0ea30b310fbca78c8b3e4159cf9141215
      n = c.GoTrackEnd();
      x1 = n->GetEndpoint()[0];
      y1 = n->GetEndpoint()[1];
      z1 = n->GetEndpoint()[2];
      px1 = n->GetMomentum()[0] / n->GetKE();
      py1 = n->GetMomentum()[1] / n->GetKE();
      pz1 = n->GetMomentum()[2] / n->GetKE();
      steps = n->GetStepID();
      n->GetVolume() == "pvPMT00" ? hit = true : hit = false;
      if (hit) {
          // photon propagates once inside the PMT volume
          // go back one step to get the hit position on the plate
          n = c.GoPrev();
          xh = n->GetEndpoint()[0];
          yh = n->GetEndpoint()[1];
          zh = n->GetEndpoint()[2];
          double dist = TMath::Sqrt(xh*xh + yh*yh);
          npe_total++;
          wpe_total += weight(dist, weights);
      }
      else {
          xh = 0.0;
          yh = 0.0;
          zh = 0.0;
      }
      //if (hit) {
          std::vector<float> fillvec = {x0, y0, z0, px0, py0, pz0,
<<<<<<< HEAD
                                    (float)hit, xh, yh, zh, xr, yr, zr, pxr, pyr, pzr};
=======
                                    (float)hit, xh, yh, zh};
>>>>>>> 55ef32f0ea30b310fbca78c8b3e4159cf9141215
          ntuple->Fill(&fillvec[0]);
      //}
      n = c.FindNextTrack();
    }
    ds = reader.NextEvent();
  }
  //std::ofstream outfile;
  //outfile.open("/home/twester/ratpac-nudot/gqe_log.txt");
  
  //int nhits = ntuple->Draw("hit>>hist","hit==1","goff"); 
  //outfile << nhits << std::endl;

  std::cout << "W: " << wpe_total << ", H: " << npe_total << std::endl;
  stringstream ss;
  double dist = 300 - (z0 + 3.96875);
  ss << "/home/twester/ratpac-nudot/" << filepath << "ntuple_" << dist << "_" 
     << datetime() << ".root";
  TFile* fout = new TFile(ss.str().c_str(), "RECREATE");
  ntuple->Write();
  fout->Close();
  return 0;
};


double weight(double r, std::vector<dblvec> &weightvec) {
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
  //std::cout << "(" << x1 << ", " << y1 << ") (" << x2 << ", " << y2 << ")\n";
  //Linear interpolate between two closest points in weightvec
  return y1 + (r - x1) * ( (y2 - y1) / (x2 - x1) );

}

string datetime() {
    TDatime t;
    stringstream ss;
    ss << t.GetDate() << "-" << t.GetTime();

    return ss.str();
}
