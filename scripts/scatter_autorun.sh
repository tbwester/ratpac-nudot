#!/bin/bash

MACFILE='mac/scatter.mac'
#pi=`echo "4*a(1)" | bc -l`

for i in `seq -19 20`;
do
	len=`echo "$i*50" | bc -l`

	#replace vertex lines in mac file
        line='21s/.*/\/generator\/pos\/set 0.0 0.0 '$len'/'
        sed -i "$line" $MACFILE

	#run rat & python script
	rat $MACFILE
        root -lbq "analysis/pecount.C($len)"
	#analysis/simple_scatter.py $len
done
