#!/bin/bash

for arg in "$@"
do
  case $arg in
    --user)
    ONDEMAND_USERNAME=$2
    shift
    shift
    ;;
esac
done

if [ "x${ONDEMAND_USERNAME}" = "x" ]; then
  echo "Must specify username"
  exit 1
fi

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

if groups "$ONDEMAND_USERNAME" | grep -q "\boscall\b"; then
  /bin/bash "$BASEDIR/k8s-bootstrap.sh" "$ONDEMAND_USERNAME"
  /bin/bash "$BASEDIR/set-k8s-creds.sh" "$ONDEMAND_USERNAME"
fi
