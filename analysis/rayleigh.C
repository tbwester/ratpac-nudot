// ====================================================
//
// rayleigh.C
// 
// script intended to test rayleigh scattering physics
// now used to produce ntuple of information for each
// photon hit in the bo_src simulation
//
// ====================================================

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <stdlib.h>

#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TMath.h"
#include "TNtuple.h"

typedef std::vector<double> dblvec;

int rayleigh() {
  //mm
  /*
  double srcdepth = 3.9687; //this is a mess due to inches conversion nonsense.
                            //also leave off 0.00005 so that the source is slightly
                            //above the plate
  double srcr = 2.5;
  double plater = 152.5;
  double platedist = dist;

  double thetalim = TMath::Min( TMath::ATan2(plater, platedist),
                                TMath::ATan2(srcr, srcdepth) );
  
  std::cout << thetalim * 180. / 3.1416 << std::endl;
  */
  //Create NTuple for photon data 
  TNtuple *ntuple = new TNtuple("dph","photon data",
      "x0:y0:z0:x1:y1:z1:px0:py0:pz0:px1:py1:pz1:hit:steps:xr:yr:zr:pxr:pyr:pzr:xh:yh:zh");

  RAT::DSReader reader("/home/twester/ratpac-nudot/output.root");
  int nevents = reader.GetTotal();
  std::cout << "Got " << nevents << " events.\n";
  
  RAT::DS::Root *ds = reader.NextEvent();

  //Define ntuple variables
  float x0, y0, z0, x1, y1, z1;
  float px0, py0, pz0, px1, py1, pz1;
  float xr, yr, zr;
  float pxr, pyr, pzr;
  float xh, yh, zh;
  bool hit = false;
  int steps = 0;

  while (ds != 0) {
    // create track navigation interface
    RAT::TrackNav nav(ds);

    RAT::TrackCursor c = nav.Cursor(false);
    RAT::TrackNode *n = c.Here();
    n = c.FindNextTrack();
    while (n != 0) {
      //std::cout << n->GetStepID() << ", ";
      // FindNextTrack returns first tracknode
      px0 = n->GetMomentum()[0] / n->GetKE();
      py0 = n->GetMomentum()[1] / n->GetKE();
      pz0 = n->GetMomentum()[2] / n->GetKE();
      x0 = n->GetEndpoint()[0];
      y0 = n->GetEndpoint()[1];
      z0 = n->GetEndpoint()[2];
 
      // check to see if photon underwent rayleigh scattering
      n = c.GoNext();
      if (n->GetProcess() == "OpRayleigh") {
        //std::cout << n->GetStepID() << ", ";
        pxr = n->GetMomentum()[0] / n->GetKE();
        pyr = n->GetMomentum()[1] / n->GetKE();
        pzr = n->GetMomentum()[2] / n->GetKE();
        xr = n->GetEndpoint()[0];
        yr = n->GetEndpoint()[1];
        zr = n->GetEndpoint()[2];
      }
      else {
        pxr = 0.0;
        pyr = 0.0;
        pyz = 0.0;
        xr = 0.0;
        yr = 0.0;
        zr = 0.0;
      }

      // get final tracknode parameters. could be the same as rayleigh scattering parameters
      n = c.GoTrackEnd();
      steps = n->GetStepID();
      //std::cout << n->GetStepID() << std::endl;
      n->GetVolume() == "pvPMT00" ? hit = true : hit = false;
      
      px1 = n->GetMomentum()[0] / n->GetKE();
      py1 = n->GetMomentum()[1] / n->GetKE();
      pz1 = n->GetMomentum()[2] / n->GetKE();
      x1 = n->GetEndpoint()[0];
      y1 = n->GetEndpoint()[1];
      z1 = n->GetEndpoint()[2];

      if (hit) {
          n = c.GoPrev();
          xh = n->GetEndpoint()[0];
          yh = n->GetEndpoint()[1];
          zh = n->GetEndpoint()[2];
      }
      else {
          xh = 0.0;
          yh = 0.0;
          zh = 0.0;
      }
      std::vector<float> fillvec = {x0, y0, z0, x1, y1, z1, px0, py0, pz0,
                                    px1, py1, pz1, (float)hit, (float)steps, 
                                    xr, yr, zr, pxr, pyr, pzr, xh, yh, zh};

      //ntuple->Fill(x0, y0, z0, x1, y1, z1, px0, py0, pz0, 
      //             px1, py1, pz1, hit, steps, pxr, pyr, pzr);
      ntuple->Fill(&fillvec[0]);

      n = c.FindNextTrack();
    }
    // go to next event
    ds = reader.NextEvent();
  }
  //std::ofstream outfile;
  //outfile.open("/home/twester/ratpac-nudot/rayleigh_log.txt", std::ios_base::app);
  //outfile << "N_sa: " << htheta_cut->GetEntries() 
  //        << ", N_miss: " << nmiss << std::endl;
  //outfile << "N_pass: " << htheta->GetEntries() 
  //        << ", N_corr: " << ncorrect << std::endl;
  int nhits = ntuple->Draw("hit>>hist","hit==1","goff"); 
  //outfile << nhits << std::endl;

  std::cout << "Hits: " << nhits << std::endl;

  TFile* fout = new TFile("/home/twester/ratpac-nudot/ntuple.root", "RECREATE");
  ntuple->Write();
  fout->Close();
  return 0;
};
