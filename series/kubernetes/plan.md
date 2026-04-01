# Kubernetes Series — Full Coverage Plan

Based on: https://kubernetes.io/docs/concepts/ (sitemap crawled 2026-04-01)

**Length estimates** based on typical episode pace (~150 words/min narration, 30fps render):
- Simple concept: ~90s
- Medium concept: ~110s  
- Complex concept: ~130s

---

## Existing Episodes (11 published)

| Ep | Title | Docs Link | YouTube | Est. Length |
|----|-------|-----------|---------|-------------|
| 01 | What is Kubernetes | [overview](https://kubernetes.io/docs/concepts/overview/) | [youtu.be/oeZeViBO-34](https://youtu.be/oeZeViBO-34) | 72s |
| 02 | Cluster Components | [components](https://kubernetes.io/docs/concepts/overview/components/) | [youtu.be/jzHthuaaJDE](https://youtu.be/jzHthuaaJDE) | 68s |
| 03 | Pods | [pods](https://kubernetes.io/docs/concepts/workloads/pods/) | [youtu.be/3gP1jeLRG-s](https://youtu.be/3gP1jeLRG-s) | 74s |
| 04 | Deployments | [deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) | [youtu.be/RF4ntSQ_pgA](https://youtu.be/RF4ntSQ_pgA) | 69s |
| 05 | Services | [service](https://kubernetes.io/docs/concepts/services-networking/service/) | [youtu.be/wnU00LpKbfI](https://youtu.be/wnU00LpKbfI) | 70s |
| 06 | ConfigMaps | [configmap](https://kubernetes.io/docs/concepts/configuration/configmap/) | [youtu.be/jxyX_3lViyU](https://youtu.be/jxyX_3lViyU) | 65s |
| 07 | Secrets | [secret](https://kubernetes.io/docs/concepts/configuration/secret/) | [youtu.be/iKiU2DXgrRE](https://youtu.be/iKiU2DXgrRE) | 69s |
| 08 | Persistent Volumes | [persistent-volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) | [youtu.be/NQ06EXGPxXg](https://youtu.be/NQ06EXGPxXg) | 71s |
| 09 | Ingress | [ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) | [youtu.be/HRCcIP-IMHM](https://youtu.be/HRCcIP-IMHM) | 68s |
| 10 | StatefulSets | [statefulset](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) | [youtu.be/vO6UTF7e0y8](https://youtu.be/vO6UTF7e0y8) | 66s |
| 11 | DaemonSets & Jobs | [daemonset](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/) + [job](https://kubernetes.io/docs/concepts/workloads/controllers/job/) | [youtu.be/c0fmmkcb0BU](https://youtu.be/c0fmmkcb0BU) | 70s |

---

## Planned Episodes

### Section 1: Overview

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 12 | The Kubernetes API | [kubernetes-api](https://kubernetes.io/docs/concepts/overview/kubernetes-api/) | REST API, API groups, versioning (alpha/beta/stable), `kubectl` under the hood | ~90s |
| 13 | Labels & Selectors | [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) + [field-selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/) | Label syntax, equality vs set-based selectors, annotations vs labels | ~90s |
| 14 | Namespaces | [namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/) + [names](https://kubernetes.io/docs/concepts/overview/working-with-objects/names/) | Namespace isolation, names, UIDs, resource scoping | ~85s |
| 15 | Finalizers & Owners | [finalizers](https://kubernetes.io/docs/concepts/overview/working-with-objects/finalizers/) + [owners-dependents](https://kubernetes.io/docs/concepts/overview/working-with-objects/owners-dependents/) | Deletion protection, owner references, cascading delete | ~85s |

### Section 2: Architecture

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 16 | Nodes | [nodes](https://kubernetes.io/docs/concepts/architecture/nodes/) | Node status, conditions, heartbeat, node controller, capacity | ~95s |
| 17 | Controllers | [controller](https://kubernetes.io/docs/concepts/architecture/controller/) | Control loop, reconciliation, desired vs actual state, watch/list | ~85s |
| 18 | Garbage Collection | [garbage-collection](https://kubernetes.io/docs/concepts/architecture/garbage-collection/) | Owner references, foreground vs background cascading deletion | ~85s |
| 19 | Leases | [leases](https://kubernetes.io/docs/concepts/architecture/leases/) | Distributed lock, leader election, node heartbeat mechanism | ~80s |
| 20 | Cloud Controller | [cloud-controller](https://kubernetes.io/docs/concepts/architecture/cloud-controller/) | Cloud-provider integration, node/route/service controllers | ~85s |
| 21 | cgroups in Kubernetes | [cgroups](https://kubernetes.io/docs/concepts/architecture/cgroups/) | cgroup v1 vs v2, resource isolation, Linux fundamentals | ~80s |

### Section 3: Containers

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 22 | Container Images | [images](https://kubernetes.io/docs/concepts/containers/images/) | Image naming, pull policy (Always/IfNotPresent/Never), private registries, imagePullSecrets | ~90s |
| 23 | Container Lifecycle | [container-lifecycle-hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/) + [container-environment](https://kubernetes.io/docs/concepts/containers/container-environment/) | PostStart/PreStop hooks, env vars available, downward API intro | ~95s |
| 24 | Runtime Classes | [runtime-class](https://kubernetes.io/docs/concepts/containers/runtime-class/) | CRI, containerd, gVisor, per-pod runtime selection | ~80s |
| 25 | Container Runtime Interface | [cri](https://kubernetes.io/docs/concepts/containers/cri/) | CRI spec, how kubelet talks to container runtimes, pluggable runtimes | ~80s |

### Section 4: Workloads — Pods

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 26 | Pod Lifecycle | [pod-lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/) | Phases (Pending/Running/Succeeded/Failed/Unknown), conditions, restart policy | ~100s |
| 27 | Init Containers | [init-containers](https://kubernetes.io/docs/concepts/workloads/pods/init-containers/) | Sequential init, blocking main containers, use cases (DB wait, config) | ~90s |
| 28 | Sidecar Containers | [sidecar-containers](https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/) | Restartable init containers as sidecars, logging/proxy pattern | ~85s |
| 29 | Pod Disruption Budgets | [disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/) | Voluntary vs involuntary disruption, PDB spec, `kubectl drain` safety | ~90s |
| 30 | Ephemeral Containers | [ephemeral-containers](https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/) | Debug containers, `kubectl debug`, no restart policy | ~80s |
| 31 | Downward API | [downward-api](https://kubernetes.io/docs/concepts/workloads/pods/downward-api/) | Exposing pod name/namespace/IP/labels to container via env or volume | ~85s |

### Section 4: Workloads — Controllers

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 32 | ReplicaSets | [replicaset](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) | Selector + template, when to use directly vs via Deployment | ~80s |
| 33 | CronJobs | [cron-jobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) | Cron syntax, concurrencyPolicy, successfulJobsHistoryLimit | ~90s |
| 34 | HPA (Autoscaling) | [horizontal-pod-autoscale](https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/) | Scale on CPU/memory/custom metrics, targetUtilization | ~95s |

### Section 5: Services & Networking

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 35 | DNS for Pods & Services | [dns-pod-service](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/) | CoreDNS, FQDN format, search domains, pod DNS policy | ~90s |
| 36 | Network Policies | [network-policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) | Ingress/egress rules, pod/namespace selectors, default deny | ~100s |
| 37 | Ingress Controllers | [ingress-controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/) | nginx/traefik/cloud options, IngressClass, choosing a controller | ~90s |
| 38 | Gateway API | [gateway](https://kubernetes.io/docs/concepts/services-networking/gateway/) | HTTPRoute, GatewayClass, TCPRoute, successor to Ingress | ~95s |
| 39 | EndpointSlices | [endpoint-slices](https://kubernetes.io/docs/concepts/services-networking/endpoint-slices/) | Scalable endpoint tracking, replacing Endpoints object, topology | ~80s |

### Section 6: Storage

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 40 | Volumes | [volumes](https://kubernetes.io/docs/concepts/storage/volumes/) | emptyDir, hostPath, configMap/secret as volumes, volume types overview | ~100s |
| 41 | Storage Classes | [storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes/) | Provisioner, reclaim policy, volumeBindingMode, WaitForFirstConsumer | ~95s |
| 42 | Dynamic Provisioning | [dynamic-provisioning](https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/) | StorageClass + PVC → auto PV, cloud provisioners | ~85s |
| 43 | Ephemeral Volumes | [ephemeral-volumes](https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/) | Generic ephemeral, CSI ephemeral, emptyDir deep dive, lifecycle | ~90s |
| 44 | Volume Snapshots | [volume-snapshots](https://kubernetes.io/docs/concepts/storage/volume-snapshots/) + [volume-snapshot-classes](https://kubernetes.io/docs/concepts/storage/volume-snapshot-classes/) | VolumeSnapshot, VolumeSnapshotContent, restore to PVC | ~90s |

### Section 7: Configuration

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 45 | Resource Requests & Limits | [manage-resources-containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) | CPU/memory requests vs limits, QoS classes (Guaranteed/Burstable/BestEffort) | ~105s |
| 46 | Liveness & Readiness Probes | [liveness-readiness-startup-probes](https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/) | HTTP/exec/TCP probes, startup probe, failure threshold, initialDelaySeconds | ~105s |

### Section 8: Scheduling & Eviction

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 47 | The Scheduler | [kube-scheduler](https://kubernetes.io/docs/concepts/scheduling-eviction/kube-scheduler/) | Filtering, scoring, binding phases, scheduler profiles | ~90s |
| 48 | Assigning Pods to Nodes | [assign-pod-node](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/) | nodeSelector, nodeAffinity (required/preferred), podAffinity/Anti | ~110s |
| 49 | Taints & Tolerations | [taint-and-toleration](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) | Taint effects (NoSchedule/PreferNoSchedule/NoExecute), toleration syntax, use cases | ~95s |
| 50 | Pod Priority & Preemption | [pod-priority-preemption](https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/) | PriorityClass, preemption, impact on scheduler decisions | ~90s |
| 51 | Node Pressure Eviction | [node-pressure-eviction](https://kubernetes.io/docs/concepts/scheduling-eviction/node-pressure-eviction/) | Memory/disk pressure signals, eviction thresholds, QoS order | ~95s |

### Section 9: Security

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 52 | RBAC | [controlling-access](https://kubernetes.io/docs/concepts/security/controlling-access/) | AuthN vs AuthZ, Roles, ClusterRoles, RoleBindings, subjects | ~110s |
| 53 | Service Accounts | [service-accounts](https://kubernetes.io/docs/concepts/security/service-accounts/) | Default SA, token automounting, IRSA pattern, projected tokens | ~95s |
| 54 | Pod Security Standards | [pod-security-standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) + [pod-security-admission](https://kubernetes.io/docs/concepts/security/pod-security-admission/) | Privileged/Baseline/Restricted profiles, PSA labels, warn/audit/enforce | ~105s |
| 55 | Network Security | [secrets-good-practices](https://kubernetes.io/docs/concepts/security/secrets-good-practices/) + [rbac-good-practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/) | Secrets hygiene, RBAC least privilege, defense in depth | ~95s |
| 56 | Multi-tenancy | [multi-tenancy](https://kubernetes.io/docs/concepts/security/multi-tenancy/) | Namespace isolation, soft vs hard tenancy, cluster vs namespace admin | ~90s |

### Section 10: Policies

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 57 | Resource Quotas | [resource-quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) | Namespace-scoped limits, compute quotas, object count quotas | ~90s |
| 58 | LimitRange | [limit-range](https://kubernetes.io/docs/concepts/policy/limit-range/) | Default requests/limits, min/max per container, ratio enforcement | ~85s |

### Section 11: Cluster Administration

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 59 | Networking Overview | [networking](https://kubernetes.io/docs/concepts/cluster-administration/networking/) | CNI, the Kubernetes network model, pod-to-pod routing requirements | ~95s |
| 60 | Logging Architecture | [logging](https://kubernetes.io/docs/concepts/cluster-administration/logging/) | Node-level, sidecar, cluster-level logging patterns | ~90s |
| 61 | Cluster Autoscaling | [node-autoscaling](https://kubernetes.io/docs/concepts/cluster-administration/node-autoscaling/) | Cluster Autoscaler, scale-up/down triggers, node groups | ~85s |

---

## Summary

| Section | Episodes | Approx. Total Time |
|---------|----------|--------------------|
| Overview (existing + new) | 4 | ~6 min |
| Architecture | 6 | ~9 min |
| Containers | 4 | ~6 min |
| Workloads — Pods | 7 | ~10 min |
| Workloads — Controllers | 5 (3 new) | ~8 min |
| Services & Networking | 7 (2 existing) | ~10 min |
| Storage | 6 (1 existing) | ~9 min |
| Configuration | 4 (2 existing) | ~7 min |
| Scheduling & Eviction | 5 | ~8 min |
| Security | 5 | ~8 min |
| Policies | 2 | ~3 min |
| Cluster Admin | 3 | ~4.5 min |
| **Total** | **61** | **~88 min** |

**50 new episodes** needed. At 1/day: ~2 months to full K8s coverage.

## Recommended Priority Order (next 10)

1. **Pod Lifecycle** (#26) — foundational, referenced everywhere
2. **Resource Requests & Limits** (#45) — every practitioner needs this
3. **Liveness & Readiness Probes** (#46) — pairs with resources
4. **Taints & Tolerations** (#49) — common in real clusters
5. **RBAC** (#52) — essential for any real cluster
6. **Labels & Selectors** (#13) — foundational but skipped
7. **Namespaces** (#14) — small, high-value
8. **CronJobs** (#33) — natural follow-on from Jobs
9. **Network Policies** (#36) — high security value
10. **Storage Classes** (#41) — natural follow-on from PV
