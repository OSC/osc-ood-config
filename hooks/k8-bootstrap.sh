#!/bin/bash

USERNAME="$1"
if [ "x${USERNAME}" = "x" ]; then
  echo "Must specify username"
  exit 1
fi

TMPFILE=$(mktemp /tmp/k8-ondemand-bootstrap-${USERNAME}.XXXXXX)
PASSWD=$(getent passwd $USERNAME)
if ! [[ "$PASSWD" =~ "${USERNAME}:"* ]]; then
  echo "level=error msg=\"Unable to perform lookup of user\" user=$USERNAME"
  exit 1
fi
USER_UID=$(echo "$PASSWD" | cut -d':' -f3)
USER_GID=$(echo "$PASSWD" | cut -d':' -f4)
NAMESPACE="user-${USERNAME}"

cat > $TMPFILE <<EOF
---
apiVersion: v1
kind: Namespace
metadata:
  name: "$NAMESPACE"
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
# the pod security policy such that you can only run pods as a single uid/gid pair
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: "$USERNAME-psp"
  annotations:
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: 'docker/default,runtime/default'
    apparmor.security.beta.kubernetes.io/allowedProfileNames: 'runtime/default'
    seccomp.security.alpha.kubernetes.io/defaultProfileName:  'runtime/default'
    apparmor.security.beta.kubernetes.io/defaultProfileName:  'runtime/default'
spec:
  # Required to prevent escalations to root.
  privileged: false
  allowPrivilegeEscalation: false
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    # Run as your own uid
    rule: 'MustRunAs'
    ranges:
    - min: $USER_UID
      max: $USER_UID
  runAsGroup:
    # Run as your own gid
    rule: 'MustRunAs'
    ranges:
    - min: $USER_GID
      max: $USER_GID
  seLinux:
    # This policy assumes the nodes are using AppArmor rather than SELinux.
    rule: 'RunAsAny'
  supplementalGroups:
    rule: 'MustRunAs'
    ranges:
    # Forbid adding the root group.
    - min: 1
      max: 65535
  fsGroup:
    rule: 'MustRunAs'
    ranges:
    # Forbid adding the root group.
    - min: 1
      max: 65535
  volumes:
  - '*'
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: "$USERNAME-psp-role"
  namespace: "$NAMESPACE"
rules:
- apiGroups: [ "extensions" ]
  resources: [ "podsecuritypolicies" ]
  resourceNames: [ "$USERNAME-psp" ]
  verbs: [ "use" ]
---
# give the service account the ood-initializer role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: "$NAMESPACE"
  name: "$USERNAME-ood-initializer"
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
  name: "$USERNAME-ood-user"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: "ood-user"
subjects:
  - kind: User
    name: "$USERNAME"
    namespace: "$NAMESPACE"
---
# bind the users' pod security policy to the user
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: "$USERNAME-psp-rolebinding"
  namespace: "$NAMESPACE"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: "$USERNAME-psp-role"
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: "$USERNAME"
  namespace: "$NAMESPACE"
EOF


export PATH=/usr/local/bin:/bin:$PATH
kubectl apply -f $TMPFILE

rm -f $TMPFILE