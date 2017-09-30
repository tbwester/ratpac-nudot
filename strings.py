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
    double scale = """ + '{} / (float)simsize;'.format(kwargs['phperalpha']) + \
    """\n    //0.67:  Relative efficiency of coated TPB plates to evap. TPB plates
    //0.4:  Efficiency of evap. TPB plates
    //0.153: QE of uBooNE PMT
    //1.22: temperature correction  
    double pefactors = """ + '{} * {} * {} * {};'.format(kwargs['tpbreleff'], kwargs['qe'], kwargs['tpbeff'], kwargs['tempscale']) + \
    """\n    stringstream ifilename;
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
    int minsize = 0.0; //wvy[wvy.size() - 1] * 0.8;
    int maxsize = 300.0; //wvy[0] * 1.2;

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
    TF1* fitfunc2 = new TF1("fitfunc2", "pol4(0)", 0.0, 3.0);
    grwhvr2->Fit("fitfunc2", "RBQ");

    TH1F* hr = new TH1F("hr", 
            "R distribution;Alpha Position on Source Disk (mm);Events",
            100, 0, 3.5);
    TH1F* hhit = new TH1F("hhit",
            "Plate Hit Distribution", 2000, 0, 100000);
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
        double pe2 = rweight(r, weights); // * scale * pefactors;
        double pe = fitfunc->Eval(r); // * scale * pefactors;
        double hit = fitfunc2->Eval(r); // * scale * pefactors;
        hpe->Fill(pe);
        hhit->Fill(hit);
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
    hhit->Write();
    hpe2->Write();
    hpep->Write();
}
"""

def geostring(*args, **kwargs):
    return """<?xml version="1.0" encoding="UTF-8"?>
