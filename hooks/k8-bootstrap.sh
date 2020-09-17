#!/bin/bash

USERNAME="$1"
if [ "x${USERNAME}" = "x" ]; then
  echo "Must specify username"
  exit 1
fi

TMPFILE=$(mktemp /tmp/k8-ondemand-bootstrap-${USERNAME}.XXXXXX)
PASSWD=$(getent passwd $USERNAME)
USER_UID=$(echo "$PASSWD" | cut -d':' -f3)
USER_GID=$(echo "$PASSWD" | cut -d':' -f4)

cat > $TMPFILE <<EOF
---
apiVersion: v1
kind: Namespace
metadata:
  name: "$USERNAME"
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
  namespace: "$USERNAME"
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
  namespace: "$USERNAME"
  name: "$USERNAME-ood-initializer"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: "ood-initializer"
subjects:
  - kind: ServiceAccount
    name: "default"
    namespace: "$USERNAME"
---
# give the user the ood-user role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: "$USERNAME"
  name: "$USERNAME-ood-user"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: "ood-user"
subjects:
  - kind: User
    name: "$USERNAME"
    namespace: "$USERNAME"
---
# bind the users' pod security policy to the user
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: "$USERNAME-psp-rolebinding"
  namespace: "$USERNAME"
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: "$USERNAME-psp-role"
subjects:
- apiGroup: rbac.authorization.k8s.io
  kind: User
  name: "$USERNAME"
  namespace: "$USERNAME"
EOF


export PATH=/usr/local/bin:/bin:$PATH
kubectl apply -f $TMPFILE

rm -f $TMPFILE