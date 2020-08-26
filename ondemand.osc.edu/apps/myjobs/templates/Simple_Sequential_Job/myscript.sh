#!/bin/bash

cat message.in > message.out
echo "The following is from myscript.sh" >> message.out

qstat -f $PBS_JOBID >> message.out