<gdml xmlns:gdml="http://cern.ch/2001/Schemas/GDML"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd" >

    <define>
        <position name="photocathode_offset" unit="cm" x="0" y="0" z="0.5*11.0-0.5*0.1"/>
        <position name="origin" unit="cm" x="0" y="0" z="0"/>
        <rotation name="identity"/>
    </define>

    <materials>
        <element name="bromine" formula="Br" Z="35"> <atom value="79.904"/> </element>
        <element name="hydrogen" formula="H" Z="1">  <atom value="1.0079"/> </element>
        <element name="nitrogen" formula="N" Z="7">  <atom value="14.0067"/> </element>
        <element name="oxygen" formula="O" Z="8">  <atom value="15.999"/> </element>
        <element name="aluminum" formula="Al" Z="13"> <atom value="26.9815"/>  </element>
        <element name="silicon" formula="Si" Z="14"> <atom value="28.0855"/>  </element>
        <element name="carbon" formula="C" Z="6">  <atom value="12.0107"/>  </element>
        <element name="potassium" formula="K" Z="19"> <atom value="39.0983"/>  </element>
        <element name="chromium" formula="Cr" Z="24"> <atom value="51.9961"/>  </element>
        <element name="iron" formula="Fe" Z="26"> <atom value="55.8450"/>  </element>
        <element name="nickel" formula="Ni" Z="28"> <atom value="58.6934"/>  </element>
        <element name="calcium" formula="Ca" Z="20"> <atom value="40.078"/>   </element>
        <element name="magnesium" formula="Mg" Z="12"> <atom value="24.305"/>   </element>
        <element name="sodium" formula="Na" Z="11"> <atom value="22.99"/>    </element>
        <element name="titanium" formula="Ti" Z="22"> <atom value="47.867"/>   </element>
        <element name="argon" formula="Ar" Z="18"> <atom value="39.9480"/>  </element>
        <element name="boron" formula="B" Z="5"> <atom value="10.811"/> </element>

        <material Z="1" formula=" " name="Vacuum">
            <D value="1.e-25" unit="g/cm3"/>
            <atom value="1.0079"/>
        </material>

        <material name="stainless_steel" formula="stainless_steel">
            <D value="7.9300" unit="g/cm3"/>
            <fraction n="0.0010" ref="carbon"/>
            <fraction n="0.1792" ref="chromium"/>
            <fraction n="0.7298" ref="iron"/>
            <fraction n="0.0900" ref="nickel"/>
        </material>

        <material name="aluminum" formula=" ">
            <D value="2.700" unit="g/cm3"/>
            <fraction n="1.0000" ref="aluminum"/>
        </material>

        <material formula=" " name="air">
            <D value="0.001205" unit="g/cm3"/>
            <fraction n="0.781154" ref="nitrogen"/>
            <fraction n="0.209476" ref="oxygen"/>
            <fraction n="0.00937" ref="argon"/>
        </material>

        <material formula=" " name="Dirt">
            <D value="1.7" unit="g/cm3"/>
            <fraction n="0.438" ref="oxygen"/>
            <fraction n="0.257" ref="silicon"/>
            <fraction n="0.222" ref="sodium"/>
            <fraction n="0.049" ref="aluminum"/>
            <fraction n="0.019" ref="iron"/>
            <fraction n="0.015" ref="potassium"/>
        </material>

        <material formula=" " name="mineral_oil">
            <D value="0.77" unit="g/cm3"/>
            <fraction n="0.8563" ref="carbon"/>
            <fraction n="0.1437" ref="hydrogen"/>
        </material>

        <material formula=" " name="pseudocumene">
            <D value="0.8758" unit="g/cm3"/>
            <fraction n="0.8994" ref="carbon"/>
            <fraction n="0.1006" ref="hydrogen"/>
        </material>

        <material formula=" " name="ppo">
            <D value="1.06" unit="g/cm3"/>
            <fraction n="0.8142" ref="carbon"/>
            <fraction n="0.0501" ref="hydrogen"/>
            <fraction n="0.0633" ref="nitrogen"/>
            <fraction n="0.0723" ref="oxygen"/>
        </material>

        <material formula=" " name="scintillator">
            <D value="0.78" unit="g/cm3"/>
            <fraction n="0.996984" ref="mineral_oil"/>
            <fraction n="0.001919" ref="pseudocumene"/>
            <fraction n="0.001097" ref="ppo"/>
        </material>

        <material formula=" " name="LAr">
            <D value="1.4" unit="g/cm3"/>
            <fraction n="1.0000" ref="argon"/>
        </material>

        <material formula=" " name="chip_silicon">
            <D value="2.3" unit="g/cm3"/>
            <fraction n="1.0" ref="silicon"/>
        </material>

        <material formula=" " name="borosilicate_glass">
            <D value="2.23" unit="g/cm3"/>
            <fraction n="0.05238" ref="silicon"/>
            <fraction n="0.55873" ref="oxygen"/>
            <fraction n="0.38889" ref="boron"/>
        </material>

        <material formula=" " name="photocathode">
            <D value="5.0" unit="g/cm3"/>
            <fraction n="1.0" ref="potassium"/>
        </material>

        <material formula=" " name="glass">
            <D value="2.23" unit="g/cm3"/>
            <fraction n="0.05238" ref="silicon"/>
            <fraction n="0.55873" ref="oxygen"/>
            <fraction n="0.38889" ref="boron"/>
        </material>

        <material formula=" " name="acrylic_uvt">
            <D value="1.18" unit="g/cm3"/>
            <fraction n="1.000" ref="carbon"/>
        </material>


    </materials>

    <solids>
        <box name="world"
            lunit="cm"
            x="300.0*2.54"
            y="300.0*2.54"
            z="300.0*2.54" />
        <tube name="cryostat" lunit="cm" aunit="deg" rmin="11*2.54" rmax="12*2.54" z="40.0*2.54" startphi="0" deltaphi="360.0"/>
        <tube name="cryostat_cap" lunit="cm" aunit="deg" rmin="0" rmax="12*2.54" z="2.0*2.54" startphi="0" deltaphi="360.0"/>
        <tube name="scint" lunit="cm" aunit="deg" rmin="0" rmax="11*2.54" z="40.0*2.54" startphi="0" deltaphi="360.0"/>
        <tube name="tpbplate" lunit="cm" aunit="deg" rmin="0" rmax="6*2.54" z="0.125*2.54" startphi="0" deltaphi="360.0"/>
        <tube name="pmtshield" lunit="mm" aunit="deg" rmin="100.5" rmax="101" z="136.65" startphi="0" deltaphi="360.0"/>
        <ellipsoid name="elpmt" """ + 'ax="{}" by="{}" cz="{}" zcut2="0" lunit="mm"/>'.format(kwargs['glassthick'], kwargs['glassthick'], kwargs['glassthick2']) + \
        """\n        <ellipsoid name="elouter" ax="101" by="101" cz="65" zcut2="0" lunit="mm"/>
        <ellipsoid name="elinner" """ + 'ax="{}" by="{}" cz="{}" zcut2="20" lunit="mm"/>'.format(kwargs['glassthick'], kwargs['glassthick'], kwargs['glassthick2']) + \
        """\n        <subtraction name="pmt_glass">
            <first ref="elouter"/>
            <second ref="elinner"/>
            <positionref ref="origin"/>
            <rotationref ref="identity"/>
        </subtraction>
        <!-- source holder is composed of 3 tubes
       bottom: rmin = 0      rmax = 1.75" z=0.40625"
       middle: rmin = 0.3cm  rmax = 1.75" z=0.09375"
       top:    rmin = 0.25cm rmax = 1.75" z=0.0625"
  -->
  <tube name="sourcediskA" lunit="cm" aunit="deg" rmin="0.0" rmax="1.75*1.27" z="0.40625*2.54" startphi="0" deltaphi="360.0"/> 
  <tube name="sourcediskB" lunit="cm" aunit="deg" rmin="0.3" rmax="1.75*1.27" z="0.09375*2.54" startphi="0" deltaphi="360.0"/>
  <tube name="sourcediskC" lunit="cm" aunit="deg" rmin="0.25" rmax="1.75*1.27" z="0.0625*2.54" startphi="0" deltaphi="360.0"/>

  <union name="sourcediskstage">
      <first ref="sourcediskA"/>
      <second ref="sourcediskB"/>
      <position name="posSourcestage" unit="cm" x="0" y="0" z="0.5*1.27"/>
      <rotationref ref="identity"/>
  </union>

  <union name="sourcediskD">
      <first ref="sourcediskstage"/>
      <second ref="sourcediskC"/>
      <position name="posSource" unit="cm" x="0" y="0" z="0.65625*1.27"/>
      <rotationref ref="identity"/>
  </union>

