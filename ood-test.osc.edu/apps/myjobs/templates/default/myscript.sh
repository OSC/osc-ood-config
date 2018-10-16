#!/bin/bash
qstat -f $PBS_JOBID
# do something
echo "I'm echoing to stdout"