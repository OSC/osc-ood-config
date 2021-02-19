#!/bin/bash

ONDEMAND_USERNAME="$1"
if [ "x${ONDEMAND_USERNAME}" = "x" ]; then
  echo "Must specify username"
  exit 1
fi

TMPFILE=$(mktemp "/tmp/k8-ondemand-bootstrap-${ONDEMAND_USERNAME}.XXXXXX")
NAMESPACE="user-${ONDEMAND_USERNAME}"

cat > "$TMPFILE" <<EOF
---
apiVersion: v1
kind: Namespace
metadata:
  name: "$NAMESPACE"
  labels:
    app.kubernetes.io/name: open-ondemand
---
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  namespace: $NAMESPACE
  name: deny-from-other-namespaces
spec:
  podSelector:
    matchLabels:
  ingress:
  - from:
    - podSelector: {}
    - ipBlock:
        cidr: 192.148.247.128/25
---
# give the service account the ood-initializer role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: "$NAMESPACE"
  name: "$ONDEMAND_USERNAME-ood-initializer"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: "ood-initializer"
subjects:
  - kind: ServiceAccount
    name: "default"
    namespace: "$NAMESPACE"
---
# give the user the ood-user role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: "$NAMESPACE"
  name: "$ONDEMAND_USERNAME-ood-user"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: "ood-user"
subjects:
  - kind: User
    name: "$ONDEMAND_USERNAME"
    namespace: "$NAMESPACE"
---
# allow job-pod-reaper to see this namespace
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: "$ONDEMAND_USERNAME-job-pod-reaper-rolebinding"
  namespace: "$NAMESPACE"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: job-pod-reaper
subjects:
- kind: ServiceAccount
  name: job-pod-reaper
  namespace: job-pod-reaper
EOF


export PATH=/usr/local/bin:/bin:$PATH
kubectl apply -f "$TMPFILE"

rm -f "$TMPFILE"