</solids>

<structure>

    <volume name="volGlass"> <!-- volPhotoCathode -->
        <materialref ref="glass"/> <!-- LAr -->
        <solidref ref="pmt_glass"/>
    </volume>
    <volume name="volPhotoCathode"> <!-- volTemp -->
        <materialref ref="glass"/> <!-- LAr -->
        <solidref ref="elpmt"/>
    </volume>
    <volume name="volTPBPlate">
        <materialref ref="acrylic_uvt"/> <!-- acrylic_uvt -->
        <solidref ref="tpbplate"/>
    </volume>
    <volume name="volPMTShield">
        <materialref ref="stainless_steel"/> <!-- acrylic_uvt -->
        <solidref ref="pmtshield"/>
    </volume>
    <!-- <volume name="volSourceA">
    <materialref ref="stainless_steel"/>
    <solidref ref="sourcediskA"/>
  </volume>-->
  <volume name="volSourceB">
      <materialref ref="stainless_steel"/>
      <solidref ref="sourcediskB"/>
  </volume>
  <volume name="volSourceC">
      <materialref ref="stainless_steel"/>
      <solidref ref="sourcediskC"/>
  </volume> 
  <volume name="volSourceD">
      <materialref ref="aluminum"/>
      <solidref ref="sourcediskD"/>
  </volume> 

  <volume name="volScint">
      <materialref ref="LAr"/>
      <solidref ref="scint"/>
      <!-- Add Photocathodes here -->

      <physvol name="pvGlass"> <!-- pvPMT00 -->
          <volumeref ref="volGlass"/>
          <position name="posGlass2" unit="mm" x="0" y="0" """ + 'z="{}"/>'.format(kwargs['platepmtdist']) + \
      """\n      </physvol>

      <physvol name="pvPMT00">
          <volumeref ref="volPhotoCathode"/>
          <position name="posGlass" unit="mm" x="0" y="0" """ + 'z="{}"/>'.format(kwargs['platepmtdist']) + \
      """\n      </physvol> 
