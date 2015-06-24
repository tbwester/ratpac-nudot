import os,sys

def gen_macro( outfile, jobid, nevents_per_job ):
    part1 = """/glg4debug/glg4param omit_muon_processes  0.0
/glg4debug/glg4param omit_hadronic_processes  0.0

/rat/db/set DETECTOR experiment \"nudotv0\"
/rat/db/set DETECTOR geo_file \"nudotv0/nudotv0.geo\"
#/tracking/storeTrajectory 1
#/tracking/discardParticleTrajectory opticalphoton

/run/initialize

# BEGIN EVENT LOOP
/rat/proc count
/rat/procset update 10

# Use IO.default_output_filename
/rat/proclast outroot
#END EVENT LOOP
"""

    run_str = "/run/beamOn %d"%(nevents_per_job)
    fout = open( outfile, 'w' )
    print >> fout,part1
    print >> fout,""
    print >> fout,"/generator/add combo gun2:point:uniform"
    print >> fout,"/generator/vtx/set e-  0.0 0.0 0.0 0.0 1.1 1.1"
    print >> fout,"/generator/pos/set 0 0 200.0"
    print >> fout,""
    print >> fout,run_str
    fout.close()
    

if __name__=="__main__":

    outfile = sys.argv[1]
    jobid = int(sys.argv[2])
    nevents_per_job = int(sys.argv[3])

    gen_macro( outfile, jobid, nevents_per_job )
