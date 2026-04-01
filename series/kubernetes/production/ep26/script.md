# K8s ep26 — Pod Lifecycle (full docs coverage)

**Source:** https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
**Target length:** 8–10 minutes total
**Structure:** 7 segments, concatenated with ffmpeg

## Docs Coverage Audit

| Docs Section | Segment |
|---|---|
| Pod lifetime — UIDs, scheduling once, binding | Seg 1 |
| Pods and fault recovery — controllers, Pod UID never rescheduled | Seg 1 |
| Associated lifetimes — volumes tied to Pod UID | Seg 1 |
| Pod phase — 5 values | Seg 2 |
| Note: STATUS ≠ phase (CrashLoopBackOff, Terminating) | Seg 2 |
| Note: graceful termination 30s, --force | Seg 2 |
| Note: K8s 1.27 phase transition before deletion | Seg 2 |
| Container states — Waiting/Running/Terminated | Seg 3 |
| preStop hook runs before Terminated | Seg 3 |
| How Pods handle problems — crash sequence | Seg 4 |
| CrashLoopBackOff causes (5 listed in docs) | Seg 4 |
| CrashLoopBackOff debugging steps | Seg 4 |
| Container restarts — cloud-native resilience principle | Seg 4 |
| restartPolicy — Always/OnFailure/Never | Seg 5 |
| Restart behavior table (exit code × policy × sidecar) | Seg 5 |
| Sidecar containers + special restart behaviour | Seg 5 |
| 3 YAML examples (Always/OnFailure/Never) + sidecar YAML | Seg 5 |
| ContainerRestartRules (beta v1.35) | Seg 5 note |
| Pod conditions — 4 built-in conditions | Seg 6 |
| Ready condition controls traffic routing | Seg 6 |
| Readiness gates — custom conditions | Seg 6 |
| Pod termination — graceful sequence (preStop → 30s → SIGTERM → SIGKILL) | Seg 7 |
| Force deletion (--force --grace-period=0) | Seg 7 |
| Garbage collection | Seg 7 |

---

## Segment 1 — Pod Lifetime (45–55s)

**File:** `seg1_lifetime.html`

**Script:**

> A Pod is a single scheduling unit. Once it's assigned to a node — that's called binding — it stays on that node until it terminates or is deleted.
>
> Every Pod gets a unique ID, called a UID. That UID is permanent for the life of that Pod. If a Pod is deleted and replaced, the replacement gets a new UID — even if it has the same name.
>
> This matters because other objects, like volumes, have the same lifetime as a specific Pod UID. Delete the Pod, the volume goes with it. Create a replacement Pod — a new volume is created from scratch.
>
> A Pod is only scheduled once. Kubernetes never moves a running Pod to a different node. If the node fails, Kubernetes deletes the Pod and creates a new one — potentially on a different node.
>
> That's why you need controllers. Deployments, StatefulSets, DaemonSets — they manage the work of replacing Pods when they fail. A Pod on its own is disposable. A controller makes that disposability invisible.

**Visual scenes:**
1. (0–5s) Hook title: "Pod Lifecycle" — episode card
2. (5–20s) Timeline: Pod manifest → scheduler → binding to node → running. UID badge appears on Pod.
3. (20–30s) Volume icon attached to Pod UID. Pod deleted → both disappear. New Pod UID appears → new volume.
4. (30–45s) Node failure scenario: Pod on Node → Node X → Pod marked for deletion → Deployment creates replacement on new Node
5. (45–52s) "Controllers make disposability invisible" — bold text summary

---

## Segment 2 — Pod Phases (90–100s)

**File:** `seg2_phases.html`

**Script:**

> A Pod's status has a phase field — a high-level summary of where the Pod is in its lifecycle. There are exactly five values.
>
> Pending. The Pod has been accepted by the cluster but isn't running yet. It's waiting to be scheduled, or scheduled but still pulling the container image.
>
> Running. The Pod is bound to a node. All containers have been created. At least one is still running — or starting, or restarting.
>
> Succeeded. All containers exited with code zero. They won't be restarted. This is the finish line for Jobs.
>
> Failed. All containers have terminated. At least one exited with a non-zero code or was killed by the system.
>
> Unknown. The Pod's state can't be determined — usually because the kubelet on that node stopped communicating.
>
> One important note. When kubectl shows "CrashLoopBackOff" or "Terminating" in the STATUS column, that's a display field for human intuition — not the phase. The actual phase is stored in pod.status.phase, and it's always one of these five values.
>
> When a Pod is deleted, it gets 30 seconds to terminate gracefully by default. You can override this with terminationGracePeriodSeconds, or skip it entirely with kubectl delete --force.
>
> Since Kubernetes 1.27: when a Pod is deleted, the kubelet first transitions it to a terminal phase — either Succeeded or Failed — before it's removed from the API server. Static Pods and force-deleted Pods without a finalizer are exceptions.