<!-- the following volume is the tpb plate -->
    <physvol name="pvPlate">
        <volumeref ref="volTPBPlate"/> <!-- volTPBPlate -->
        <position name="posPlate" unit="mm" x="0" y="0" z="301.5875"/>
    </physvol>
    <physvol name="pvShield">
        <volumeref ref="volPMTShield"/> <!-- volTPBPlate -->
        <position name="posShield" unit="mm" x="0" y="0" z="439.675"/>
    </physvol>

    <!-- End of photocathodes --> 
    <physvol name="pvSourceD">
        <volumeref ref="volSourceD"/>
        <position name="posSource" unit="mm" x="0" y="0" z="-77.128125"/>
    </physvol>
    <!--
    <physvol name="pvSource">
      <volumeref ref="volSource"/>
<position name="posSource" unit="mm" x="0" y="0" z="87.871875"/>
    </physvol>-->
    <!-- End of photocathodes --> 
    <!--    <physvol name="pvSourceD">
      <volumeref ref="volSourceD"/>
<position name="posSource" unit="mm" x="0" y="0" z="-77.128125"/>
    </physvol>-->
<!--
    <physvol name="pvSource">
      <volumeref ref="volSource"/>
<position name="posSource" unit="mm" x="0" y="0" z="87.871875"/>
    </physvol>

    <physvol name="pvSourceA">
      <volumeref ref="volSourceA"/>
<position name="posSource" unit="mm" x="0" y="0" z="0"/>
    </physvol>
    <physvol name="pvSourceB">
      <volumeref ref="volSourceB"/>
<position name="posSource" unit="cm" x="0" y="0" z="-0.15625*1.27"/>
    </physvol>
    <physvol name="pvSourceC">
      <volumeref ref="volSourceC"/>
<position name="posSource" unit="cm" x="0" y="0" z="-0.65625*1.27"/>
    </physvol>
-->
  </volume>

  <volume name="volCryo">
      <materialref ref="stainless_steel"/>
      <solidref ref="cryostat"/>
  </volume>

  <volume name="volCryoCap">
      <materialref ref="stainless_steel"/> <!-- stainless_steel -->
      <solidref ref="cryostat_cap"/>
  </volume>

  <volume name="volWorld">
      <materialref ref="air"/>
      <solidref ref="world"/>

      <physvol name="pvCryo">  <!-- pvCryo -->
          <volumeref ref="volCryo"/>
          <position name="posCryo" unit="cm" x="0" y="0" z="0"/>
      </physvol>

      <physvol name="pvCryoCap1">
          <volumeref ref="volCryoCap"/>
          <position name="posCryoCap1" unit="cm" x="0" y="0" z="21*2.54"/> <!-- 32.69975 -->
      </physvol>
      <physvol name="pvCryoCap2">
          <volumeref ref="volCryoCap"/>
          <position name="posCryoCap2" unit="cm" x="0" y="0" z="-21*2.54"/> <!-- -9.737875 -->
      </physvol>

      <physvol name="pvScint">
          <volumeref ref="volScint"/>
          <position name="posScint" x="0" y="0" z="0"/>
      </physvol>

  </volume>
</structure>

<setup name="Default" version="1.0">
    <world ref="volWorld" />
</setup>

</gdml>
"""

def srcgeostring(*args, **kwargs):
    return """<?xml version="1.0" encoding="UTF-8"?>
