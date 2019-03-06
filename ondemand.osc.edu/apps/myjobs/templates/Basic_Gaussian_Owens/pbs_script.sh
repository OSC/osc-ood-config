#PBS -N ondemand/sys/myjobs/basic_gaussian
#PBS -l walltime=0:30:00
#PBS -l nodes=1:ppn=28
#PBS -j oe 
#PBS -S /bin/csh

# A Basic Gaussian Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/gaussian

# PBS_O_WORKDIR refers to the directory from which the job was submitted.

# Emit verbose details as the job script executes.
set echo
set verbose
# Emit verbose details on the job's queuing.
qstat -f $PBS_JOBID

#
# The following lines set up the Gaussian environment
#
module load gaussian/g16a03
#
# Move to the directory where the job was submitted
#
cd $TMPDIR
cp -p /users/appl/srb/workshops/compchem/gaussian/c80.owens.com .
#
# Run Gaussian
#
g16 < c80.owens.com
ls -al
#
# Now, copy data (or move) back once the simulation has completed
#
cp -p *.chk $PBS_O_WORKDIR
