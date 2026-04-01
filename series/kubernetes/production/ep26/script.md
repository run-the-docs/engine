# K8s ep26 — Pod Lifecycle (full docs coverage)

**Source:** https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
**Target length:** 8–10 minutes total
**Structure:** 8 segments, concatenated with ffmpeg into one continuous video

## Rules
- **Seg 1 only**: full episode intro card + channel branding
- **Segs 2–7**: NO title cards — visual cue only (section label fades in corner, 1s)
- **Seg 8 only**: recap + outro + end card
- **Every segment ends with a bridge sentence** that leads directly into the next topic
- **Narration flows continuously** — no "welcome back" or "in this segment"

## Docs Coverage Audit ✅

| Docs Section | Segment | Status |
|---|---|---|
| Pod lifetime — UIDs, scheduling once, binding | Seg 1 | ✅ |
| Pods and fault recovery — controllers, Pod UID never rescheduled | Seg 1 | ✅ |
| Associated lifetimes — volumes tied to Pod UID | Seg 1 | ✅ |
| Pod Scheduling Readiness (scheduling gates mention) | Seg 1 | ✅ |
| Pod phase — 5 values | Seg 2 | ✅ |
| Note: STATUS ≠ phase (CrashLoopBackOff, Terminating) | Seg 2 | ✅ |
| Note: graceful termination 30s, --force | Seg 2 | ✅ |
| Note: K8s 1.27 phase transition before deletion | Seg 2 | ✅ |
| Container states — Waiting/Running/Terminated | Seg 3 | ✅ |
| preStop hook runs before Terminated | Seg 3 | ✅ |
| postStart hook noted on Running | Seg 3 | ✅ |
| kubectl describe pod output | Seg 3 | ✅ |
| How Pods handle problems — crash sequence | Seg 4 | ✅ |
| CrashLoopBackOff causes (5 listed in docs) | Seg 4 | ✅ |
| CrashLoopBackOff debugging steps (5 listed in docs) | Seg 4 | ✅ |
| Backoff reset after 10 min success | Seg 4 | ✅ |
| Cloud-native resilience principle | Seg 4 | ✅ |
| restartPolicy — Always/OnFailure/Never | Seg 5 | ✅ |
| Restart behavior table (exit code × policy × sidecar) | Seg 5 | ✅ |
| Sidecar containers + special restart behaviour | Seg 5 | ✅ |
| 3 YAML examples (Always/OnFailure/Never) + sidecar YAML | Seg 5 | ✅ |
| ContainerRestartRules (beta v1.35) | Seg 5 | ✅ |
| RestartAllContainers (alpha v1.35) | Seg 5 | ✅ |
| Pod conditions — 4 built-in conditions | Seg 6 | ✅ |
| Ready condition controls traffic routing | Seg 6 | ✅ |
| Readiness gates — custom conditions | Seg 6 | ✅ |
| Pod termination — graceful sequence | Seg 7 | ✅ |
| Force deletion (--force --grace-period=0) | Seg 7 | ✅ |
| Garbage collection / node death | Seg 7 | ✅ |

---

## Segment 1 — Pod Lifetime (50–55s)
**File:** `seg1_lifetime.html`
**Intro:** Full episode card + channel branding
**Ends with:** bridge → phases

```
[NARRATION]

Your Pod just died. The question is: where in its lifecycle did it fail?

To answer that, you need to understand what a Pod actually goes through — from manifest to deletion.

A Pod is a single scheduling unit. Once it's assigned to a node — that binding is permanent. Kubernetes never moves a running Pod. If the node fails, the Pod is deleted and a new one is created elsewhere.

Every Pod gets a unique ID: a UID. That UID is permanent for the life of that Pod. Replace the Pod, you get a new UID — even with the same name. This matters because other objects, like volumes, have the same lifetime as a specific Pod UID. Delete the Pod, the volume goes with it.

A Pod on its own is disposable. Controllers — Deployments, StatefulSets, DaemonSets — handle replacement automatically. That's cloud-native resilience: design for failure, not against it.

One more thing before we get into the lifecycle itself: Pod Scheduling Readiness. You can hold a Pod in a pending state until all its scheduling gates are removed — useful when you need a group of Pods to only start once all of them exist.

Now let's walk through the five phases a Pod moves through.
```

