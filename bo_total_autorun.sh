#!/bin/bash

## CONFIGURATION ##
# Source to plate simulation files
MACFILEPLT='mac/bo_final.mac'
GDMLFILEPLT='data/bo_final/bo_final.gdml'

# Plate to PMT simulation files
MACFILESRC='mac/bo_src.mac'
GDMLFILESRC='data/bo_src/bo_src.gdml'

# Fine-ness, events, etc.
PLTR=15.24
DSTEP=1
NEVENTSPLT=10000
NEVENTSSRC=100000
DISTLIST=( -6.8 9.7 6 7 8 9 10 11 12 13 14 )
ROFLIST=( 0.0 ) #( 0.0 0.05 0.1 0.15 0.2 0.25 ) 
## END CONFIGURATION ##

## Generate the weight file
if [ -f analysis/weights.txt ] && [ "$1" != "new" ] ; then
    echo "Found weight file."
else
    rm analysis/weights.txt
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
        line2='27s/.*/\/run\/beamOn '$NEVENTSPLT'/'
        sed -i "$line" $MACFILEPLT
        sed -i "$line2" $MACFILEPLT
        #run rat & python script
        rat -q $MACFILEPLT
        root -l -b -q "analysis/pecount_weight.C($len)"
    done
fi

## Do source to plate simulation
if [ 1 -eq 1 ]; then
    echo "Starting source to plate simulation."
    for i in "${DISTLIST[@]}"
    do
        for j in "${ROFLIST[@]}"
        do
           
            #rd is radial offset variable
            rd=`echo "($j*10)" | bc -l`	
            #len is variable for starting source position
            len=`echo "($i*10)-3.96875" | bc -l` #-3.96875
            #len2 is variable for starting source holder position
            len2=`echo "($i*10)-9.128125" | bc -l` #const offset puts face of holder at 'd' away
            len3=`echo "300-($i*10)" | bc -l`

            echo "Processing d="$len3"mm, r="$rd"mm"

            #replace vertex lines in mac file
            line='21s/.*/\/generator\/pos\/set 0.0 '$rd' '$len'/'
            sed -i "$line" $MACFILESRC
            
            line2='228s/.*/<position name="posSource" unit="mm" x="0" y="0" z="'$len2'"\/>/'
            sed -i "${line2}" $GDMLFILESRC

            line3='27s/.*/\/run\/beamOn '$NEVENTSSRC'/'
            sed -i "$line3" $MACFILESRC

            #run rat & root script
            rat -q $MACFILESRC
            root -l -b -q "analysis/gqe.C()"  #$len3, $rd)"
        done
    done
fi
rm *.log
