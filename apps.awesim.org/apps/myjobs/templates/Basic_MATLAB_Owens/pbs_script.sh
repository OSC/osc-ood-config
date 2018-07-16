#PBS -N matlab_example
#PBS -l walltime=00:10:00
#PBS -l nodes=1:ppn=28
#PBS -j oe

#   A Basic MATLAB Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/matlab

# load MATLAB module
module load matlab

# transfer MATLAB script file to TMPDIR
cd $PBS_O_WORKDIR
cp hello.m $TMPDIR
cd $TMPDIR

# run MATLAB script
matlab -nodisplay -nodesktop < hello.m
# end of example file
