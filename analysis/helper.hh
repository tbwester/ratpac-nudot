// ====================================================
//
// helper.hh
// Thomas Wester July 2017
// 
// Helper functions for analysis scripts
//
// ====================================================

#ifndef _HELPER_HH
#define _HELPER_HH

#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <string>
#include <stdlib.h>

#include "TMath.h"
#include "TDatime.h"

typedef std::vector<double> dblvec;

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

std::vector<dblvec> vecfromfile(string fname) {
    //Fill weight vector from file
    std::vector<dblvec> vec;
    std::ifstream ifile;
    ifile.open(fname);
    string line;
    while (ifile >> line) {
        //Split string at comma
        dblvec v;
        stringstream ss(line);
        string d;
        while (getline(ss, d, ',')) {
            v.push_back(std::atof(d.c_str()));
        }
        vec.push_back(v);
    }
    ifile.close();

    return vec;
}

string datetime() {
    //Return string of format YYYYMMDD-HHMMSS
    TDatime t;
    stringstream ss;
    ss << t.GetDate() << "-" << t.GetTime();

    return ss.str();
}

#endif
