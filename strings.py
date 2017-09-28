def opticsstring(*args, **kwargs):
    return """// -------------  General Environment ---------------
{
name: "OPTICS",
index: "air",
valid_begin : [0, 0],
valid_end : [0, 0],
RINDEX_option: "wavelength", //60 nm is bogus to prevent G4 from complaining when VUVs hit the air
RINDEX_value1: [60.0, 200.0, 300.0, 500.0, 700.0, 800.0, ], //with neck some vuvs reach the air
RINDEX_value2: [1.0003236, 1.0003236, 1.0002915, 1.0002792, 1.0002763, 1.0002756, ],
ABSLENGTH_option: "wavelength", //60 nm is bogus to prevent G4 from complaining when VUVs hit the air
ABSLENGTH_value1: [60.0, 200.0, 300.0, 330.0, 500.0, 600.0, 770.0, 800.0, ],
ABSLENGTH_value2: [1.0e6, 1.0e6, 1.0e6, 1.0e6, 1.0e6, 1.0e6, 1.0e6, 1.0e6, ],
PROPERTY_LIST: ["RINDEX", "ABSLENGTH", ]
}

{
// Reflectance data taken from Figure 1 of Karlsson and Ribbing, J. Appl. Phys. Vol 53. No. 9 Sept. 1982 
// Assuming austenitic stainless (832MV on Figure) and assuming constant reflectivity below 200nm (limit of plot)
name: "OPTICS",
index: "stainless_steel",
valid_begin : [0, 0],
valid_end : [0, 0],
surface: 1,
finish: "ground",
model: "glisur",
type: "dielectric_metal",
polish: 0.1,
REFLECTIVITY_option: "wavelength",
REFLECTIVITY_value1: [60.0, 200.0, 800.0,],
REFLECTIVITY_value2: """ + '[{}, {}, {},],'.format(kwargs['ssref_128'], kwargs['ssref_128'], kwargs['ssref_420'],) + \
"""\nABSLENGTH_option: "wavelength",
ABSLENGTH_value1: [60d,  800d, ],
ABSLENGTH_value2: [0.00001d, 0.00001d, ],
PROPERTY_LIST: ["REFLECTIVITY", "ABSLENGTH", ]
}

{
name: "OPTICS",
index: "aluminum",
valid_begin : [0, 0],
valid_end : [0, 0],
surface: 1,
//finish: "polished",
finish: "ground",
model: "glisur",
type: "dielectric_metal",
//polish: 0.9,
REFLECTIVITY_option: "wavelength",
REFLECTIVITY_value1: [ 60.0, 800.0, ],
REFLECTIVITY_value2: """ + '[ {}, {}, ],'.format(kwargs['alref_128'], kwargs['alref_128'],) + \
"""\nABSLENGTH_option: "wavelength",
ABSLENGTH_value1: [60.0, 800.0, ],
ABSLENGTH_value2: [1.0e-3, 1.0e-3, ],
PROPERTY_LIST: ["REFLECTIVITY", "ABSLENGTH", ]
}

// ------------------- PMT materials ----------------

{
name: "OPTICS",
index: "glass",
valid_begin : [0, 0],
valid_end : [0, 0],
surface: 1,
finish: "ground",
model: "glisur",
type: "dielectric_dielectric",
polish: 0.9,
RINDEX_option: "wavelength",
RINDEX_value1: [60.0, 200.0, 300.0, 600.0, 800.0, ],
RINDEX_value2: """ + '[{}, {}, {}, {}, {},],'.format(kwargs['nglass_420'],kwargs['nglass_420'],kwargs['nglass_420'],kwargs['nglass_420'],kwargs['nglass_420'],) + \
"""\nABSLENGTH_option: "wavelength",
ABSLENGTH_value1: [60.0, 200.0, 300.0, 330.0, 500.0, 600.0, 770.0, 800.0, ],
ABSLENGTH_value2: [0.1e-3, 0.1e-3, 0.1e-3, 1.0e3, 2.0e3, 1.0e3, 0.5e3, 0.1e-3, ],
PROPERTY_LIST: ["RINDEX", "ABSLENGTH", ]
}

// --------------------- Plastics ----------------------------

{
name: "OPTICS",
index: "acrylic_uvt",
valid_begin : [0, 0],
valid_end : [0, 0],
ABSLENGTH_option: "wavelength",
// we will account for absorption at the end
ABSLENGTH_value1: [ 60.0, 200.0, 800.0 ],
ABSLENGTH_value2: [ 1.0e-9, 1.0e-9, 1.0e4 ],
RINDEX_option: "wavelength",
RINDEX_value1: [ 60.0, 200.0, 800.0 ],
RINDEX_value2: """ + '[{}, {}, {},],'.format( kwargs['nacrylic_420'],kwargs['nacrylic_420'],kwargs['nacrylic_420']  ,) + \
"""\nPROPERTY_LIST: ["RINDEX", "ABSLENGTH", ]
}

// -------------  General Environment ---------------

{
name: "OPTICS",
index: "LAr",
valid_begin : [0, 0],
valid_end : [0, 0],
RINDEX_option: "wavelength",
RINDEX_value1: [60d, 200d, 800d, ],
RINDEX_value2: """ + '[{}d, {}d, {}d, ],'.format(kwargs['nlar_128'], kwargs['nlar_128'], kwargs['nlar_420'], ) + \
"""\nABSLENGTH_option: "wavelength",
ABSLENGTH_value1: [ 60d, 200d,   800d, ],
ABSLENGTH_value2: [ 1.79d6, 1.79d6, 1.79d6 ],
OPSCATFRAC_option: "wavelength",
OPSCATFRAC_value1: [60d, 800d, ],
OPSCATFRAC_value2: [0.0d, 0.0d, ],
RAYLEIGH_option: "wavelength",
RAYLEIGH_value1: [60d, 800d, ],
RAYLEIGH_value2: """ + '[{}, {},],'.format(kwargs['rayleigh'], kwargs['rayleigh'], ) + \
"""\nSCINTILLATION_option: "dy_dwavelength",
SCINTILLATION_value1: [100d, 125d, 128d,       131d, 800d, ],
SCINTILLATION_value2: [0d,     0d, 13333.33d,  0.0d, 0.0d, ],
SCINTWAVEFORM_value1: [-6.0d, -1500d, ],
SCINTWAVEFORM_value2: [0.50d, 0.50d,],
SCINTWAVEFORMalpha_value1: [-6.0d,-1500d],
SCINTWAVEFORMalpha_value2: [0.7d, 0.3d],
SCINTWAVEFORMneutron_value1: [-6.0d,-1500d],
SCINTWAVEFORMneutron_value2: [0.5d, 0.5d],
PROPERTY_LIST: ["RINDEX", "ABSLENGTH","OPSCATFRAC","RAYLEIGH", "SCINTILLATION", "SCINTWAVEFORM", "SCINTWAVEFORMalpha", "SCINTWAVEFORMneutron" ]
}"""


def sourcestring(*args, **kwargs):
    return """//=================================================
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
    double scale = 1.;//134000. / (float)simsize;
    //0.64:  Relative efficiency of coated TPB plates to evap. TPB plates
    //1.18:  Efficiency of evap. TPB plates
    //0.199: QE of uBooNE PMT
    //0.64:  Opacity of coated plate
    double pefactors = 1.; //0.64 * 1.18 * 0.199 * 0.64;

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
    double sigma = """ + '{}; // Alpha position spread parameter'.format(kwargs['sourcewidth']) + \
    """\n    double maxradius = 3.0; // Source disk radial cutoff
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
"""

def geostring(*args, **kwargs):
    return """
