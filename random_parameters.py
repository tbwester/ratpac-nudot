#!/usr/env/bin python

# Script to randomize optical parameters

import numpy as np

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
        'sourceheight': {'mean': 0.01, 'sigma': 0.002}, #cm
        'glassthick': {'mean': 0.5, 'sigma': 0.1}, # cm
        'platepmtdist': {'mean': 0.13, 'sigma': 0.03}, # in
        'colimatorheight': {'mean': 0.16, 'sigma': 0.03}, #in
        'd': {'mean': 20.3, 'sigma': 0.4},
        }

sourceparams = {
        'sourcewidth': {'mean': 0.5, 'sigma': 0.4},
        }

def random_params():
    opticsvals = {}
    for param, data in opticsparams.iteritems():
        opticsvals[param] = '%.3f' % (np.random.normal(data['mean'], data['sigma']))

    geovals = {}
    for param, data in geoparams.iteritems():
        geovals[param] = '%.3f' % (np.random.normal(data['mean'], data['sigma']))

    sourcevals = {}
    for param, data in sourceparams.iteritems():
        sourcevals[param] = '%.3f' % (np.random.normal(data['mean'], data['sigma']))

    return opticsvals, geovals, sourcevals

if __name__ == '__main__':
    #print(opticsstring(**random_params()[0]))
    print(sourcestring(**random_params()[2]))