**Visual scenes:**
1. (0–5s) Episode intro card: "kubernetes · pod lifecycle" — full branding
2. (5–12s) `kubectl get pods` output with `CrashLoopBackOff` — hook
3. (12–25s) Pod manifest → scheduler → binding arrow to node. UID badge on Pod.
4. (25–35s) Volume tied to Pod UID. Pod deleted → both gone. New Pod UID → new volume.
5. (35–45s) Node dies → Pod marked for deletion → Deployment creates replacement on new node
6. (45–52s) Scheduling gate concept: Pod held Pending → gates cleared → scheduled

---

## Segment 2 — Pod Phases (90–100s)
**File:** `seg2_phases.html`
**Intro:** Section label "Pod Phases" fades in corner (1s), no title card
**Ends with:** bridge → container states

```
[NARRATION]

A Pod's status field contains a phase — a high-level summary of where the Pod is in its lifecycle. Exactly five values, tightly defined.

Pending. The Pod has been accepted by the cluster but isn't running yet. It's either waiting for a node, or it's scheduled but still pulling the container image.

Running. Bound to a node. All containers created. At least one is still running — or starting, or restarting.

Succeeded. All containers exited with code zero. No restarts. This is the finish line for Jobs.

Failed. All containers terminated. At least one exited non-zero or was killed by the system.

Unknown. The state can't be determined — the kubelet on that node stopped communicating.

Important: STATUS in kubectl is not the phase. When you see CrashLoopBackOff or Terminating in the STATUS column, that's a display field — for human intuition. The real phase lives in pod.status.phase and it's always one of those five values.

When a Pod is deleted, it gets 30 seconds to shut down gracefully by default. You can change this with terminationGracePeriodSeconds, or bypass it entirely with kubectl delete --force.

Since Kubernetes 1.27: when a Pod is deleted, the kubelet transitions it to a terminal phase — Succeeded or Failed — before removing it from the API server. Static Pods and force-deleted Pods without a finalizer skip this.

Phases describe the Pod. But inside the Pod, each container has its own finer-grained state.
```

**Visual scenes:**
1. (0–2s) "Pod Phases" label fades in top-right corner
2. (2–45s) Five phase pills on horizontal timeline. Each highlights as narrated:
   - `Pending` (yellow): "Waiting to schedule / pulling image"
   - `Running` (green): "Bound. ≥1 container active"
   - `Succeeded` (blue): "All exited 0. No restarts."
   - `Failed` (red): "≥1 exited non-zero or killed"
   - `Unknown` (gray): "Node comms lost"
3. (45–62s) Split panel: `kubectl get pods` STATUS=`CrashLoopBackOff` ←→ `pod.status.phase = Running`. "Not the same."
4. (62–75s) 30s grace period countdown. `--force` badge skips it.
5. (75–95s) K8s 1.27 flow: delete → kubelet transitions to terminal phase → removed from API

---

## Segment 3 — Container States (75–85s)
**File:** `seg3_container_states.html`
**Intro:** "Container States" label fades in corner
**Ends with:** bridge → CrashLoopBackOff

```
[NARRATION]

The Pod has a phase. Each container inside it has a state. Three possible values.

Waiting. The container hasn't started. It's pulling an image, waiting on a Secret, or blocked behind an init container. kubectl describe shows a Reason field — ContainerCreating, ImagePullBackOff, and so on.

Running. The process is executing. If a postStart lifecycle hook was configured, it has already completed — postStart must finish before the container is considered Running. kubectl shows when the container entered this state.

Terminated. The container ran to completion or failed. You get a reason, an exit code, and start and finish timestamps. If a preStop hook is configured, it runs before Terminated is set — your application gets a window to clean up connections and finish in-flight work.

Use kubectl describe pod to inspect every container's state at once. You'll see State, Reason, Exit Code, Started, and Finished for each one.

Container states are the detail level. Pod phases are the summary. Both matter when you're debugging.

But the most important question in debugging isn't which state a container is in — it's why it keeps going back to Waiting or Terminated. That's where CrashLoopBackOff comes in.
```

