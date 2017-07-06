#include <iostream>

#include "TTree.h"
#include "TFile.h"
#include <RAT/DS.hh>

using namespace std;

void getnumpe() {

    RAT::DSReader r("output.root");
    RAT::DS::Root *ds = r.NextEvent();
    RAT::DS::MC *mc = ds->GetMC();
    Int_t npes = mc->GetNumPE();

    TFile* f = TFile::Open("output.root");
    Int_t npe;

    TTree* tree = (TTree*)f->Get("T");
    tree->SetBranchAddress("mc.numPE", &npe);

    Int_t nentries = tree->GetEntries();
    Int_t totalhits = 0;
    
    for (int i = 0; i < nentries; i++) {
        tree->GetEntry(i);
        totalhits += npe;
    }
    tree->Draw("mc.numPE");
    cout << "Total hits: " << totalhits << "/" << nentries << endl;

//    DSReader dsroot = reader.NextEvent();
//    cout <<  dsroot.GetNumPE() << endl;

}
