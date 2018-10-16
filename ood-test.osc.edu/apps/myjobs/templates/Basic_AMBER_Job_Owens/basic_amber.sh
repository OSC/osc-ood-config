#PBS -N ondemand/sys/myjobs/basic_amber
#PBS -j oe
#PBS -l walltime=0:10:00
#PBS -l nodes=2:ppn=12
#
# The following lines set up the Amber environment
# Further Details at
#	https://www.osc.edu/resources/available_software/software_list/amber
#
set echo
# emit verbose details on the job's queuing.
qstat -f $PBS_JOBID
module load intel/17.0.7  mvapich2/2.3 amber/18
echo "AMBERHOME=$AMBERHOME"
#
# PBS_O_WORKDIR refers to the directory from which the job was submitted.
echo "PBS_O_WORKDIR=$PBS_O_WORKDIR"
cd $TMPDIR
#
# The file names below may need to be changed
set MDIN=mdin
set MDOUT=mdout
set MDINFO=mdinfo
set PRMTOP=prmtop
set INPCRD=inpcrd.equil
set REFC=refc
set MDCRD=mdcrd
set MDVEL=mdvel
set MDEN=mden
set RESTRT=restrt
cp -p /users/appl/srb/workshops/compchem/amber/$MDIN .
cp -p /users/appl/srb/workshops/compchem/amber/$PRMTOP .
cp -p /users/appl/srb/workshops/compchem/amber/$INPCRD .
cp -p /users/appl/srb/workshops/compchem/amber/$REFC .
#cp -p $PBS_O_WORKDIR/$RESTRT .
#
# Some jobs may require the -O option on the Amber command lines below
#mpiexec $AMBERHOME/bin/sander.MPI -i $MDIN -o stdout -inf $MDINFO -p $PRMTOP -c $INPCRD -ref $REFC -x $MDCRD -v $MDVEL -e $MDEN -r $RESTRT
# Some jobs may use pmemd which consumes less walltime than sander.
mpiexec $AMBERHOME/bin/pmemd.MPI -i $MDIN -o $MDOUT -inf $MDINFO -p $PRMTOP -c $INPCRD -ref $REFC -x $MDCRD -v $MDVEL -e $MDEN -r $RESTRT
ls -al
cp -p $MDOUT $MDINFO $MDCRD $MDVEL $MDEN $RESTRT $PBS_O_WORKDIR
cat $MDOUT