**Visual scenes:**
1. (0–2s) "Container States" label fades in corner
2. (2–40s) Three state boxes:
   - `Waiting` (gray): "Reason: ContainerCreating / ImagePullBackOff"
   - `Running` (green): "postStart done, process executing"
   - `Terminated` (blue/red): "exit code + start/finish timestamps"
3. (40–58s) Lifecycle hooks on state transitions:
   - postStart → fires on start, must finish → Running
   - preStop → fires before Terminated → cleanup window
4. (58–78s) `kubectl describe pod` output block:
   ```
   State:     Running
     Started: Wed, 02 Apr 2026 08:00:00 +0000
   ```
   Then Terminated:
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
**Intro:** "How Pods Handle Problems" label fades in corner
**Ends with:** bridge → restartPolicy

```
[NARRATION]

When a container fails, Kubernetes tries to restart it immediately. But if it keeps failing, it applies exponential backoff: 10 seconds between attempts, then 20, then 40, capping at 5 minutes. That state — backoff in effect — is what kubectl shows as CrashLoopBackOff.

It's not a phase. It's the backoff mechanism being active on a container in the Running phase.

If a container runs successfully for 10 minutes, the backoff timer resets. The next crash is treated as the first.

The docs list five common causes: application bugs that cause the process to exit; configuration errors like wrong environment variables or missing config files; resource constraints — not enough CPU or memory to start; health checks timing out before the app is ready; and liveness or startup probes returning failure.

To debug: start with kubectl logs — this is almost always the fastest path to the root cause. Then kubectl describe pod to read events. Review environment variables and mounted volumes. Check your resource limits — OOM kills look like crashes. Run the image locally if nothing else works.

CrashLoopBackOff tells you a container is struggling. The cause is in the logs.

How aggressively Kubernetes restarts a crashing container — and under what conditions — is controlled by one field: restartPolicy.
```

**Visual scenes:**
1. (0–2s) "How Pods Handle Problems" label fades in corner
2. (2–28s) Crash animation: container starts → crash → 10s bar → restart → crash → 20s bar → crash → 40s bar → `CrashLoopBackOff` badge. Bars grow visually.
3. (28–42s) Backoff reset: green 10-min timer → resets → next crash restarts 10s gap
4. (42–65s) 5 causes, numbered, appear one by one:
   1. App bug → process exits
   2. Config error → wrong env vars
   3. Resource constraints → OOM killed
   4. Health check timeout
   5. Liveness/startup probe failure
5. (65–90s) Debug terminal:
   ```
   kubectl logs <pod>           # start here
   kubectl describe pod <pod>   # events + config issues
   # check: env vars, mounts, resource limits
   ```

---

## Segment 5 — Restart Policy (100–110s)
**File:** `seg5_restart_policy.html`
**Intro:** "restartPolicy" label fades in corner
**Ends with:** bridge → conditions

```
[NARRATION]

The restartPolicy field in the Pod spec controls what Kubernetes does when a container exits. Three values: Always, OnFailure, and Never. The default is Always.

Always: restart regardless of exit code — zero or non-zero. This is the only value Deployments allow. Use it for long-running services.

OnFailure: only restart on non-zero exit. Use this for Jobs that should retry on failure but complete cleanly on success.

Never: don't restart. The container runs once and stays Terminated.

The policy applies to app containers and regular init containers. Sidecars are the exception — they're init containers with a container-level restartPolicy of Always. A sidecar always restarts, regardless of the Pod's policy.

Here's the full matrix. With Always: both exit code 0 and non-zero trigger a restart. With OnFailure: only non-zero restarts. With Never: nothing restarts. Sidecar containers always restart in both cases.

Two new features in Kubernetes 1.35 worth knowing. ContainerRestartRules is beta — per-container restart policies and rules based on specific exit codes, letting you say "restart only if exit code is 42." RestartAllContainers is alpha — an action in restart rules that terminates and restarts the entire Pod in-place, preserving the Pod's UID, IP, and volumes. Useful for batch and ML workloads where rescheduling is expensive.

Now — once a Pod is running and containers are healthy, how does Kubernetes decide whether to send it traffic?
```

