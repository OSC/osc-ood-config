#PBS -N ondemand/sys/myjobs/basic_python_serial
#PBS -j oe
#PBS -l walltime=0:10:00
#PBS -l nodes=1:ppn=28
qstat -f $PBS_JOBID
export

#   A Basic Python Serial Job for the OSC Owens Cluster
#   https://www.osc.edu/resources/available_software/software_list/python

#
# The following lines set up the Python environment
#
module load python
#
# Move to the directory where the job was submitted from
# You could also 'cd' directly to your working directory
cd $PBS_O_WORKDIR
#
# Run Python
#
python hello.py