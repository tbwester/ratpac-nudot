## Some notes on running on Tier 2

Access to network disks are now limited.  The idea is to push most of one's files to and from the worker node.  Reduces network traffic.

However, there is one location

<pre>
/cvmfs/cvmfs.cmsaf.mit.edu/t2srv0008/export/app/ 
</pre>

which is accessable by the worker nodes. It is READ-ONLY and not meant to change much.  One can only modify this area when logged into the t2srv0008 node. However, changes to this area propagate every 15 minutes or so to the batch system.  This means that only external software packages like ROOT and GEANT4 make sense to live here.  Things like RAT or one's analysis code, which will be modifying regularly, SHOULD NOT go into this space.  Such code must be pushed to the worker node. I have been some tools to help do this.  (Or if you prefer to write your own condor scripts, I hope this helps to show one how.)

(note to self, ask Lindley to get a NuDot folder on /cvmfs/cvmfs.cmsaf.mit.edu/t2srv0008/export/app/  -- or we can keep using dChooz)

Additional note: the environment is SL5, which is ancient.  I'm working on figuring out a way to get a better, more modern environment using Gentoo prefix. (I'm getting help with this from Gabriel Collin.)

## Example Job

In the nudot RAT repository, there are tier 2 scripts (in the tier2scripts folder) to make this process a bit easier.  The idea behind these scripts is to setup a json file (which looks like a python dictionary) and then run the submission program, run_tier2.py.  The program uses the json file to setup a bunch of condor job files, which it submits and tracks for you.

This example job generates a bunch of electrons isotropically in the tank.

### Components

* run_nudot_beta.sh: This is the script that launches the jobs. It also unpacks a tar ball containing RAT and another tarball containing a local copy of python the job requires. This script launches the RAT job.

* example_cfg.json: This is the json file that configures the job.  It wants to know the executable script (in this case run_nudot_beta.sh), the number of jobs, the ID ranges condor should give the jobs, the tarballs it should ship to the worker node, and the arguments to the scripts, which will be added to the condor submission script.

* env_condornode.sh and env_condornode_localpython.sh: These are called by the example script above to setup the environment on the worker node.  Note how it sets up the binary and library folders for the packages in the read only network disk, /cvmfs/cvmfs.cmsaf.mit.edu/t2srv0008/export/app/. Also note that this will be part of the RAT tarball, so it gets shipped to the worker nodes.

### Arguments to the run_tier2.py tool

<pre>
$ python run_tier2.py --help
usage: run_tier2.py [-h] [--check] [--submit] [--redo] [--test]
                    [--limit LIMIT]
                    setup_file

Manage Tier 2 Submissions

positional arguments:
  setup_file     json file with setup of submission

optional arguments:
  -h, --help     show this help message and exit
  --check        only checks if all files made
  --submit       submit jobs (does not resubmit completed files)
  --redo         submit jobs (will resubmit completed files)
  --test         test mode. runs until submission, which it will skip. makes
                 the condor scripts.
  --limit LIMIT  limit the number of jobs made
</pre>

### Running the run_tier2.py tool

Note: before submitting jobs, run the program in test mode to make sure all the scripts are what you expect!

<pre>
$ python run_tier2.py --test example_cfg.json
</pre>

Check your condor scripts (will be made in the ./condor_scripts/ folder). See an example in the next section.

If everything looks OK:

<pre>
$ python run_tier2.py --submit example_cfg.json
</pre>

To check the status of your jobs:

<pre>
$ python run_tier2.py --check example_cfg.json
</pre>

### The Configuration JSON file

Example of a file

<pre>
{ "job": {
      	"script":"/net/hisrv0001/home/taritree/nudot/ratpac-nudot/tier2scripts/run_nudot_beta.sh",
	"startjob":"0",
	"njobs":"20",
	"nargs":"3",
	"packagefiles":["/net/hisrv0001/home/taritree/nudot/rat.tar.gz",
			"/net/hisrv0001/home/taritree/kpipe/production/python2.6.9.tar"],
	"args":[ {"argname":"id","value":"%d","njobids":"1","transfer":"False","type":"arg"},
		 {"argname":"kdar-out","value":"output_nudot_%05d.root","njobids":"1","transfer":"True","type":"output","dest":"spacing30cm"},
	 	 {"argname":"events","value":"1000","njobids":"0","transfer":"False","type":"arg"} ]
	}
}
</pre>

The trickiest part of this file is the argument list provided in "args":[...,...,...]. The order matters, the are given to the executable script in the order they appear in the list.

Each argument is provided as a dictionary with the following structure:

* "argname":just the name given to the argument, used internally
* "value": the value of the argument. Note that you can provide a location for an integer in the argument. We will pass the job number to this argument.
* "type":either can be "arg", "input", "output". If "output", then this file will be asked to be transferred from the node back to the folder from which run_tier2.py was called. If "input", then this file will be marked to be transferred to the node.
* "transfer":If "type" was either "input" or "output". Then this file will be transferred to/from the node.
* "njobids":Number of jobs to be passed into this argument (check this).

### Example condor script made by run_tier2.py

This is the condor script generated by run_tier2.py using the configuration json file.

<pre>
# Generated Tier 2 KPipe Condor submission file
# --------------------------------------------
Universe                = vanilla
Environment             ="HOSTNAME=$HOSTNAME"
Requirements            = UidDomain == "cmsaf.mit.edu" && Arch == "X86_64" && HasFileTransfer
Executable              =  /net/hisrv0001/home/taritree/nudot/ratpac-nudot/tier2scripts/run_nudot_beta.sh
Arguments               =   0 output_nudot_00000.root 1000
Input                   = /dev/null
Output                  = condor_out/condor_job0.out
Error                   = condor_err/condor_job0.err
Log                     = condor.log
transfer_input_files    =  /net/hisrv0001/home/taritree/nudot/rat.tar.gz, /net/hisrv0001/home/taritree/kpipe/production/python2.6.9.tar
transfer_output_files =  output_nudot_00000.root
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
+AccountingGroup = "group_mitlns.taritree"
Queue
# --------------------------------------------
</pre>
