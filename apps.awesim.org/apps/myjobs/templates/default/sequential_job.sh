#PBS -N my_job
#PBS -l walltime=00:10:00
#PBS -l nodes=1:ppn=1
#PBS -j oe

cd $PBS_O_WORKDIR
./myscript.sh > output.txt

