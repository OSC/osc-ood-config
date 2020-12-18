#!/bin/bash

ONDEMAND_USERNAME="$1"
if [ "x${ONDEMAND_USERNAME}" = "x" ]; then
  echo "Must specify username"
  exit 1
fi

# This file has environment specific stuff like TOKEN_URL, CLIENT_SECRET,
# CLIENT_ID and K8S_USERNAME
# shellcheck disable=SC1091
source "/opt/osc/etc/ondemand-k8.env"

# we use pass ACCESS_TOKEN into the id-token arg. That's OK, it works and refreshes.
sudo -u "$ONDEMAND_USERNAME" kubectl config set-credentials "$K8S_USERNAME" \
   --auth-provider=oidc \
   --auth-provider-arg=idp-issuer-url="$TOKEN_URL" \
   --auth-provider-arg=client-id="$CLIENT_ID" \
   --auth-provider-arg=client-secret="$CLIENT_SECRET" \
   --auth-provider-arg=refresh-token="$OIDC_REFRESH_TOKEN" \
   --auth-provider-arg=id-token="$OIDC_ACCESS_TOKEN"
