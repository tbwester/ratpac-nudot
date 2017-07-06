#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <stdlib.h>

#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TMath.h"

typedef std::vector<double> dblvec;

void rayleigh_test() {
  //cm
  double srcdepth = 0.19;
  double srcr = 0.25;
  double plater = 15.3;
  double platedist = 20.3;

  double thetalim = TMath::Min( TMath::ATan2(plater, platedist + srcdepth), 
                                TMath::ATan2(srcr, srcdepth) ); 
  double deltatheta = 0.08;
  std::cout << thetalim * 180. / 3.1416 << std::endl;
  //thetalim = 28.8 * 3.1416 / 180.;
  int converge = 0;
  while (converge != 2) {
  if (converge == 1) {
    thetalim -= deltatheta;
  }
  else if (converge == 0) {
    thetalim += deltatheta;
  }
  int npass = 0; 
  int nsim = 0;
  RAT::DSReader reader("/home/twester/ratpac-nudot/output.root");
  int nevents = reader.GetTotal();
  
  RAT::DS::Root *ds = reader.NextEvent();
  
  while (ds != 0) {
    // create track navigation interface
    RAT::TrackNav nav(ds);

    RAT::TrackCursor c = nav.Cursor(false);
    RAT::TrackNode *n = c.Here();

    n = c.FindNextTrack();
    while (n != 0) {
      // FindNextTrack returns first tracknode
      double px, py, pz;
      px = n->GetMomentum()[0] / n->GetKE();
      py = n->GetMomentum()[1] / n->GetKE();
      pz = n->GetMomentum()[2] / n->GetKE();
      double angle = TMath::ATan2(TMath::Sqrt(px*px + py*py), pz);

      //std::cout << px*px + py*py + pz*pz << std::endl; //check if getting unit vectors
      if (pz > 0 && angle < thetalim && angle > (-1. * thetalim)) {
        npass++;
      }
      // get last tracknode parameters
      n = c.GoTrackEnd();
      if (n->GetVolume() != "pvPMT00") {
        n = c.FindNextTrack();
        continue;
      }
      nsim++;
      // do this at the end in case n == 0
      n = c.FindNextTrack();
    }
    // go to next event
    ds = reader.NextEvent();
  }
  std::cout << thetalim << "\t" << npass << "\t" << nsim << std::endl;
  if (npass > nsim) {
    if (converge == 0) { deltatheta /= 2.; }
    converge = 1;
  }
  else if (npass < nsim) {
    if (converge == 1) { deltatheta /= 2.; }
    converge = 0;
  }
  else {
    converge = 2;
  }
  std::cout << thetalim * 180. / 3.1416 << std::endl;
  }
}
