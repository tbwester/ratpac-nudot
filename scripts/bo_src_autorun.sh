#!/bin/bash

MACFILE='mac/bo_src.mac'
GDMLFILE='data/bo_src/bo_src.gdml'
#pi=`echo "4*a(1)" | bc -l`

#for i in `seq -29 29`; #original line 
#for i in `seq -5 1 5`;
distlist=( -6.8 )
roflist=( 0.0 ) #( 0.0 0.05 0.1 0.15 0.2 0.25 ) 
for i in "${distlist[@]}"
do
	for j in "${roflist[@]}"
	do
        #rd is radial offset variable
        rd=`echo "($j*10)" | bc -l`	
        #len is variable for starting source position
        len=`echo "($i*10)-3.96875" | bc -l` #-3.96875
        #len2 is variable for starting source holder position
        len2=`echo "($i*10)-9.128125" | bc -l` #const offset puts face of holder at 'd' away

        #replace vertex lines in mac file
        line='21s/.*/\/generator\/pos\/set 0.0 '$rd' '$len'/'
        sed -i "$line" $MACFILE
        
        line2='228s/.*/<position name="posSource" unit="mm" x="0" y="0" z="'$len2'"\/>/'
        sed -i "${line2}" $GDMLFILE

        #run rat & root script
        len3=`echo "300-($len)" | bc -l`

        echo $len3
        rat $MACFILE
        #root -l -b -q "analysis/pecount_weight.C($len3)"
        root -l -b -q "analysis/rayleigh.C()"  #$len3, $rd)"
        #analysis/simple_scatter.py $len
	done
done

rm *.log
