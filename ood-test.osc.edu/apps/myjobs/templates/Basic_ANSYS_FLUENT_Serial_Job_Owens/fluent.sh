#PBS -N ondemand/sys/myjobs/basic_ansys_fluent_serial
#PBS -l walltime=00:30:00
#PBS -l nodes=1:ppn=1
#PBS -l software=ansys+1
#PBS -j oe

# A basic FLUENT Serial Job
# Further details available at:
# 	https://www.osc.edu/resources/available_software/software_list/ansys/fluent

#
# The following lines set up the FLUENT environment
#
module load ansys
#
# Move to the directory where the job was submitted from
# You could also 'cd' directly to your working directory
cd $PBS_O_WORKDIR
#
# Copy files to $TMPDIR and move there to execute the program
#
cp /users/oscgen/xwang/Fluent/Demo_tmi_fluent/test.* run.input $TMPDIR
cd $TMPDIR
#
# Run fluent
fluent 3d -g < run.input
#
# Where the file 'run.input' contains the commands you would normally
# type in at the Fluent command prompt.
# Finally, copy files back to your home directory
cp *   $PBS_O_WORKDIR