<gdml xmlns:gdml="http://cern.ch/2001/Schemas/GDML"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd" >

    <define>
        <position name="photocathode_offset" unit="cm" x="0" y="0" z="0.5*11.0-0.5*0.1"/>
        <position name="origin" unit="cm" x="0" y="0" z="0"/>
        <rotation name="identity"/>
    </define>

    <materials>
        <element name="bromine" formula="Br" Z="35"> <atom value="79.904"/> </element>
        <element name="hydrogen" formula="H" Z="1">  <atom value="1.0079"/> </element>
        <element name="nitrogen" formula="N" Z="7">  <atom value="14.0067"/> </element>
        <element name="oxygen" formula="O" Z="8">  <atom value="15.999"/> </element>
        <element name="aluminum" formula="Al" Z="13"> <atom value="26.9815"/>  </element>
        <element name="silicon" formula="Si" Z="14"> <atom value="28.0855"/>  </element>
        <element name="carbon" formula="C" Z="6">  <atom value="12.0107"/>  </element>
        <element name="potassium" formula="K" Z="19"> <atom value="39.0983"/>  </element>
        <element name="chromium" formula="Cr" Z="24"> <atom value="51.9961"/>  </element>
        <element name="iron" formula="Fe" Z="26"> <atom value="55.8450"/>  </element>
        <element name="nickel" formula="Ni" Z="28"> <atom value="58.6934"/>  </element>
        <element name="calcium" formula="Ca" Z="20"> <atom value="40.078"/>   </element>
        <element name="magnesium" formula="Mg" Z="12"> <atom value="24.305"/>   </element>
        <element name="sodium" formula="Na" Z="11"> <atom value="22.99"/>    </element>
        <element name="titanium" formula="Ti" Z="22"> <atom value="47.867"/>   </element>
        <element name="argon" formula="Ar" Z="18"> <atom value="39.9480"/>  </element>
        <element name="boron" formula="B" Z="5"> <atom value="10.811"/> </element>

        <material Z="1" formula=" " name="Vacuum">
            <D value="1.e-25" unit="g/cm3"/>
            <atom value="1.0079"/>
        </material>

        <material name="stainless_steel" formula="stainless_steel">
            <D value="7.9300" unit="g/cm3"/>
            <fraction n="0.0010" ref="carbon"/>
            <fraction n="0.1792" ref="chromium"/>
            <fraction n="0.7298" ref="iron"/>
            <fraction n="0.0900" ref="nickel"/>
        </material>

        <material name="aluminum" formula=" ">
            <D value="2.700" unit="g/cm3"/>
            <fraction n="1.0000" ref="aluminum"/>
        </material>

        <material formula=" " name="air">
            <D value="0.001205" unit="g/cm3"/>
            <fraction n="0.781154" ref="nitrogen"/>
            <fraction n="0.209476" ref="oxygen"/>
            <fraction n="0.00937" ref="argon"/>
        </material>

        <material formula=" " name="Dirt">
            <D value="1.7" unit="g/cm3"/>
            <fraction n="0.438" ref="oxygen"/>
            <fraction n="0.257" ref="silicon"/>
            <fraction n="0.222" ref="sodium"/>
            <fraction n="0.049" ref="aluminum"/>
            <fraction n="0.019" ref="iron"/>
            <fraction n="0.015" ref="potassium"/>
        </material>

        <material formula=" " name="mineral_oil">
            <D value="0.77" unit="g/cm3"/>
            <fraction n="0.8563" ref="carbon"/>
            <fraction n="0.1437" ref="hydrogen"/>
        </material>

        <material formula=" " name="pseudocumene">
            <D value="0.8758" unit="g/cm3"/>
            <fraction n="0.8994" ref="carbon"/>
            <fraction n="0.1006" ref="hydrogen"/>
        </material>

        <material formula=" " name="ppo">
            <D value="1.06" unit="g/cm3"/>
            <fraction n="0.8142" ref="carbon"/>
            <fraction n="0.0501" ref="hydrogen"/>
            <fraction n="0.0633" ref="nitrogen"/>
            <fraction n="0.0723" ref="oxygen"/>
        </material>

        <material formula=" " name="scintillator">
            <D value="0.78" unit="g/cm3"/>
            <fraction n="0.996984" ref="mineral_oil"/>
            <fraction n="0.001919" ref="pseudocumene"/>
            <fraction n="0.001097" ref="ppo"/>
        </material>

        <material formula=" " name="LAr">
            <D value="1.4" unit="g/cm3"/>
            <fraction n="1.0000" ref="argon"/>
        </material>

        <material formula=" " name="chip_silicon">
            <D value="2.3" unit="g/cm3"/>
            <fraction n="1.0" ref="silicon"/>
        </material>

        <material formula=" " name="borosilicate_glass">
            <D value="2.23" unit="g/cm3"/>
            <fraction n="0.05238" ref="silicon"/>
            <fraction n="0.55873" ref="oxygen"/>
            <fraction n="0.38889" ref="boron"/>
        </material>

        <material formula=" " name="photocathode">
            <D value="5.0" unit="g/cm3"/>
            <fraction n="1.0" ref="potassium"/>
        </material>

        <material formula=" " name="glass">
            <D value="2.23" unit="g/cm3"/>
            <fraction n="0.05238" ref="silicon"/>
            <fraction n="0.55873" ref="oxygen"/>
            <fraction n="0.38889" ref="boron"/>
        </material>

        <material formula=" " name="acrylic_uvt">
            <D value="1.18" unit="g/cm3"/>
            <fraction n="1.000" ref="carbon"/>
        </material>


    </materials>

    <solids>
        <box name="world"
            lunit="cm"
            x="300.0*2.54"
            y="300.0*2.54"
            z="300.0*2.54" />
        <tube name="cryostat" lunit="cm" aunit="deg" rmin="11*2.54" rmax="12*2.54" z="40.0*2.54" startphi="0" deltaphi="360.0"/>
        <tube name="cryostat_cap" lunit="cm" aunit="deg" rmin="0" rmax="12*2.54" z="2.0*2.54" startphi="0" deltaphi="360.0"/>
        <tube name="scint" lunit="cm" aunit="deg" rmin="0" rmax="11*2.54" z="40.0*2.54" startphi="0" deltaphi="360.0"/>
        <tube name="tpbplate" lunit="cm" aunit="deg" rmin="0" rmax="6*2.54" z="0.125*2.54" startphi="0" deltaphi="360.0"/>
        <tube name="pmtshield" lunit="mm" aunit="deg" rmin="100.5" rmax="101" z="136.65" startphi="0" deltaphi="360.0"/>
        <ellipsoid name="elpmt" ax="100.5" by="100.5" cz="64.5" zcut2="0" lunit="mm"/>
        <ellipsoid name="elouter" ax="101" by="101" cz="65" zcut2="0" lunit="mm"/>
        <ellipsoid name="elinner" ax="100.5" by="100.5" cz="64.5" zcut2="20" lunit="mm"/>
        <subtraction name="pmt_glass">
            <first ref="elouter"/>
            <second ref="elinner"/>
            <positionref ref="origin"/>
            <rotationref ref="identity"/>
        </subtraction>
        <!-- source holder is composed of 3 tubes
       bottom: rmin = 0      rmax = 1.75" z=0.40625"
       middle: rmin = 0.3cm  rmax = 1.75" z=0.09375"
       top:    rmin = 0.25cm rmax = 1.75" z=0.0625"
  -->
  <tube name="sourcediskA" lunit="cm" aunit="deg" rmin="0.0" rmax="1.75*1.27" z="0.40625*2.54" startphi="0" deltaphi="360.0"/> 
  <tube name="sourcediskB" lunit="cm" aunit="deg" rmin="0.3" rmax="1.75*1.27" z="0.09375*2.54" startphi="0" deltaphi="360.0"/>
  <tube name="sourcediskC" lunit="cm" aunit="deg" rmin="0.25" rmax="1.75*1.27" z="0.0625*2.54" startphi="0" deltaphi="360.0"/>

  <union name="sourcediskstage">
      <first ref="sourcediskA"/>
      <second ref="sourcediskB"/>
      <position name="posSourcestage" unit="cm" x="0" y="0" z="0.5*1.27"/>
      <rotationref ref="identity"/>
  </union>

  <union name="sourcediskD">
      <first ref="sourcediskstage"/>
      <second ref="sourcediskC"/>
      <position name="posSource" unit="cm" x="0" y="0" z="0.65625*1.27"/>
      <rotationref ref="identity"/>
  </union>

