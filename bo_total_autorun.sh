#!/bin/bash

MACFILE='mac/bo_total.mac'
GDMLFILE='data/bo_total/bo_total.gdml'
#pi=`echo "4*a(1)" | bc -l`

for i in `seq 0 1`; #original line 
#for i in `seq -5 1 5`;
do
	#len is variable for starting source position
	len=`echo "($i*10)-1.9" | bc -l`
	#len2 is variable for starting source holder position
	len2=`echo "($i*10)" | bc -l`

	#replace vertex lines in mac file
        line='21s/.*/\/generator\/pos\/set 0.0 0.0 '$len'/'
        sed -i "$line" $MACFILE
        
        line2='249s/.*/<position name="posSource" unit="mm" x="0" y="0" z="'$len2'"\/>/'
        sed -i "${line2}" $GDMLFILE

	#run rat & python script
	rat $MACFILE
        root -l -b -q "analysis/pecount_weight.C($len2)"
	#analysis/simple_scatter.py $len
done

rm *.log
