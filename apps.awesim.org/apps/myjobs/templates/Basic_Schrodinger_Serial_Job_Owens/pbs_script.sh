#PBS -N ondemand/sys/myjobs/basic_schrodinger_serial
#PBS -j oe
#PBS -l walltime=0:10:00
#PBS -l nodes=1:ppn=28
#PBS -l software=glide+1
#PBS -S /bin/sh
qstat -f $PBS_JOBID

#   A Basic Schrodinger Serial Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/schrodinger

#
# The following lines set up the Schrodinger environment
#
module load schrodinger
#
# Move to the directory where the job was submitted
# More information about pbsdcp: https://www.osc.edu/~troy/pbstools/man/pbsdcp
#
cd $PBS_O_WORKDIR
pbsdcp -p * $TMPDIR
cd $TMPDIR
#
# Run schrodinger, Schrodinger scripts source: https://www.bi.cs.titech.ac.jp/mga_glide/
#
$SCHRODINGER/run xglide_mga.py inputfile.inp
ls -l
#
# Now, copy data (or move) back once the simulation has completed
#
pbsdcp -p '*' $PBS_O_WORKDIR
