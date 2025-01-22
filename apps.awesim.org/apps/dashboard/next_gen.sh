#!/bin/bash

CMD=$(basename "${BASH_SOURCE[0]}")
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [[ "$CMD" == "squeue" ]]; then
  ARGS="-p nextgen,nextgen-cpuonly,nextgen-gpu"
else
  ARGS="-p nextgen"
fi

"$CMD" "$ARGS" "$@"