</solids>

<structure>

    <volume name="volGlass"> <!-- volPhotoCathode -->
        <materialref ref="glass"/> <!-- LAr -->
        <solidref ref="pmt_glass"/>
    </volume>
    <volume name="volTemp"> <!-- volTemp -->
        <materialref ref="glass"/> <!-- LAr -->
        <solidref ref="elpmt"/>
    </volume>
    <volume name="volPhotoCathode">
        <materialref ref="LAr"/> <!-- acrylic_uvt -->
        <solidref ref="tpbplate"/>
    </volume>
    <volume name="volPMTShield">
        <materialref ref="stainless_steel"/> <!-- acrylic_uvt -->
        <solidref ref="pmtshield"/>
    </volume>
    <!-- <volume name="volSourceA">
    <materialref ref="stainless_steel"/>
    <solidref ref="sourcediskA"/>
  </volume>-->
  <volume name="volSourceB">
      <materialref ref="stainless_steel"/>
      <solidref ref="sourcediskB"/>
  </volume>
  <volume name="volSourceC">
      <materialref ref="stainless_steel"/>
      <solidref ref="sourcediskC"/>
  </volume> 
  <volume name="volSourceD">
      <materialref ref="aluminum"/>
      <solidref ref="sourcediskD"/>
  </volume> 

  <volume name="volScint">
      <materialref ref="LAr"/>
      <solidref ref="scint"/>
      <!-- Add Photocathodes here -->

      <physvol name="pvGlass"> <!-- pvPMT00 -->
          <volumeref ref="volGlass"/>
          <position name="posGlass2" unit="mm" x="0" y="0" z="371.35"/>
      </physvol>

      <physvol name="pvTemp">
          <volumeref ref="volTemp"/>
          <position name="posGlass" unit="mm" x="0" y="0" z="371.35"/>
      </physvol> 
