# GET JOBID FROM ARGUMENTS
JOBID=$1
NUDOT_OUT=$2
NEVENTS=$3

# SETUP LOCAL PYTHON
tar zxvf python2.6.9.tar > /dev/null

# SETUP RAT
tar zxvf rat.tar.gz > /dev/null
source ratpac-nudot/tier2scripts/env_condornode_localpython.sh

# GEN MACRO
RATMAC=nudot_beta_job"$JOBID".mac
python ratpac-nudot/tier2scripts/gen_macro.py $RATMAC $JOBID $NEVENTS
cat $RATMAC

# RUN JOB
rat $RATMAC -o $NUDOT_OUT

# CLEAN UP
rm -rf ratpac-nudot
rm -rf export
rm $RATMAC