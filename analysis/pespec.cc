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

#include "helper.hh"

typedef std::vector<double> dblvec;

void pespec(string filepath) {
    TRandom3 rnd;
    rnd.SetSeed(time(NULL));

    stringstream ifilename;
    ifilename << "/home/twester/ratpac-nudot/" << filepath << "pltweights.txt";

    std::vector<dblvec> weights = vecfromfile(ifilename.str().c_str());

    //Unpack the weight vector for plotting
    dblvec wvx, wvy, wvxe, wvye;
    for (std::size_t it = 0; it != weights.size(); it++) {
        wvx.push_back(weights[it][0]);
        wvy.push_back(weights[it][1]);
        wvxe.push_back(0.0);
        wvye.push_back(TMath::Sqrt(weights[it][1]));
    }

    //Do source plate monte carlo
    TGraphErrors* grwhvr = new TGraphErrors(weights.size(), 
            &(wvx[0]), &(wvy[0]), &(wvxe[0]), &(wvye[0]));

    TH1F* hr = new TH1F("hr", "R distribution", 100, 0, 3.5);
    TH1F* hpe = new TH1F("hpe", "PE Spectrum", 100, 0, 100);
    TH1F* hpep = new TH1F("hpep", "PE Spectrum (Pois)", 100, 0, 100);
    double sigma = 1.0;
    double maxradius = 3.0;
    int n = 100000;
    int total = 0;
    for (int i = 0; i < n; i++) {
        double x = rnd.Gaus(0.0, sigma);
        double y = rnd.Gaus(0.0, sigma);

        double r = TMath::Sqrt(x*x + y*y);

        if (r > maxradius) {
            continue;
        }
        hr->Fill(r);
        double pe = rweight(r, weights);
        hpe->Fill(pe);
        hpep->Fill(rnd.PoissonD(pe));
    }

    stringstream ofilename;
    ofilename << "/home/twester/ratpac-nudot/" << filepath << "pespec.root";
    TFile* f = new TFile(ofilename.str().c_str(), "RECREATE");

    //ROOT plotting junk
    grwhvr->SetTitle("PE Function");
    grwhvr->GetXaxis()->SetTitle("Source disk radius");
    grwhvr->GetYaxis()->SetTitle("PE");

    hr->GetXaxis()->SetTitle("Source disk radius");
    hr->GetYaxis()->SetTitle("Events");

    hpe->GetXaxis()->SetTitle("PE");
    hpe->GetYaxis()->SetTitle("Events");

    hpep->GetXaxis()->SetTitle("PE");
    hpep->GetYaxis()->SetTitle("Events");

    grwhvr->Write();
    hr->Write();
    hpe->Write();
    hpep->Write();
}


