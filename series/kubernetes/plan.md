# Kubernetes Series — Full Coverage Plan

Based on: https://kubernetes.io/docs/concepts/ (sitemap crawled 2026-04-01)

## Existing Episodes (11 published)

| Ep | Title | Docs URL | Status |
|----|-------|----------|--------|
| 01 | What is Kubernetes | /docs/concepts/overview/ | ✅ Published |
| 02 | Cluster Components | /docs/concepts/overview/components/ | ✅ Published |
| 03 | Pods | /docs/concepts/workloads/pods/ | ✅ Published |
| 04 | Deployments | /docs/concepts/workloads/controllers/deployment/ | ✅ Published |
| 05 | Services | /docs/concepts/services-networking/service/ | ✅ Published |
| 06 | ConfigMaps | /docs/concepts/configuration/configmap/ | ✅ Published |
| 07 | Secrets | /docs/concepts/configuration/secret/ | ✅ Published |
| 08 | Persistent Volumes | /docs/concepts/storage/persistent-volumes/ | ✅ Published |
| 09 | Ingress | /docs/concepts/services-networking/ingress/ | ✅ Published |
| 10 | StatefulSets | /docs/concepts/workloads/controllers/statefulset/ | ✅ Published |
| 11 | DaemonSets & Jobs | /docs/concepts/workloads/controllers/daemonset/ + /job/ | ✅ Published |

---

## Full Coverage Plan

### Section 1: Overview (4 episodes — 1 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| 01 | What is Kubernetes | /overview/ | What K8s is, what it does, what it's not. Containers → VMs → K8s history | ✅ Done |
| NEW | The Kubernetes API | /overview/kubernetes-api/ | REST API, API groups, versioning (alpha/beta/stable), how kubectl talks to the API | 🔲 Planned |
| 02 | Cluster Components | /overview/components/ | Control plane (API server, etcd, scheduler, controller-manager) + node components | ✅ Done |
| NEW | Working with Objects | /overview/working-with-objects/ | Spec vs Status, names & UIDs, namespaces, labels, annotations, selectors | 🔲 Planned |

Sub-pages of Working with Objects (can merge into one or split):
- labels, annotations, field-selectors, names, namespaces, finalizers, owners-dependents, common-labels

> **Decision:** Merge into 2 episodes: "Labels & Selectors" + "Namespaces & Object Metadata"

| NEW | Labels & Selectors | /working-with-objects/labels/ + /field-selectors/ | Label syntax, equality vs set-based selectors, annotation vs label | 🔲 Planned |
| NEW | Namespaces | /working-with-objects/namespaces/ + /names/ | Namespace isolation, names/UIDs, object references | 🔲 Planned |

---

### Section 2: Architecture (6 episodes — 0 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| NEW | Nodes | /architecture/nodes/ | Node status, heartbeat, node controller, taints | 🔲 Planned |
| NEW | Controllers | /architecture/controller/ | Control loop, reconciliation, desired vs actual state | 🔲 Planned |
| NEW | Garbage Collection | /architecture/garbage-collection/ | Owner references, cascading deletion, foreground vs background | 🔲 Planned |
| NEW | Leases | /architecture/leases/ | Distributed coordination, leader election, node heartbeat mechanism | 🔲 Planned |
| NEW | Cloud Controller | /architecture/cloud-controller/ | Cloud-provider integration, node/route/service controllers | 🔲 Planned |
| NEW | cgroups | /architecture/cgroups/ | cgroup v1 vs v2, resource isolation, Linux fundamentals | 🔲 Planned |

---

### Section 3: Containers (4 episodes — 0 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| NEW | Container Images | /containers/images/ | Image naming, pull policy, private registries, imagePullSecrets | 🔲 Planned |
| NEW | Container Lifecycle | /containers/container-lifecycle-hooks/ + /container-environment/ | PostStart/PreStop hooks, env vars, downward API | 🔲 Planned |
| NEW | Runtime Classes | /containers/runtime-class/ | CRI, containerd, RuntimeClass, per-pod runtime selection | 🔲 Planned |
| NEW | Container Runtime Interface | /containers/cri/ | CRI spec, how kubelet talks to container runtimes | 🔲 Planned |