**Visual scenes:**
1. (0–2s) "restartPolicy" label fades in corner
2. (2–30s) Three-branch diagram from `restartPolicy`:
   - `Always` → green → "Services / Deployments"
   - `OnFailure` → yellow → "Jobs / batch"
   - `Never` → red → "One-shot tasks"
3. (30–52s) Restart behavior table (rows appear one at a time):
   ```
   Exit Code    Always      OnFailure   Never    Sidecar
   0 (Success)  Restarts    No          No       Always
   Non-zero     Restarts    Restarts    No       Always
   ```
   Sidecar column highlighted
4. (52–75s) Two YAML panels:
   - `restartPolicy: Always` — nginx Pod spec comment: "crashes restart automatically"
   - `restartPolicy: OnFailure` — Job spec comment: "retry on failure, stop on success"
   Then sidecar YAML: `initContainers` with container-level `restartPolicy: Always`
5. (75–95s) v1.35 feature callouts:
   - `ContainerRestartRules` (beta): exit-code-based per-container rules
   - `RestartAllContainers` (alpha): restarts entire Pod in-place, preserves UID/IP/volumes

---

## Segment 6 — Pod Conditions & Readiness Gates (65–75s)
**File:** `seg6_conditions.html`
**Intro:** "Pod Conditions" label fades in corner
**Ends with:** bridge → termination

```
[NARRATION]

A Pod can be Running, but still not receive traffic. That's because of conditions.

Kubernetes tracks four built-in conditions as boolean flags in pod.status.conditions.

PodScheduled: has the Pod been assigned to a node? Initialized: have all init containers completed? ContainersReady: are all containers reporting ready? And Ready: is the Pod ready to receive traffic?

Each condition has a status of True, False, or Unknown — plus a Reason and Message when something's wrong.

Ready is the one that matters most in production. It's what Services use to route traffic. If Ready is False, the Pod is removed from the Service's Endpoints — no traffic reaches it, even if it's in the Running phase.

You can extend this with readiness gates: custom conditions that your application or an external controller must set to True before Kubernetes considers the Pod Ready. Warm-up periods. External dependency checks. Database connection pools. Anything you need to gate traffic on.

That's how a Pod enters service. Now let's look at how it leaves — graceful termination.
```

**Visual scenes:**
1. (0–2s) "Pod Conditions" label fades in corner
2. (2–38s) Conditions table, rows appear one at a time:
   ```
   Condition           Status
   PodScheduled        True   ✓ Assigned to node
   Initialized         True   ✓ Init containers done
   ContainersReady     True   ✓ All containers ready
   Ready               False  ✗ No traffic
   ```
   `Ready: False` row pulses red
3. (38–55s) Service routing: Service → Pod A `Ready: True` (arrow through) → Pod B `Ready: False` (X, traffic blocked)
4. (55–70s) Readiness gate flow: custom condition box → app/controller sets True → Pod becomes Ready → traffic flows

---

## Segment 7 — Pod Termination & Garbage Collection (65–70s)
**File:** `seg7_termination.html`
**Intro:** "Pod Termination" label fades in corner
**Ends with:** natural end (leads into recap seg)

