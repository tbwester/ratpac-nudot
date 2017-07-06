
# NuDOT rat-pac fork

Simulation code for NuDot

This fork contains geometry, scripts and settings for the Bo cryostat optical monte carlo

## Checking out

* using git flow pattern (more info: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)
* git clone https://github.com/NuDot/ratpac-nudot.git
* git checkout develop (this moves you to the develop branch)

## Dependencies
* ROOT 6 (tested with v6.08/02)
* Geant4 (tested with v4.10.03)
* scons


## building
* instructions in doc/installation.rst
* make sure ROOT and geant4 environment variables set
* ./configure
* scons

## Running Bo optical simulation
* ./bo\_src\_autorun.sh
* ./bo\_final\_autorun.sh

The first command produces an ntuple of photon hits on the TPB plate. The second command outputs the number of hits on the PMT from photons coming from the TPB plate.


## Adding a feature
* git checkout develop
* git checkout -b [username]_[featurename]
* do something awesome
* to put your code onto develop: git checkout develop; git merge [username]_[featurename]
* delete the branch

## Chroma Interface Optional

This copy has an extremely developmental feature: an interface to Chroma, which simulates photon transport on a GPU. Current state is that it is not really working.

But to build with it anyway:

* go into ./configure and change USECHROMA=1
* one needs to have zmq and google protobufs
* one also needs to clone and install the ratchroma interface ...

## Geometry

## Optical Detector

* Needed to add new type of Sensitive Detector class for optical detectors
* RAT optical detectors too tied to PMTs
* Created GLG4SimpleOpDetSD.  No fancy physics. If opticalphoton hits it, then a hit gets made. (later we can maybe configure this.)
* To add it, include opdet_lv_name in GEO RAT db table.
* Also, in GDML give each physvol instance a name with a number. This number will be used to assign the opdet a channel number.
* example:
```
[In GEO table]
{
name: "GEO",
valid_begin: [0, 0],
valid_end: [0, 0],
gdml_file: "nudot.gdml",
opdet_lv_name: "volSiPM",
}

[in GDML file]
...
    <physvol name="OpDet1">
      <volumeref ref="volSiPM"/>
      <position name="posSiPM1" unit="cm" x="0" y="0" z="0"/>
    </physvol>
    <physvol name="OpDet2">
      <volumeref ref="volSiPM"/>
      <position name="posSiPM2" unit="cm" x="0" y="0" z="10"/>
    </physvol>
...
```


# RAT (is an Analysis Tool), Public Edition
-----------------------------------------
RAT is a simulation and analysis package built with GEANT4, ROOT, and C++,
originally developed by S. Seibert for the Braidwood Collaboration. Versions
of RAT are now being used and developed by several particle physics
experiments.

RAT combines simulation and analysis into a single framework, which allows
analysis code to trivially access the same detector geometry and physics
parameters used in the detailed simulation.

RAT follows the "AMARA" principle: As Microphysical as Reasonably Achievable.
Each and every photon is tracked through an arbitrarily detailed detector
geometry, using standard GEANT4 or custom physics processes. PMTs are fully
modeled, and detected photons may be propagated to a simulation of front-end
electronics and DAQ.

This generic version is intended as a starting point for collaborations
looking for an easy-to-learn, extensible detector simulation and analysis
package that works out of the box. Once acquainted with RAT, it is easy to
customize the geometry elements, physics details, data structure, analysis
tools, etc., to suit your experiment's needs.

