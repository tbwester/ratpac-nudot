/* PlateFit.cc
 * Thomas Wester
 * Fits a gaussian function to the plate weight file
 */

#include <iostream>
#include <string>
#include <sstream>
#include <vector>

#include "TFile.h"
#include "TF1.h"
#include "TGraphErrors.h"

#include "helper.hh"

typedef std::vector<double> dblvec;

void PlateFit(string filepath, int simsize) {
    stringstream ifilename;
    ifilename << filepath << "weights.txt";

    std::vector<dblvec> weights = vecfromfile(ifilename.str().c_str());

    //Unpack the weight vector for plotting
    dblvec wvx, wvy, wvxe, wvye;
    for (std::size_t it = 0; it != weights.size(); it++) {
        double y = weights[it][1] * simsize;
        wvx.push_back(weights[it][0]);
        wvy.push_back(y / (double)simsize);
        wvxe.push_back(0.0);
        wvye.push_back(TMath::Sqrt(y) / (double)simsize);
    }
    TGraphErrors* grwhvr = new TGraphErrors(weights.size(), 
            &(wvx[0]), &(wvy[0]), &(wvxe[0]), &(wvye[0]));

    TF1* fitfunc = new TF1("fitfunc", "gaus(0)", wvx[0], wvx[wvx.size() - 1]);
    fitfunc->SetParameter(0, 0.2);
    fitfunc->SetParameter(2, 90.0);
    fitfunc->FixParameter(1, 0.0);
    grwhvr->Fit("fitfunc", "RBQ");

    TF1* result = (TF1 *)grwhvr->GetFunction("fitfunc");
    std::cout << "=====================\n";
    std::cout << "Plate Efficiency Fit:\n";
    std::cout << "Mean: " << result->GetParameter(1) << " +/- " 
        << result->GetParError(1) << std::endl << "Sigma: " 
        << result->GetParameter(2) << " +/- " << result->GetParError(2)
        << std::endl;
    std::cout << "=====================\n";

    grwhvr->GetXaxis()->SetTitle("Plate Radius (mm)");
    grwhvr->GetYaxis()->SetTitle("PMT Collection Efficiency");

    stringstream ofilename;
    ofilename << filepath << "PlateEff.root";
    TFile* f = new TFile(ofilename.str().c_str(), "RECREATE");
    grwhvr->Write();
}