**Visual scenes:**
1. (0–8s) Five phase pills on a horizontal timeline: `Pending` → `Running` → `Succeeded` / `Failed`, `Unknown` below
2. (8–45s) Each phase highlights as narrated, 2-line description below each:
   - Pending: "Accepted. Waiting to schedule or pull image."
   - Running: "Bound. ≥1 container active."
   - Succeeded: "All exited 0. No restarts."
   - Failed: "≥1 exited non-zero or killed."
   - Unknown: "Node comms lost."
3. (45–60s) Split view: `kubectl get pods` output showing STATUS column with `CrashLoopBackOff`. Arrow to `pod.status.phase = Running`. "Not the same thing."
4. (60–75s) Graceful termination: 30s countdown animation. `--force` badge skips it.
5. (75–95s) K8s 1.27 note: deletion flow diagram — Pod deleted → kubelet transitions to Failed/Succeeded → removed from API server

---

## Segment 3 — Container States (75–85s)

**File:** `seg3_container_states.html`

**Script:**

> The Pod has a phase. Each container inside it has its own state. Three possible values.
>
> Waiting. The container hasn't started yet. It's pulling an image, waiting on a Secret, or blocked by an init container. kubectl describe shows a Reason field — things like ContainerCreating or ImagePullBackOff.
>
> Running. The container process is executing. If a postStart lifecycle hook was configured, it's already completed. kubectl shows when the container entered this state.
>
> Terminated. The container ran to completion or failed. You get a reason, an exit code, and start and finish timestamps. If a preStop hook is configured, it runs before the container enters Terminated — giving your app time to clean up.
>
> Use kubectl describe pod to see the state of every container in a Pod. The output shows State, Reason, Exit Code, Started, and Finished for each one.
>
> Container states are the detail level. Pod phases are the summary. Both matter when you're debugging.

**Visual scenes:**
1. (0–5s) Title card: "Container States"
2. (5–40s) Three state boxes appear:
   - `Waiting` (gray): "Reason: ContainerCreating / ImagePullBackOff"
   - `Running` (green): "postStart hook done, process alive"
   - `Terminated` (blue/red): "exit code + start + finish timestamps"
   Each box highlights as narrated
3. (40–60s) Lifecycle hook callouts:
   - postStart → fires at container start → must complete before Running
   - preStop → fires before Terminated → cleanup window
   Small arrows on the state flow showing where each hook fires
4. (60–78s) `kubectl describe pod` output panel showing container state block:
   ```
   State:          Running
     Started:      Wed, 02 Apr 2026 08:00:00 +0000
   ```
   Then Terminated variant:
   ```
   State:          Terminated
     Reason:       Error
     Exit Code:    1
     Started:      ...
     Finished:     ...
   ```

---

## Segment 4 — CrashLoopBackOff & Debugging (90–100s)

**File:** `seg4_crashloop.html`

**Script:**

> When a container fails, Kubernetes tries to restart it immediately — based on the restartPolicy. But if it keeps failing, Kubernetes applies exponential backoff: 10 seconds, then 20, then 40, capping at 5 minutes between restart attempts.
>
> That's CrashLoopBackOff. It's not a phase. It's the backoff mechanism being active.
>
> If a container runs successfully for 10 minutes, the backoff timer resets. The next crash is treated as the first.
>
> The docs list five common causes of CrashLoopBackOff: application bugs causing the process to exit; configuration errors like wrong environment variables or missing config files; resource constraints — not enough CPU or memory to start; health checks failing because the app isn't ready in time; and liveness or startup probes returning failure.
>
> To debug it: first, kubectl logs to see the container's output — this is usually the fastest path. Then kubectl describe pod to see events, which surfaces scheduling and config issues. Review your environment variables and mounted volumes. Check your resource limits — the container might be OOM-killed on startup. And if all else fails, run the image locally.
>
> CrashLoopBackOff tells you a container is struggling to start. The cause is in the logs.