<!-- the following volume is the tpb plate -->
    <physvol name="pvPMT00">
        <volumeref ref="volPhotoCathode"/> <!-- volTPBPlate -->
        <position name="posPlate" unit="mm" x="0" y="0" z="301.5875"/>
    </physvol>
    <physvol name="pvShield">
        <volumeref ref="volPMTShield"/> <!-- volTPBPlate -->
        <position name="posShield" unit="mm" x="0" y="0" z="439.675"/>
    </physvol>

    <!-- End of photocathodes --> 
    <physvol name="pvSourceD">
        <volumeref ref="volSourceD"/>
<position name="posSource" unit="mm" x="0" y="0" z="87.871875"/>
    </physvol>
    <!--
    <physvol name="pvSource">
      <volumeref ref="volSource"/>
<position name="posSource" unit="mm" x="0" y="0" z="87.871875"/>
    </physvol>-->
    <!-- End of photocathodes --> 
    <!--    <physvol name="pvSourceD">
      <volumeref ref="volSourceD"/>
<position name="posSource" unit="mm" x="0" y="0" z="-77.128125"/>
    </physvol>-->
<!--
    <physvol name="pvSource">
      <volumeref ref="volSource"/>
<position name="posSource" unit="mm" x="0" y="0" z="87.871875"/>
    </physvol>

    <physvol name="pvSourceA">
      <volumeref ref="volSourceA"/>
<position name="posSource" unit="mm" x="0" y="0" z="0"/>
    </physvol>
    <physvol name="pvSourceB">
      <volumeref ref="volSourceB"/>
<position name="posSource" unit="cm" x="0" y="0" z="-0.15625*1.27"/>
    </physvol>
    <physvol name="pvSourceC">
      <volumeref ref="volSourceC"/>
<position name="posSource" unit="cm" x="0" y="0" z="-0.65625*1.27"/>
    </physvol>
-->
  </volume>

  <volume name="volCryo">
      <materialref ref="stainless_steel"/>
      <solidref ref="cryostat"/>
  </volume>

  <volume name="volCryoCap">
      <materialref ref="stainless_steel"/> <!-- stainless_steel -->
      <solidref ref="cryostat_cap"/>
  </volume>

  <volume name="volWorld">
      <materialref ref="air"/>
      <solidref ref="world"/>

      <physvol name="pvCryo">  <!-- pvCryo -->
          <volumeref ref="volCryo"/>
          <position name="posCryo" unit="cm" x="0" y="0" z="0"/>
      </physvol>

      <physvol name="pvCryoCap1">
          <volumeref ref="volCryoCap"/>
          <position name="posCryoCap1" unit="cm" x="0" y="0" z="21*2.54"/> <!-- 32.69975 -->
      </physvol>
      <physvol name="pvCryoCap2">
          <volumeref ref="volCryoCap"/>
          <position name="posCryoCap2" unit="cm" x="0" y="0" z="-21*2.54"/> <!-- -9.737875 -->
      </physvol>

      <physvol name="pvScint">
          <volumeref ref="volScint"/>
          <position name="posScint" x="0" y="0" z="0"/>
      </physvol>

  </volume>
</structure>

<setup name="Default" version="1.0">
    <world ref="volWorld" />
</setup>

