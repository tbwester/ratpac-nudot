#!/bin/bash

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
NEVENTSPLT=10000
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
            len=`echo "($i*10)-3.95875" | bc -l` #-3.96875
            #len2 is variable for starting source holder position
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
