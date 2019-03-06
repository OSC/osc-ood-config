#PBS -N ondemand/sys/myjobs/basic_gaussian
#PBS -l walltime=00:30:00
#PBS -l nodes=1:ppn=40
#PBS -j oe 
#PBS -S /bin/csh

# A Basic Gaussian Job for the OSC Pitzer Cluster
#   https://www.osc.edu/resources/available_software/software_list/gaussian

# PBS_O_WORKDIR refers to the directory from which the job was submitted.

#
# The following lines set up the Gaussian environment
#
module load gaussian
#
# Move to the directory where the job was submitted
#
cd $TMPDIR
cp -p /users/appl/srb/workshops/compchem/gaussian/glucose.com .
#
# Run Gaussian
#
g16 < glucose.com
ls -al
#
# Now, copy data (or move) back once the simulation has completed
#
cp -p glucose.log glucose.chk $PBS_O_WORKDIR
