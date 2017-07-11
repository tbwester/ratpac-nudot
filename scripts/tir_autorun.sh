#!/bin/bash

MACFILE='mac/tir.mac'
#pi=`echo "4*a(1)" | bc -l`

for i in `seq -9 9`;
do
	len=`echo "$i*10" | bc -l`

	#replace vertex lines in mac file
        line='21s/.*/\/generator\/pos\/set 0.0 0.0 '$len'/'
        sed -i "$line" $MACFILE

	#run rat & python script
	rat $MACFILE
        root -l -b -q "analysis/pecount.C($len)"
	#analysis/simple_scatter.py $len
done

rm *.log
