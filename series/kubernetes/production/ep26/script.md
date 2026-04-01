# K8s ep26 — Pod Lifecycle (6-min deep dive)

**Source:** https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
**Target length:** 6–7 minutes total
**Structure:** 5 segments, concatenated with ffmpeg

---

## Segment 1 — Hook (30–45s)

**File:** `seg1_hook.html`
**Script (~60 words, ~25s narration + 10s intro silence + 5s hook beat):**

> You deployed your app. It was running. Now kubectl says CrashLoopBackOff.
> What happened?
>
> To debug anything in Kubernetes, you need to understand what a Pod actually goes through from the moment you apply a manifest to the moment it dies.
>
> This is Pod Lifecycle. Five phases. Three container states. One restart policy that controls everything.
>
> Let's go.

**Visual scenes:**
1. (0–3s) Dark screen, terminal text `kubectl get pods` fades in showing `CrashLoopBackOff`
2. (3–8s) Red pulse on the CrashLoopBackOff text, "What happened?" appears
3. (8–20s) Diagram: Pod box appears centre, lifecycle arrow draws left-to-right (Pending → Running → Failed), each phase label fades in
4. (20–30s) "Five phases. Three container states." — stacked bold text, each line drops in
5. (30–40s) "Let's go." + React-style episode title card: `kubernetes · pod lifecycle`

---

## Segment 2 — Pod Phases (85–95s)

**File:** `seg2_phases.html`
**Script (~200 words, ~80s narration):**

> A Pod's phase is the highest-level summary of its lifecycle. There are exactly five values — and Kubernetes is very strict about them.
>
> Pending. The Pod has been accepted by the cluster, but it's not running yet. This could mean it's waiting to be scheduled to a node — or it's scheduled, but the container image is still downloading.
>
> Running. The Pod is bound to a node. All containers have been created. At least one is still running — or starting, or restarting.
>
> Succeeded. All containers have terminated with exit code zero. They will not be restarted. This is the happy ending for batch jobs.
>
> Failed. All containers have terminated. At least one exited with a non-zero code — or was killed by the system. If your restartPolicy is Never, this is the end.
>
> Unknown. The phase can't be determined — usually because the node running the Pod has lost contact with the control plane.
>
> One important note: Status is not phase. When kubectl shows "CrashLoopBackOff" or "Terminating" in the STATUS column — that's a display field for human intuition. The actual phase is stored in pod.status.phase, and it's one of these five values only.

**Visual scenes:**
1. (0–5s) Section title card: "Pod Phases" — large text, dark BG
2. (5–20s) Five phase pills appear left-to-right in a timeline row:
   - `Pending` (yellow) → `Running` (green) → `Succeeded` (blue) / `Failed` (red)
   - `Unknown` (gray) floats below
3. (20–50s) Each phase pill highlights as it's narrated, with a 2-line description appearing below:
   - Pending: "Waiting to schedule / pulling image"
   - Running: "Bound to node, ≥1 container active"
   - Succeeded: "All exited 0 — no restarts"
   - Failed: "At least one exited non-zero"
   - Unknown: "Node comms lost"
4. (50–75s) Split panel: LEFT shows `kubectl get pods` output with STATUS column. RIGHT shows `pod.status.phase` field. Arrow connects STATUS "CrashLoopBackOff" to phase "Running" — "Not the same thing."
5. (75–90s) Recap row: all 5 phases visible simultaneously, dimmed except the phase being summarised

---

## Segment 3 — Container States & Restart Policy (85–95s)

**File:** `seg3_container_states.html`
**Script (~210 words, ~85s narration):**

> The Pod has a phase. But each container inside it has its own state — and that's where the detail lives.
>
> Waiting. The container hasn't started yet. It's pulling an image, waiting on a Secret, or blocked by an init container. kubectl describe will show you a Reason field.
>
> Running. The container is executing. If a postStart hook was configured, it's already finished. This state tells you the main process is alive.
>
> Terminated. The container finished — either successfully or with an error. You get a reason, an exit code, and a start and finish time.
>
> Now — what happens when a container fails?
>
> Kubernetes uses the restartPolicy to decide. There are three values: Always, OnFailure, and Never. The default is Always.
>
> Always means restart no matter what — exit zero or non-zero. Use this for long-running services in Deployments.
>
> OnFailure means only restart if the container exits with a non-zero code. Use this for Jobs that should retry on failure but stop when they succeed.
>
> Never means don't restart. Ever. The container runs once and stays dead.
>
> When restarts happen repeatedly, the kubelet applies exponential backoff — 10 seconds, 20, 40, up to 5 minutes between attempts. That's the CrashLoopBackOff you see in kubectl. It's not a phase — it's the backoff mechanism in action.

