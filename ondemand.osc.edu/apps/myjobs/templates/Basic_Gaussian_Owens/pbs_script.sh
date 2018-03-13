#PBS -N GaussianJob
#PBS -l nodes=1:ppn=28

#  A Basic Gaussian Job for the OSC Owens Cluster
#  https://www.osc.edu/supercomputing/software/gaussian

# PBS_O_WORKDIR refers to the directory from which the job was submitted.
 
cd $PBS_O_WORKDIR

cp input.com $TMPDIR

# Use TMPDIR for best performance.
cd $TMPDIR

module load gaussian

g09 < input.com

cp -p input.log *.chk $PBS_O_WORKDIR
