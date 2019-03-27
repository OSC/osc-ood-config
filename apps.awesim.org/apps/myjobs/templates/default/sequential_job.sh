#PBS -N ondemand/sys/myjobs/default
#PBS -l walltime=00:10:00
#PBS -l nodes=1:ppn=1
#PBS -j oe
#
# Move to the directory where the job was submitted
#
cd $PBS_O_WORKDIR
cp myscript.sh $TMPDIR
cd $TMPDIR
#
# Run script
#
sh myscript.sh > my_results
#
# Now, copy data (or move) back once the simulation has completed
#
cp my_results $PBS_O_WORKDIR