---

### Section 4: Workloads (10 episodes — 5 existing)

#### Pods sub-pages (need coverage)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| 03 | Pods | /workloads/pods/ | Pod spec, containers, scheduling unit | ✅ Done |
| NEW | Pod Lifecycle | /workloads/pods/pod-lifecycle/ | Phases (Pending/Running/Succeeded/Failed), conditions, container states | 🔲 Planned |
| NEW | Init Containers | /workloads/pods/init-containers/ | Sequential init, use cases (DB wait, config setup) | 🔲 Planned |
| NEW | Sidecar Containers | /workloads/pods/sidecar-containers/ | Restartable init containers, logging/proxy sidecars | 🔲 Planned |
| NEW | Pod Disruption Budgets | /workloads/pods/disruptions/ | PDB, voluntary vs involuntary disruptions, drain operations | 🔲 Planned |
| NEW | Ephemeral Containers | /workloads/pods/ephemeral-containers/ | Debug containers, kubectl debug | 🔲 Planned |
| NEW | Downward API | /workloads/pods/downward-api/ | Exposing pod metadata to containers (env vars + volume files) | 🔲 Planned |

#### Controllers (need coverage)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| 04 | Deployments | /controllers/deployment/ | ReplicaSet management, rolling updates, rollback | ✅ Done |
| NEW | ReplicaSets | /controllers/replicaset/ | Direct ReplicaSet use (rare), relationship to Deployments | 🔲 Planned |
| 10 | StatefulSets | /controllers/statefulset/ | Stable identity, ordered deploy/scale, persistent storage | ✅ Done |
| 11 | DaemonSets | /controllers/daemonset/ | One pod per node, node selector, tolerations | ✅ Done |
| 11 | Jobs | /controllers/job/ | Run-to-completion, parallelism, completions | ✅ Done (combined) |
| NEW | CronJobs | /controllers/cron-jobs/ | Scheduled jobs, cron syntax, concurrency policy | 🔲 Planned |
| NEW | Autoscaling | /workloads/autoscaling/ + /horizontal-pod-autoscale/ | HPA, VPA overview, metrics | 🔲 Planned |

---

### Section 5: Services & Networking (7 episodes — 2 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| 05 | Services | /services-networking/service/ | ClusterIP, NodePort, LoadBalancer, ExternalName, kube-proxy | ✅ Done |
| 09 | Ingress | /services-networking/ingress/ | Ingress resources, controllers, rules, TLS | ✅ Done |
| NEW | DNS for Pods & Services | /services-networking/dns-pod-service/ | CoreDNS, FQDN, search domains, pod DNS | 🔲 Planned |
| NEW | Network Policies | /services-networking/network-policies/ | Ingress/egress rules, pod selectors, namespace isolation | 🔲 Planned |
| NEW | Ingress Controllers | /services-networking/ingress-controllers/ | nginx, traefik, cloud options, choosing a controller | 🔲 Planned |
| NEW | Gateway API | /services-networking/gateway/ | HTTPRoute, GatewayClass, successor to Ingress | 🔲 Planned |
| NEW | EndpointSlices | /services-networking/endpoint-slices/ | Scalable endpoint tracking, replacing Endpoints | 🔲 Planned |

---

