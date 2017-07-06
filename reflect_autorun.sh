#!/bin/bash

# the round function:
round()
{
echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
};

MACFILE='mac/reflect_shell.mac'
pi=`echo "4*a(1)" | bc -l`

for i in `seq 1 17`;
do
	#Get angle in radians, calculate sin/cos
        deg=`echo "$i*5" | bc -l`
	rad=`echo "$i*5*($pi/180)" | bc -l`
	sin=`echo "1000*s($rad)" | bc -l`
	cos=`echo "1000*c($rad)" | bc -l`
	
	#replace vertex lines in mac file
	line='20s/.*/\/generator\/vtx\/set opticalphoton  '$(round $cos 3)' -'$(round $sin 3)' 0.0 0.00000295/'
	line2='21s/.*/\/generator\/pos\/set -'$(round $cos 3)' '$(round $sin 3)' 0.0/'
	#echo $line
	#echo $line2
        sed -i "$line" $MACFILE
	sed -i "$line2" $MACFILE

	#run rat & python script
	rat $MACFILE
	analysis/simple.py $deg
done
