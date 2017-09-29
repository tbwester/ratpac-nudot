//=================================================
//
// PESpectrum.cc
// Thomas Wester
//
// Generates the simulated PE spectrum using
// pltweights.txt. This file sets the alpha
// distribution width for the alpha monte carlo.
//
// ================================================

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <stdlib.h>

#include "TH1.h"
#include "TGraphErrors.h"
#include "TFile.h"
#include "TMath.h"
#include "TNtuple.h"
#include "TDatime.h"
#include "TRandom.h"

#include "helper.hh" /* vecfromfile, rweight */

typedef std::vector<double> dblvec;

void PESpectrum(string filepath, int simsize) {
    TRandom3 rnd;
    rnd.SetSeed(time(NULL));

    //Number of photons per alpha, divided by number of simulated photons
    double scale = 134000. / (float)simsize;
    //0.67:  Relative efficiency of coated TPB plates to evap. TPB plates
    //0.4:  Efficiency of evap. TPB plates
    //0.153: QE of uBooNE PMT
    //1.22: temperature correction  
    double pefactors = 0.67 * 1.53 * 0.4 * 1.22;

    stringstream ifilename;
    ifilename << filepath << "pltweights.txt";

    std::vector<dblvec> weights = vecfromfile(ifilename.str().c_str());

    //Unpack the weight vector for plotting
    dblvec wvx, wvy, wvxe, wvye;
    dblvec wvy2, wvye2;
    for (std::size_t it = 0; it != weights.size(); it++) {
        //PE vs. source position graph
        double y = weights[it][1];
        wvx.push_back(weights[it][0]);
        wvy.push_back(y * scale * pefactors);
        wvxe.push_back(0.0);
        wvye.push_back(TMath::Sqrt(y) * scale * pefactors);
        //Raw count graph vs source position graph
        wvy2.push_back(weights[it][2] * scale);
        wvye2.push_back(TMath::Sqrt(weights[it][2]) * scale);
    }
    int minsize = wvy[wvy.size() - 1] * 0.8;
    int maxsize = wvy[0] * 1.2;

    //Graphs and histograms to save
    TGraphErrors* grwhvr = new TGraphErrors(weights.size(), 
            &(wvx[0]), &(wvy[0]), &(wvxe[0]), &(wvye[0]));
    TF1* fitfunc = new TF1("fitfunc", "pol4(0)", 0.0, 3.0);
    //fitfunc->SetParameter(0, (float)simsize / 100.);
    //fitfunc->SetParameter(1, -50.0);
    //fitfunc->FixParameter(2, -50.0);
    //fitfunc->FixParameter(3, 0.0);
    grwhvr->Fit("fitfunc", "RBQ");

    TGraphErrors* grwhvr2 = new TGraphErrors(weights.size(), 
            &(wvx[0]), &(wvy2[0]), &(wvxe[0]), &(wvye2[0]));

    TH1F* hr = new TH1F("hr", 
            "R distribution;Alpha Position on Source Disk (mm);Events",
            100, 0, 3.5);
    TH1F* hpe = new TH1F("hpe", 
            "PE Spectrum;PE;Events", 500, minsize, maxsize);
    TH1F* hpe2 = new TH1F("hpe2", 
            "PE Spectrum;PE;Events", 500, minsize, maxsize);
    TH1F* hpep = new TH1F("hpep", 
            "PE Spectrum (Pois);PE;Events", 300, minsize, maxsize);

    //Do source plate monte carlo
    double sigma = 0.750; // Alpha position spread parameter
    double maxradius = 3.0; // Source disk radial cutoff
    int n = 1000000;         // Total number of draws
    int count = 0;          // Counter to keep track of successful draws
    while (count < n) {
        if (sigma < 0.0) {
            sigma = 0.001;
        }
        double x = rnd.Gaus(0.0, sigma);
        double y = rnd.Gaus(0.0, sigma);
        double r = TMath::Sqrt(x*x + y*y);

        if (r > maxradius) {
            continue;
        }

        count++;
        hr->Fill(r);
        double pe2 = rweight(r, weights) * scale * pefactors;
        double pe = fitfunc->Eval(r) * scale * pefactors;
        hpe->Fill(pe);
        hpe2->Fill(pe2);
        hpep->Fill(rnd.PoissonD(pe));
    }

    stringstream ofilename;
    ofilename << filepath << "PESpec.root";
    TFile* f = new TFile(ofilename.str().c_str(), "RECREATE");

    //ROOT plotting junk
    grwhvr->SetName("grpe");
    grwhvr->SetTitle("PE Function");
    grwhvr->GetXaxis()->SetTitle("Source disk radius (mm)");
    grwhvr->GetYaxis()->SetTitle("PE");

    grwhvr2->SetName("grhit");
    grwhvr2->SetTitle("Plate Hits");
    grwhvr2->GetXaxis()->SetTitle("Source disk radius (mm)");
    grwhvr2->GetYaxis()->SetTitle("Hits");

    grwhvr->Write();
    grwhvr2->Write();
    hr->Write();
    hpe->Write();
    hpe2->Write();
    hpep->Write();
}