### Section 6: Storage (6 episodes — 1 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| 08 | Persistent Volumes | /storage/persistent-volumes/ | PV/PVC lifecycle, access modes, reclaim policy | ✅ Done |
| NEW | Volumes | /storage/volumes/ | emptyDir, hostPath, nfs, configMap/secret as volumes | 🔲 Planned |
| NEW | Storage Classes | /storage/storage-classes/ | Dynamic provisioning, provisioner, reclaim policy | 🔲 Planned |
| NEW | Ephemeral Volumes | /storage/ephemeral-volumes/ | Generic ephemeral, CSI ephemeral, emptyDir deep dive | 🔲 Planned |
| NEW | Volume Snapshots | /storage/volume-snapshots/ + /volume-snapshot-classes/ | Snapshot API, VolumeSnapshotContent | 🔲 Planned |
| NEW | Dynamic Provisioning | /storage/dynamic-provisioning/ | StorageClass, auto-creating PVs, cloud provisioners | 🔲 Planned |

---

### Section 7: Configuration (3 episodes — 2 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| 06 | ConfigMaps | /configuration/configmap/ | ConfigMap vs Secret, env injection, volume mount | ✅ Done |
| 07 | Secrets | /configuration/secret/ | Types, opaque/TLS/docker, encryption at rest | ✅ Done |
| NEW | Resource Management | /configuration/manage-resources-containers/ | requests vs limits, CPU/memory, LimitRange, QoS classes | 🔲 Planned |
| NEW | Liveness & Readiness Probes | /configuration/liveness-readiness-startup-probes/ | HTTP/exec/TCP probes, startup probes, failure thresholds | 🔲 Planned |

---

### Section 8: Scheduling & Eviction (5 episodes — 0 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| NEW | The Scheduler | /scheduling-eviction/kube-scheduler/ | Filtering, scoring, binding, scheduler profiles | 🔲 Planned |
| NEW | Assigning Pods to Nodes | /scheduling-eviction/assign-pod-node/ | nodeSelector, nodeAffinity, podAffinity, topologySpreadConstraints | 🔲 Planned |
| NEW | Taints & Tolerations | /scheduling-eviction/taint-and-toleration/ | Taint effects (NoSchedule/NoExecute), toleration syntax | 🔲 Planned |
| NEW | Pod Priority & Preemption | /scheduling-eviction/pod-priority-preemption/ | PriorityClass, preemption, when to use | 🔲 Planned |
| NEW | Node Pressure Eviction | /scheduling-eviction/node-pressure-eviction/ | kubelet eviction, memory/disk pressure, eviction signals | 🔲 Planned |

---

### Section 9: Security (5 episodes — 0 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| NEW | RBAC | /security/controlling-access/ | AuthN vs AuthZ, RBAC, Roles, ClusterRoles, Bindings | 🔲 Planned |
| NEW | Service Accounts | /security/service-accounts/ | Default SA, token mounting, IRSA pattern | 🔲 Planned |
| NEW | Pod Security Standards | /security/pod-security-standards/ + /pod-security-admission/ | Privileged/Baseline/Restricted, PSA admission controller | 🔲 Planned |
| NEW | Network Security | /security/secrets-good-practices/ + RBAC good practices | Defense in depth, secrets hygiene | 🔲 Planned |
| NEW | Multi-tenancy | /security/multi-tenancy/ | Namespace isolation, soft vs hard tenancy | 🔲 Planned |

---

### Section 10: Policies (2 episodes — 0 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| NEW | Resource Quotas | /policy/resource-quotas/ | Namespace-scoped limits, compute/object quotas | 🔲 Planned |
| NEW | LimitRange | /policy/limit-range/ | Default requests/limits, min/max per container | 🔲 Planned |

---

### Section 11: Cluster Administration (3 episodes — 0 existing)

| Ep | Title | Docs URL | Concepts Covered | Status |
|----|-------|----------|-----------------|--------|
| NEW | Networking Overview | /cluster-administration/networking/ | CNI, network model, pod-to-pod routing | 🔲 Planned |
| NEW | Logging | /cluster-administration/logging/ | Node-level, sidecar, cluster-level logging architectures | 🔲 Planned |
| NEW | Cluster Autoscaling | /cluster-administration/node-autoscaling/ | Cluster Autoscaler, scale-up/down triggers | 🔲 Planned |

