# AMBER 16 Example Batch Script for Owens
#
#PBS -N jac9999cuda.owens
#PBS -j oe
#PBS -m ae
#PBS -M srb@osc.edu
#PBS -l walltime=0:10:00
#PBS -l nodes=1:ppn=1:gpus=1
#PBS -S /bin/csh
set echo
# emit verbose details on the job's queuing.
qstat -f $PBS_JOBID
module load amber/16
module load cuda/8.0.44
module list
echo "AMBERHOME=$AMBERHOME"
#
# PBS_O_WORKDIR refers to the directory from which the job was submitted.
echo "PBS_O_WORKDIR=$PBS_O_WORKDIR"
cd $TMPDIR
#
# The file names below may need to be changed
set MDIN=mdin9999
set MDOUT=mdout9999
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
cp -p /users/appl/srb/workshops/compchem/amber/$RESTRT .
cp -p /users/appl/srb/workshops/compchem/amber/$MDOUT .
cp -p /users/appl/srb/workshops/compchem/amber/$MDINFO .
cp -p /users/appl/srb/workshops/compchem/amber/$MDCRD .
cp -p /users/appl/srb/workshops/compchem/amber/$MDVEL .
cp -p /users/appl/srb/workshops/compchem/amber/$MDEN .
#
# pmemd.cuda uses this variable to select an available gpu;
# this is not necessary on Owens which has only 1 gpu per node
#setenv CUDA_VISIBLE_DEVICES `cat $PBS_GPUFILE|sed 's/.*gpu//'|paste -s -d,`
#
# These commands report the status of the GPUs; this is sometimes useful
# for detecting if other batch jobs are using the GPUs properly.
nvidia-smi
/usr/local/cuda/5.0.35/1_Utilities/deviceQuery/deviceQuery | grep -i 'device[ 0-9]*[:(]'
#
# Some jobs may require the -O option on the Amber command lines below
pmemd.cuda -i $MDIN -o $MDOUT -inf $MDINFO -p $PRMTOP -c $INPCRD -ref $REFC -x $MDCRD -v $MDVEL -e $MDEN -r $RESTRT
ls -al
cp -p $MDOUT $MDINFO $MDCRD $MDVEL $MDEN $RESTRT $PBS_O_WORKDIR
cat $MDOUT
