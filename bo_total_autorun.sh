#!/bin/bash

## CONFIGURATION ##
# Source to plate simulation files
MACFILEPLT='mac/bo_final.mac'
GDMLFILEPLT='data/bo_final/bo_final.gdml'

# Plate to PMT simulation files
MACFILESRC='mac/bo_src.mac'
GDMLFILESRC='data/bo_src/bo_src.gdml'

# Fine-ness, events, etc.
PLTR=2 #15.24
DSTEP=1
NEVENTS=1000
## END CONFIGURATION ##

## Generate the weight file
if [ -f analysis/weights.txt ] && [ "$1" != "new" ] ; then
    echo "Found weight file."
else
    echo "Plate Radius: "$PLTR
    echo "Step Size: "$DSTEP
    echo "Events/Point: "$NEVENTS
    echo "Creating weight file..."

    for i in `seq 0 $DSTEP $PLTR`;
    do
        echo "Processing r="$i"cm"
        len=`echo "$i*10" | bc -l`
        #replace vertex lines in mac file
        line='21s/.*/\/generator\/pos\/set '$len' 0.0 300.001/'
        line2='27s/.*/\/run\/beamOn '$NEVENTS'/'
        sed -i "$line" $MACFILEPLT
        sed -i "$line2" $MACFILEPLT
        #run rat & python script
        rat -q $MACFILEPLT
        #root -l -b -q "analysis/pecount_weight.C($len)"
    done
fi

## Do source to plate simulation

## Clean up
rm *.log