**Visual scenes:**
1. (0–5s) Title: "CrashLoopBackOff"
2. (5–30s) Animated crash sequence: container starts → crashes → 10s gap → restart → crash → 20s gap → restart → crash → 40s gap → "CrashLoopBackOff" label appears. Growing gaps visualised as expanding bars.
3. (30–45s) "Backoff reset" note: green 10-min timer → resets → next crash = 10s gap again
4. (45–65s) Five causes as numbered list, appearing one by one:
   1. App bug → process exits
   2. Config error → wrong env vars
   3. Resource constraints → OOM killed
   4. Health check timeout
   5. Liveness/startup probe failure
5. (65–90s) Debug steps as terminal commands:
   ```
   kubectl logs <pod>          # start here
   kubectl describe pod <pod>  # events
   # check env vars, mounts, resource limits
   ```

---

## Segment 5 — Restart Policy (90–100s)

**File:** `seg5_restart_policy.html`

**Script:**

> The restartPolicy field in the Pod spec controls what happens when a container exits. Three values: Always, OnFailure, and Never. Default is Always.
>
> Always means restart regardless of exit code — zero or non-zero. This is the only value Deployments allow. Use it for long-running services.
>
> OnFailure means only restart if the exit code is non-zero. Use this for Jobs that should retry on failure but stop when they succeed.
>
> Never means don't restart. Ever. The container runs once and stays in Terminated.
>
> The policy applies to app containers and regular init containers. Sidecars are different — they're defined as init containers with their own container-level restartPolicy set to Always. A sidecar always restarts, regardless of the Pod-level policy.
>
> Here's the full matrix. Exit code zero with Always: restarts. Exit code zero with OnFailure: does not restart. Exit code zero with Never: does not restart. Non-zero with Always: restarts. Non-zero with OnFailure: restarts. Non-zero with Never: does not restart. Sidecar containers always restart in both cases.
>
> One more thing: Kubernetes 1.35 adds ContainerRestartRules in beta — per-container restart policies and rules based on specific exit codes. If you need fine-grained control over which container restarts when, that's worth reading.

**Visual scenes:**
1. (0–8s) Title: "restartPolicy"
2. (8–35s) Three branches from `restartPolicy`:
   - `Always` → green → "Deployment use case — services"
   - `OnFailure` → yellow → "Job use case — batch"
   - `Never` → red → "One-shot tasks"
3. (35–55s) Restart behavior table:
   ```
   Exit Code    Always      OnFailure   Never    Sidecar
   0 (Success)  Restarts    No          No       Always
   Non-zero     Restarts    Restarts    No       Always
   ```
   Rows appear one at a time, Sidecar column highlighted
4. (55–75s) Two YAML code panels side by side:
   - Left: `restartPolicy: Always` with nginx Deployment comment
   - Right: `restartPolicy: OnFailure` with Job comment
5. (75–90s) Sidecar YAML: `initContainers` with `restartPolicy: Always` at container level — "Sidecar ignores Pod policy"
6. (90–98s) Beta note: "ContainerRestartRules (v1.35 beta) — per-container exit-code rules"

---

## Segment 6 — Pod Conditions & Readiness Gates (60–70s)

**File:** `seg6_conditions.html`

**Script:**

> Beyond phases, Kubernetes tracks four Pod conditions — boolean flags in pod.status.conditions.
>
> PodScheduled: has the Pod been assigned to a node? Initialized: have all init containers completed? ContainersReady: are all containers reporting ready? And Ready: is the Pod ready to receive traffic?
>
> Each condition has a status of True, False, or Unknown, plus a reason and message when something's wrong.
>
> The Ready condition is what Services use. If Ready is False, the Pod is removed from the Service's endpoints — no traffic reaches it, even if it's in the Running phase.
>
> You can extend this with readiness gates. Define a custom condition that your application — or an external system — must set to True before Kubernetes marks the Pod Ready. This is the escape hatch when built-in conditions aren't enough: warm-up periods, external dependency checks, anything you need to gate on.

**Visual scenes:**
1. (0–5s) Title: "Pod Conditions"
2. (5–35s) Conditions table, rows appear one by one:
   ```
   Condition           Status    Meaning
   PodScheduled        True      Assigned to node
   Initialized         True      Init containers done
   ContainersReady     True      All containers ready
   Ready               False  ← no traffic
   ```
   Ready row pulses red
