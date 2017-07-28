/*
 * alphamc.cc
 *
 * Runs the alpha-from-Gaussian drawing process separately from the autorun script
 * Useful for making plots on the fly
 */

#include <iostream>
#include <vector>
#include <iomanip>

#include "TCanvas.h"
#include "TH1.h"
#include "TFile.h"
#include "TGraphErrors.h"
#include "TRandom.h"

typedef std::vector<double> dblvec;

double rweight(double r, std::vector<dblvec> weightvec);

void alphamc() {
    gStyle->SetOptStat(0);
    TRandom3 rnd;
    rnd.SetSeed(time(NULL));

    TFile* fin = new TFile("203_1m/PESpec.root");
    TGraphErrors* gr = (TGraphErrors *)fin->Get("grpe");
    TGraphErrors* gr2 = (TGraphErrors *)fin->Get("grhit");

    std::vector<dblvec> weights;
    double x, y;
    for (int i = 0; i < gr->GetN(); i++) {
        dblvec pt;
        gr->GetPoint(i, x, y);
        pt.push_back(x);
        pt.push_back(y);
        weights.push_back(pt);
    }

    std::vector<dblvec> weights2;
    double x2, y2;
    for (int i = 0; i < gr2->GetN(); i++) {
        dblvec pt;
        gr2->GetPoint(i, x2, y2);
        pt.push_back(x2);
        pt.push_back(y2);
        weights2.push_back(pt);
    }

    TH1F* hr = new TH1F("hr", "R distribution;Alpha Position (mm)", 100, 0, 3.5);
    TH1F* hpe = new TH1F("hpe", "PE Spectrum;PE", 500, 0, 300);
    TH1F* hpep = new TH1F("hpep", "PE Spectrum (Pois);PE", 300, 0, 300);
    TH1F* hhit = new TH1F("hhit", "Plate Hits;Photon Hits on Plate", 500, 0, 10000);
    TH1F* hhitp = new TH1F("hhitp", "Plate Hits (Pois);Photon Hits on Plate", 500, 0, 10000);
    TH2F* hpos = new TH2F("hpos", "Alpha Emission Position;X (mm);Y (mm)", 100, -3., 3., 100, -3., 3.);
    double sigma = 0.8;
    double maxradius = 3.0;
    int n = 100000;
    int total = 0;
    int count = 0;
    while (count < n) {
        double x = rnd.Gaus(0.0, sigma);
        double y = rnd.Gaus(0.0, sigma);

        double r = TMath::Sqrt(x*x + y*y);

        if (r > maxradius) {
            continue;
        }

        count++;
        hr->Fill(r);
        hpos->Fill(x,y);
        double pe = rweight(r, weights);
        double hits = rweight(r, weights2);
        hpe->Fill(pe);
        hpep->Fill(rnd.PoissonD(pe));
        hhit->Fill(hits);
        hhitp->Fill(rnd.PoissonD(hits));

        if (count % 100000 == 0) {
            stringstream fname;
            fname << "hist/pe" << std::setfill('0') << std::setw(3) << count << ".png";
            TCanvas* c1 = new TCanvas("c1", "Plots", 800, 800);
            c1->Divide(2,2);
            c1->cd(1);
            hr->Draw();

            c1->cd(2);
            hpe->Draw();

            c1->cd(3);
            TMultiGraph* mg = new TMultiGraph();
            mg->Add(gr);
            double xlist[1] = { r };
            double ylist[1] = {rweight(r, weights)};

            TGraphErrors* gr2 = new TGraphErrors(1, &xlist[0], &ylist[0]);
            gr2->SetMarkerStyle(8);
            gr2->SetMarkerColor(2);
            gr2->SetMarkerSize(1);
            mg->Add(gr2);
            mg->Draw("AP");
            mg->GetXaxis()->SetTitle("Alpha Position (mm)");
            mg->GetYaxis()->SetTitle("PE");
            mg->GetYaxis()->SetTitleOffset(1.5);

            c1->cd(4);
            hpep->Draw();

            c1->SaveAs(fname.str().c_str());
            delete c1;
        }
    }
    std::cout << "Hit Mean: " << hhit->GetMean() << std::endl;
    std::cout << "PE Mean: " << hpe->GetMean() << std::endl;

    gStyle->SetOptStat(111);

    stringstream ofilename;
    ofilename << "PESpec.root";
    TFile* f = new TFile(ofilename.str().c_str(), "RECREATE");

    //ROOT plotting junk
    hr->GetXaxis()->SetTitle("Source disk radius (mm)");
    hr->GetYaxis()->SetTitle("Events");

    hpe->GetXaxis()->SetTitle("PE");
    hpe->GetYaxis()->SetTitle("Events");

    hpep->GetXaxis()->SetTitle("PE");
    hpep->GetYaxis()->SetTitle("Events");

    //grwhvr->Write();
    hr->Write();
    hpe->Write();
    hpep->Write();
    hpos->Write();
    hhit->Write();
    hhitp->Write();

}

double rweight(double r, std::vector<dblvec> weightvec) {
    //Finds point on weight curve given r and a vector of (x, y) pairs
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
    //Just in case we are outside the curve, return the last value
    if (!foundpts) {
        return weightvec[weightvec.size() - 1][1];
    }
    //Linear interpolate between two closest points on the curve
    return y1 + (r - x1) * ( (y2 - y1) / (x2 - x1) );
}
