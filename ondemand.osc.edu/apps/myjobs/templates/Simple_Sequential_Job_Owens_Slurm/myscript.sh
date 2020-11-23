#!/bin/bash

cat message.in > message.out
echo "The following is from myscript.sh" >> message.out

scontrol show job $SLURM_JOBID >> message.out