3. (35–50s) Service routing diagram: Service → two Pods. Pod with `Ready: True` gets arrow. Pod with `Ready: False` gets X. Clean split.
4. (50–65s) Readiness gate: custom condition box → app sets it True → Pod becomes Ready. "Your app controls its own readiness."

---

## Segment 7 — Pod Termination & Garbage Collection (60–70s)

**File:** `seg7_termination.html`

**Script:**

> When you delete a Pod, Kubernetes doesn't kill it immediately. It starts a graceful termination sequence.
>
> First, the Pod is marked Terminating and removed from Service endpoints — no new traffic. Then Kubernetes runs any preStop hooks. Then it sends SIGTERM to the main container process, giving it time to finish in-flight work. If the process is still running after the grace period — 30 seconds by default — it gets SIGKILL.
>
> You can configure terminationGracePeriodSeconds in the Pod spec to change that window. For force deletion — kubectl delete pod --force --grace-period=0 — Kubernetes removes the Pod from the API server immediately, without waiting for the kubelet to confirm termination. Use with care: the Pod may still be running on the node briefly.
>
> For garbage collection: when a node dies, the control plane marks all Pods on that node for deletion after a timeout. Terminated Pods aren't automatically removed — they stay until garbage collected or manually deleted. The kubectl describe output, including logs, remains available until then.

**Visual scenes:**
1. (0–5s) Title: "Pod Termination"
2. (5–40s) Termination sequence timeline:
   ```
   kubectl delete pod →
   [Terminating] → removed from Service endpoints →
   preStop hook → SIGTERM → [30s grace period] → SIGKILL
   ```
   Each step appears as an arrow + label
3. (40–52s) YAML snippet: `terminationGracePeriodSeconds: 60`
4. (52–62s) Force delete warning: `--force --grace-period=0` — "Pod removed from API, may still be running. Use with care."
5. (62–70s) Node failure + garbage collection: Node X → Pods marked for deletion → stay visible until collected

---

## Segment 8 — Recap (40–45s)

**File:** `seg8_recap.html`

**Script:**

> Let's pull it together.
>
> Every Pod has a UID and is scheduled once. Controllers handle replacement.
> Five phases: Pending, Running, Succeeded, Failed, Unknown. STATUS in kubectl is not the phase.
> Three container states: Waiting, Running, Terminated. preStop and postStart hooks fire at state transitions.
> CrashLoopBackOff is exponential backoff — the cause is in kubectl logs.
> restartPolicy — Always, OnFailure, Never — controls everything. Sidecars always restart.
> Four conditions — Ready controls traffic. Readiness gates let you customise it.
> Graceful termination: preStop → SIGTERM → 30s → SIGKILL.
>
> Next: resource requests and limits — how to tell Kubernetes how much CPU and memory your Pod needs.

**Visual scenes:**
1. (0–5s) "Recap" title card
2. (5–32s) Eight bullet points appear sequentially, each with a mini-icon:
   - UID + scheduling once
   - 5 phases timeline (mini)
   - STATUS ≠ phase
   - 3 container states
   - CrashLoopBackOff = backoff → check logs
   - restartPolicy 3 values + sidecars
   - Ready condition = traffic gate
   - Graceful termination sequence
3. (32–40s) "Next: Resource Requests & Limits" episode teaser card
4. (40–44s) End card: "Run the Docs · kubernetes · pod lifecycle" + playlist link
5. (44–45s) Fade to black

---

## ffmpeg Concatenation

```bash
cat > /tmp/ep26_concat.txt << 'EOF'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg1.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg2.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg3.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg4.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg5.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg6.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg7.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg8.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i /tmp/ep26_concat.txt \
  -c copy \
  /Users/claude/runthedocs/videos/kubernetes/ep26.mp4
```

## Production Checklist

- [ ] Seg 1 — Pod Lifetime (~50s)
- [ ] Seg 2 — Pod Phases (~95s)
- [ ] Seg 3 — Container States (~80s)
- [ ] Seg 4 — CrashLoopBackOff (~95s)
- [ ] Seg 5 — Restart Policy (~95s)
- [ ] Seg 6 — Conditions & Readiness Gates (~65s)
- [ ] Seg 7 — Termination & GC (~65s)
- [ ] Seg 8 — Recap (~43s)
- [ ] Concatenate → ep26.mp4
- [ ] Verify total duration ≥ 8 min
- [ ] Upload to YouTube, add to K8s playlist
- [ ] Update series/kubernetes/episodes.md
- [ ] Commit all production assets to engine repo
