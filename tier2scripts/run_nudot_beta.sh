# GET JOBID FROM ARGUMENTS
JOBID=$1
NUDOT_OUT=$2
NEVENTS=$3

# SETUP LOCAL PYTHON (We shipped this to the node)
# This local python is needed to run the gen_macro.py script below
tar zxvf python2.6.9.tar > /dev/null

# SETUP RAT (We shipped this to the node)
tar zxvf rat.tar.gz > /dev/null

# We setup the environment for RAT and the local python we provided
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