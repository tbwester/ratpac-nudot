#!/bin/bash

MACFILE='mac/bo_final.mac'
#pi=`echo "4*a(1)" | bc -l`

#for i in `seq 0 15`;
array=( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 )
for i in "${array[@]}"
do
	len=`echo "$i*10" | bc -l`

	#replace vertex lines in mac file
    line='21s/.*/\/generator\/pos\/set '$len' 0.0 300.001/'
    sed -i "$line" $MACFILE

	#run rat & python script
	rat $MACFILE
    root -l -b -q "analysis/pecount_weight.C($len)"
	#analysis/simple_scatter.py $len
done
