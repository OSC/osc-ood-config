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

if [ "${ONDEMAND_USERNAME}" = "" ]; then
  echo "Must specify username"
  exit 1
fi

HOOKSDIR="/opt/ood/hooks"
HOOKENV="/etc/ood/config/hook.env"

/bin/bash "$HOOKSDIR/k8s-bootstrap/k8s-bootstrap-ondemand.sh" "$ONDEMAND_USERNAME" "$HOOKENV"
/bin/bash "$HOOKSDIR/k8s-bootstrap/set-k8s-creds.sh" "$ONDEMAND_USERNAME" "$HOOKENV"