**Visual scenes:**
1. (0–5s) Title card: "Container States"
2. (5–35s) Three state boxes appear in a row:
   - `Waiting` (gray) with sub-label "Reason: ContainerCreating / ImagePullBackOff"
   - `Running` (green) with sub-label "postStart done, process alive"
   - `Terminated` (blue/red) with sub-label "exit code + timestamps"
3. (35–55s) "restartPolicy" label appears. Three branches split below:
   - `Always` → "Always restart" (service icon)
   - `OnFailure` → "Restart on non-zero exit" (job icon)
   - `Never` → "Run once" (one-shot icon)
   Each branch highlights as narrated
4. (55–80s) Animated timeline: container crashes → 10s wait → restart → crash → 20s wait → restart → "CrashLoopBackOff" label appears. Exponential backoff visualised as growing gaps
5. (80–90s) "CrashLoopBackOff = backoff in action. Not a phase." — text emphasis

---

## Segment 4 — Pod Conditions & Readiness Gates (55–65s)

**File:** `seg4_conditions.html`
**Script (~145 words, ~58s narration):**

> Beyond phases, Kubernetes tracks Pod conditions — boolean flags that describe specific aspects of the Pod's state.
>
> The four built-in conditions are: PodScheduled — has the Pod been assigned to a node? Initialized — have all init containers completed? ContainersReady — are all containers reporting ready? And Ready — is the Pod ready to receive traffic?
>
> Each condition has a status of True, False, or Unknown.
>
> The Ready condition is what Services use to decide whether to route traffic to a Pod. If it's False, the Pod is excluded from load balancing — even if it's Running.
>
> You can also define readiness gates — custom conditions your application must set before Kubernetes marks the Pod as Ready. This gives you control: maybe your app needs a warm-up period, or an external system needs to confirm readiness before traffic arrives.
>
> Readiness gates are the escape hatch when the built-in conditions aren't enough.

**Visual scenes:**
1. (0–5s) Title card: "Pod Conditions"
2. (5–35s) Conditions table appears row by row:
   ```
   Condition         Status    Meaning
   PodScheduled      True      Assigned to node
   Initialized       True      Init containers done
   ContainersReady   True      All containers ready
   Ready             False     ← traffic excluded
   ```
   The `Ready: False` row pulses red
3. (35–50s) Service → Pod routing diagram. Pod with `Ready: False` has an X through the arrow. Pod with `Ready: True` gets traffic. Clean, clear.
4. (50–62s) "Readiness Gates" label. Custom condition box appears: app sets condition manually → Pod becomes Ready. "Your app controls readiness."

---

## Segment 5 — Recap + What's Next (40–50s)

**File:** `seg5_recap.html`
**Script (~95 words, ~38s narration):**

> Let's pull it together.
>
> A Pod moves through five phases: Pending, Running, Succeeded, Failed, Unknown.
> Each container inside has three states: Waiting, Running, Terminated.
> The restartPolicy — Always, OnFailure, or Never — controls what happens after failure.
> CrashLoopBackOff is exponential backoff, not a phase.
> And conditions — especially Ready — control whether a Pod receives traffic.
>
> Next up: resource requests and limits. How you tell Kubernetes exactly how much CPU and memory your Pod needs — and what happens when it asks for too much.
>
> Run the Docs. One concept. From the actual docs.

**Visual scenes:**
1. (0–5s) "Recap" title card
2. (5–30s) Five bullet points appear one at a time, each with a small icon:
   - 5 phases timeline (mini)
   - 3 container states (mini boxes)
   - restartPolicy: Always / OnFailure / Never
   - CrashLoopBackOff = backoff
   - Ready condition = traffic gate
3. (30–42s) "Next: Resource Requests & Limits" — next episode teaser card, same style as landscape eps
4. (42–48s) End card: "Run the Docs" + channel link + K8s playlist link
5. (48–50s) Fade to black

---

## ffmpeg Concatenation

After all 5 segments are rendered and encoded:

```bash
# Create concat list
cat > /tmp/ep26_concat.txt << 'EOF'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg1.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg2.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg3.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg4.mp4'
file '/Users/claude/runthedocs/videos/kubernetes/ep26_seg5.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i /tmp/ep26_concat.txt \
  -c copy \
  /Users/claude/runthedocs/videos/kubernetes/ep26.mp4
```

## Production Checklist

- [ ] Seg 1 TTS + HTML + render + encode → ep26_seg1.mp4
- [ ] Seg 2 TTS + HTML + render + encode → ep26_seg2.mp4
- [ ] Seg 3 TTS + HTML + render + encode → ep26_seg3.mp4
- [ ] Seg 4 TTS + HTML + render + encode → ep26_seg4.mp4
- [ ] Seg 5 TTS + HTML + render + encode → ep26_seg5.mp4
- [ ] Concatenate → ep26.mp4
- [ ] Verify total duration is 6–7 min
- [ ] Upload to YouTube, add to K8s playlist
- [ ] Update episodes.md
- [ ] Commit all production assets to engine repo
