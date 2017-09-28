// ====================================================
//
// WeightedHits.cc
// Thomas Wester July 2017
// 
// Takes a ntuple of plate hits, and convolves the
// plate efficiency curve with it. Returns the sum
// of all convolved hits over the plate in 
// pltweights.txt file.
//
// ====================================================

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <stdlib.h>

#include "TH1.h"
#include "TF1.h"
#include "TFile.h"
#include "TMath.h"
#include "TNtuple.h"
#include "TDatime.h"
#include "TRandom.h"
#include "TGraphErrors.h"

#include "helper.hh" /* rweight, datetime, vecfromfile */

typedef std::vector<double> dblvec;

void WeightedHits(string filepath) {

    stringstream ifilename;
    ifilename << filepath << "PlateEff.root";
    TFile* platefile = TFile::Open(ifilename.str().c_str());

    TGraphErrors* gr = (TGraphErrors *)platefile->Get("Graph");
    TF1* fitfunc = (TF1 *)gr->GetFunction("fitfunc");

    //Fill ntuple with values from output.root file
    TNtuple* ntp = GetPhotonInfo(filepath);

    TH1F* hwh = new TH1F("hwh", "weighted hit dist", 100, 0, 1);
    float x, y, xh, yh;
    ntp->SetBranchAddress("x0", &x);
    ntp->SetBranchAddress("y0", &y);
    ntp->SetBranchAddress("xh", &xh);
    ntp->SetBranchAddress("yh", &yh);

    //All photons start from the same point, so use the first event
    ntp->GetEntry(0);
    double srcr = TMath::Sqrt(x*x + y*y);

    double whits = 0.0;
    for (int i = 0; i < ntp->GetEntries(); i++) {
        ntp->GetEntry(i);
        double pltr = TMath::Sqrt(xh*xh + yh*yh);
        double weightedhit = fitfunc->Eval(pltr);
        hwh->Fill(weightedhit);
        whits += weightedhit;
    }

    std::cout << "r " << srcr << "\thits " << whits 
              << "\ttotal " << ntp->GetEntries() << std::endl;

    //Append numbers to text file
    stringstream ofilename;
    ofilename << filepath << "pltweights.txt";
    std::ofstream outfile;
    outfile.open(ofilename.str().c_str(), std::ios_base::app);
    outfile << srcr << "," << whits << "," << ntp->GetEntries() << std::endl;
    outfile.close();

    stringstream of2;
    of2 << filepath << "PlateHits_r" << int(srcr * 100.) << ".root";
    TFile* myfile = new TFile(of2.str().c_str(), "RECREATE");
    ntp->Write();
    hwh->Write();
    myfile->Close();

    delete ntp; //avoid memory leaks?
}
