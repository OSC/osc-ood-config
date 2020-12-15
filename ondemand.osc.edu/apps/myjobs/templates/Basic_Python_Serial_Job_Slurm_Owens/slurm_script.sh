#!/bin/bash
#SBATCH --job-name=ondemand/sys/myjobs/basic_python_serial
#SBATCH --time=0:10:00
#SBATCH -N 1 -n 1
qstat -f $SLURM_JOB_ID

#   A Basic Python Serial Job for the OSC Owens cluster
#   https://www.osc.edu/resources/available_software/software_list/python

#
# The following lines set up the Python environment
#
module load python
#
# Move to the directory where the job was submitted from
# You could also 'cd' directly to your working directory
cd $SLURM_SUBMIT_DIR
#
# Run Python
#
python hello.py
