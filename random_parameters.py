#!/usr/env/bin python

# Script to randomize optical parameters

import numpy as np
import json
import sys

from strings import *

opticsparams = {
        'rayleigh': {'mean': 600, 'sigma': 60},
        'ssref_128': {'mean': 0.35, 'sigma': 0.05},
        'ssref_420': {'mean': 0.54, 'sigma': 0.005},
        'alref_128': {'mean': 0.12, 'sigma': 0.02},
        'nlar_128': {'mean': 1.45, 'sigma': 0.07},
        'nlar_420': {'mean': 1.23, 'sigma': 0.002},
        'nglass_420': {'mean': 1.46, 'sigma': 0.04},
        'nacrylic_420': {'mean': 1.49, 'sigma': 0.02},
        }

geoparams = {
        'glassthick': {'mean': 0.5, 'sigma': 0.1}, # cm
        'platepmtdist': {'mean': 0.13, 'sigma': 0.03}, # in
        }

srcgeoparams = {
        'colimatorheight': {'mean': 0.16, 'sigma': 0.03}, #in NOT IMPLEMENTED
        }

scriptparams = {
        'sourceheight': {'mean': 0.01, 'sigma': 0.002}, #cm
        'd': {'mean': 20.3, 'sigma': 0.4}, #cm NOT IMPLEMENTED
        }

sourceparams = {
        'sourcewidth': {'mean': 0.5, 'sigma': 0.4},
        'phperalpha': {'mean': 134000, 'sigma': 4000},
        'qe': {'mean': 0.153, 'sigma': 0.008},
        'tpbeff': {'mean': 0.4, 'sigma': 0.04},
        'tempscale': {'mean': 1.22, 'sigma': 0.15},
        'tpbreleff': {'mean': 0.67, 'sigma': 0.06},
        }

def random_params():
    opticsvals = {}
    for param, data in opticsparams.iteritems():
        opticsvals[param] = '%.3f' % (np.random.normal(data['mean'], data['sigma']))

    geovals = {}
    for param, data in geoparams.iteritems():
        if param == 'glassthick':
            rnd = np.random.normal(data['mean'], data['sigma'])
            val = 101 - rnd
            val2 = 65 - rnd
            if val < 0:
                val == 100.99
                val2 == 64.99
            geovals[param] = '%.3f' % (val)
            geovals['glassthick2'] = '%.3f' % (val2)
        elif param == 'platepmtdist':
            val = 301.5875 + 0.125*25.4*0.5+65+np.random.normal(data['mean'], data['sigma'])*25.4
            geovals[param] = '%.3f' % (val)
        else:
            geovals[param] = '%.3f' % (np.random.normal(data['mean'], data['sigma']))

    srcgeovals = {}
    for param, data in srcgeoparams.iteritems():
        srcgeovals[param] = '%.3f' % (np.random.normal(data['mean'], data['sigma']))

    scriptvals = {}
    for param, data in scriptparams.iteritems():
        if param == 'sourceheight':
            val = 3.96875 - np.random.normal(data['mean'], data['sigma'])
            scriptvals[param] = '%.3f' % (val)
        else:
            scriptvals[param] = '%.3f' % (np.random.normal(data['mean'], data['sigma']))


    sourcevals = {}
    for param, data in sourceparams.iteritems():
        sourcevals[param] = '%.3f' % (np.random.normal(data['mean'], data['sigma']))

    return {
            'optics': opticsvals, 
            'geo': geovals, 
            'srcgeo': srcgeovals, 
            'script': scriptvals, 
            'source': sourcevals,
            }

def main():
    mode = sys.argv[1]
    if mode in ['r', 'x']:
        if mode == 'r':
            lineid = int(sys.argv[2])
            with open('{}/paramlist.txt'.format(sys.argv[3]), 'r') as f:
                for i, line in enumerate(f):
                    if i == lineid:
                        params = json.loads(line)
                        print(params)
                        break
        elif mode == 'x':
            params = random_params()

        with open('data/OPTICS.ratdb', 'w') as f:
            f.write(opticsstring(**params['optics']))

        with open('data/bo_final/bo_final.gdml', 'w') as f:
            f.write(geostring(**params['geo']))

        with open('data/bo_src/bo_src.gdml' , 'w') as f:
            f.write(srcgeostring(**params['srcgeo']))

        with open('bo_total_autorun.sh', 'w') as f:
            f.write(scriptstring(**params['script']))

        with open('analysis/PESpectrum.cc', 'w') as f:
            f.write(sourcestring(**params['source']))

    elif mode == 'n':
        nlines = int(sys.argv[2])
        with open('{}/paramlist.txt'.format(sys.argv[3]), 'w') as f:
            for _ in range(nlines):
                json.dump(random_params(), f)
                f.write('\n')

if __name__ == '__main__':
    main()