```
[NARRATION]

When you delete a Pod, Kubernetes doesn't kill it immediately. It runs a graceful termination sequence.

First, the Pod is marked Terminating and removed from Service endpoints — no new traffic. Then any preStop hooks run. Then SIGTERM is sent to container processes, giving them time to finish in-flight work and close connections. If anything is still running after the grace period — 30 seconds by default — SIGKILL is sent.

Configure terminationGracePeriodSeconds in the Pod spec to adjust that window. For applications that need more time to drain — load balancers, message consumers, database connections — set this appropriately.

Force deletion — kubectl delete pod --force --grace-period=0 — removes the Pod from the API immediately, without confirmation from the kubelet. The Pod may still be running on the node for a brief window. Use it only when a Pod is truly stuck.

For garbage collection: when a node becomes unreachable, the control plane marks its Pods for deletion after a timeout. Terminated Pods don't disappear immediately — they stay until garbage collected or manually removed. Their logs and describe output remain available until then.

That's the full lifecycle of a Pod. Let's recap.
```

**Visual scenes:**
1. (0–2s) "Pod Termination" label fades in corner
2. (2–40s) Graceful termination timeline, each step appears as an arrow + label:
   ```
   kubectl delete →
   Terminating (removed from endpoints) →
   preStop hooks →
   SIGTERM →
   [30s grace period] →
   SIGKILL
   ```
3. (40–52s) YAML: `terminationGracePeriodSeconds: 60`
4. (52–60s) `--force --grace-period=0` warning banner: "Pod removed from API. May still be running. Use carefully."
5. (60–68s) Node failure: Node X → Pods marked for deletion → stay visible until GC

---

## Segment 8 — Recap + Outro (42–45s)
**File:** `seg8_recap.html`
**Intro:** "Recap" — light transition
**Outro:** Full end card + playlist link

```
[NARRATION]

Let's pull it together.

Every Pod has a UID and is scheduled once. Controllers handle replacement.
Five phases: Pending, Running, Succeeded, Failed, Unknown — STATUS in kubectl is not the phase.
Three container states: Waiting, Running, Terminated — with postStart and preStop hooks at the transitions.
CrashLoopBackOff is exponential backoff in action. The cause is in kubectl logs.
restartPolicy — Always, OnFailure, Never — controls everything. Sidecars always restart.
Four conditions — Ready controls traffic. Readiness gates let you gate on anything.
Termination: preStop, SIGTERM, 30 seconds, SIGKILL. Force delete skips the wait.

If you watched this, you've read the Pod Lifecycle docs.

Next: resource requests and limits — how to tell Kubernetes exactly how much CPU and memory your Pod needs, and what happens when it asks for too much.

Run the Docs. One concept. From the actual docs.
```

**Visual scenes:**
1. (0–5s) Minimal "Recap" label, dark background
2. (5–30s) Eight bullet points, each with a small icon, appearing one per line:
   - UID + schedule once + controllers
   - 5 phases (mini timeline)
   - STATUS ≠ phase
   - 3 container states + hooks
   - CrashLoopBackOff = backoff → logs
   - restartPolicy 3 values + sidecars always
   - Ready = traffic gate + readiness gates
   - Termination sequence (mini)
3. (30–38s) "Next: Resource Requests & Limits" teaser card
4. (38–43s) End card: "Run the Docs · kubernetes · pod lifecycle" + K8s playlist link + channel link
5. (43–45s) Fade to black

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

- [ ] Seg 1 — Pod Lifetime (~52s)
- [ ] Seg 2 — Pod Phases (~95s)
- [ ] Seg 3 — Container States (~80s)
- [ ] Seg 4 — CrashLoopBackOff (~95s)
- [ ] Seg 5 — Restart Policy (~105s)
- [ ] Seg 6 — Conditions & Readiness Gates (~70s)
- [ ] Seg 7 — Termination & GC (~68s)
- [ ] Seg 8 — Recap (~44s)
- [ ] Concatenate → ep26.mp4
- [ ] Verify total duration ≥ 8 min
- [ ] Verify narration flows continuously (no jarring cuts)
- [ ] Upload to YouTube, add to K8s playlist
- [ ] Update series/kubernetes/episodes.md
- [ ] Commit all production assets to engine repo