---

### Sections Skipped (out of scope for beginner series)

| Section | Reason |
|---------|--------|
| Windows in Kubernetes | Platform-specific, niche audience |
| Extending Kubernetes (CRD/Operator) | Advanced — save for dedicated series |
| Mixed-version proxy | Very advanced operational topic |
| cgroup v2 deep dives | Linux internals — brief mention only |
| Gang scheduling | Batch/ML specific |

---

## Episode Count Summary

| Section | Existing | New | Total |
|---------|----------|-----|-------|
| Overview | 2 | 3 | 5 |
| Architecture | 0 | 6 | 6 |
| Containers | 0 | 4 | 4 |
| Workloads | 5 | 7 | 12 |
| Services & Networking | 2 | 5 | 7 |
| Storage | 1 | 5 | 6 |
| Configuration | 2 | 2 | 4 |
| Scheduling & Eviction | 0 | 5 | 5 |
| Security | 0 | 5 | 5 |
| Policies | 0 | 2 | 2 |
| Cluster Admin | 0 | 3 | 3 |
| **TOTAL** | **12** | **47** | **59** |

**47 new episodes needed for full coverage of kubernetes.io/docs/concepts.**

---

## Recommended Watch Order

### Beginner Track (Episodes 1-15)
1. What is Kubernetes
2. Cluster Components
3. The Kubernetes API
4. Working with Objects / Labels & Namespaces
5. Pods
6. Pod Lifecycle
7. Deployments
8. Services
9. ConfigMaps
10. Secrets
11. Persistent Volumes
12. StatefulSets
13. DaemonSets & Jobs
14. CronJobs
15. Ingress

### Intermediate Track (Episodes 16-35)
16. Resource Management (requests/limits)
17. Liveness & Readiness Probes
18. Init Containers
19. Sidecar Containers
20. Nodes
21. Controllers (control loop)
22. The Scheduler
23. Taints & Tolerations
24. Assigning Pods to Nodes
25. Network Policies
26. DNS for Pods & Services
27. Volumes
28. Storage Classes
29. Dynamic Provisioning
30. RBAC
31. Service Accounts
32. Pod Security Standards
33. Resource Quotas
34. LimitRange
35. Autoscaling (HPA)

### Advanced Track (Episodes 36-59)
36. Gateway API
37. EndpointSlices
38. Ingress Controllers
39. Ephemeral Volumes
40. Volume Snapshots
41. Pod Disruption Budgets
42. Ephemeral Containers (kubectl debug)
43. Downward API
44. ReplicaSets
45. Pod Priority & Preemption
46. Node Pressure Eviction
47. Garbage Collection
48. Leases
49. Networking Overview (CNI)
50. Logging Architecture
51. Cluster Autoscaling
52. Runtime Classes
53. Container Images & Registries
54. Container Lifecycle Hooks
55. Cloud Controller
56. Multi-tenancy
57. cgroups
58. CRI
59. Container Runtime Interface

---

## Notes & Decisions Needed

1. **Episode 11 (DaemonSets & Jobs)** — currently combined. Should split into separate episodes for full coverage. Jobs has parallelism, completions, backoffLimit that deserve full treatment. CronJobs needs its own ep regardless.

2. **Operators/CRDs** — excluded from this plan. Could be a separate "Extending Kubernetes" series.

3. **kubectl commands** — not a docs/concepts page but viewers will want practical demos. Keep as supplementary "quick tip" Shorts rather than full episodes.

4. **Difficulty gating** — Advanced Track assumes viewer has done Beginner + Intermediate. Episodes should reference prerequisites explicitly.

5. **Production rate** — at 1 episode/day we're looking at ~47 days for full coverage. Suggest prioritizing Intermediate Track next (resource management, probes, scheduling are high-value for practitioners).