</gdml>
"""

def scriptstring(*args, **kwargs):
    return """#!/bin/bash

## CONFIGURATION ##
# Source to plate simulation files
MACFILEPLT='mac/bo_final.mac'
GDMLFILEPLT='data/bo_final/bo_final.gdml'

# Plate to PMT simulation files
MACFILESRC='mac/bo_src.mac'
GDMLFILESRC='data/bo_src/bo_src.gdml'

# Radii to test for Plate to PMT simulation
PLTLIST=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 15.24)

# Radii to test for source to plate simulation
ROFLIST=( 0.0 0.025 0.05 0.075 0.1 0.15 0.2 0.25 0.295 0.3) 

# Events/pt for each simulation
NEVENTSPLT=100000
NEVENTSSRC=100000

# Source holder position
# originally meant to be a list, but probably won't work if more than 1 number
DISTLIST=( 9.7 )

## END CONFIGURATION ##

RUNPATH=`pwd`"/output/"$1"/"
echo "Saving output to "$RUNPATH

mkdir -p $RUNPATH

## Generate the weight file
if [ -f "$RUNPATH"weights.txt ] && [ "$2" != "new" ] ; then
    echo "Found weight file."
    ## Save local copy to run directory
    # cp analysis/weights.txt "$RUNPATH"weights.txt
else
    rm -f "$RUNPATH"weights.txt # -f option suppresses error if file doesn't exist
    echo "Events/Point: "$NEVENTSPLT
    echo "Creating weight file..."

    for i in "${PLTLIST[@]}";
    do
        echo "Processing r="$i"cm"
        len=`echo "$i*10" | bc -l`
        #replace vertex lines in mac file
        line='21s/.*/\/generator\/pos\/set '$len' 0.0 300.01/'
        line2='27s/.*/\/run\/beamOn '$NEVENTSPLT'/'
        sed -i "$line" $MACFILEPLT
        sed -i "$line2" $MACFILEPLT
        #run rat & root file
        rat -q $MACFILEPLT
        root -l -b -q 'analysis/PlateCount.cc("'$RUNPATH'", '$NEVENTSPLT', '$len')'
    done
fi

## At this point, "$RUNPATH"weights.txt should exist!
## this root script saves the weight file as a graph and fits it
root -l -b -q 'analysis/PlateFit.cc("'$RUNPATH'", '$NEVENTSPLT')'

## Do source to plate simulation
if [ 1 -eq 1 ]; then # 'if' wrapper is for testing. Set to 1 -eq 0 to disable this block
    rm -f "$RUNPATH"pltweights.txt
    echo "Starting source to plate simulation."
    for i in "${DISTLIST[@]}" # again, probably should not have more than one distance in here...
    do
        for j in "${ROFLIST[@]}"
        do
            #rd is radial offset variable
            rd=`echo "($j*10)" | bc -l`	
            #len is variable for starting point source position
            len=`echo "($i*10)-""" + '{}" | bc -l` #-3.96875'.format(kwargs['sourceheight']) + \
            """        \n#len2 is variable for starting source holder position
            len2=`echo "($i*10)-9.128125" | bc -l` #const offset puts face of holder at 'd' away
            len3=`echo "300-($i*10)" | bc -l`

            echo "Processing d="$len3"mm, r="$rd"mm"

            #replace vertex lines in mac file
            line='21s/.*/\/generator\/pos\/set 0.0 '$rd' '$len'/'
            sed -i "$line" $MACFILESRC
            
            #replace position line in GDML file
            line2='237s/.*/<position name="posSource" unit="mm" x="0" y="0" z="'$len2'"\/>/'
            sed -i "${line2}" $GDMLFILESRC

            #replace event line in mac file
            line3='27s/.*/\/run\/beamOn '$NEVENTSSRC'/'
            sed -i "$line3" $MACFILESRC

            #run rat & root script
            rat -q $MACFILESRC
            root -l -b -q 'analysis/WeightedHits.cc("'$RUNPATH'")'
        done
    done
    # old version python analysis/circledist.py $RUNPATH #log_process.py $RUNPATH
fi

# final creation of pe spectrum
root -l -b -q 'analysis/PESpectrum.cc("'$RUNPATH'",'$NEVENTSSRC')'

# clean up RAT log files
rm *.log
"""
