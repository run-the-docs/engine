# K8s ep13 — Labels & Selectors (7-min deep dive)

**Source:** 
- https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
- https://kubernetes.io/docs/concepts/overview/working-with-objects/field-selectors/

**Target length:** 7–8 minutes total
**Structure:** 5 segments, concatenated with ffmpeg

---

## Segment 1 — Hook (35–45s)

**File:** `seg1_hook.html`
**Script (~70 words, ~28s narration):**

> You have fifty Pods running. Some are in production. Some are in staging. Some are backends, some are frontends. How does Kubernetes even know which is which?
>
> The answer is Labels. Two words. A colon. Maximum power.
>
> Labels let you attach arbitrary metadata to any object — and then query, route, and manage objects in bulk using that metadata. Selectors are what make the queries possible.
>
> This is episode thirteen. Labels and Selectors. Let's go.

**Visual scenes:**
1. (0–3s) Dark screen, multiple Pod boxes appear with no labels — just "pod-1", "pod-2", "pod-3"...
2. (3–8s) "How does Kubernetes know which is which?" appears in amber text
3. (8–18s) Labels animate onto pods: environment: production, tier: frontend, app: nginx — color coded
4. (18–28s) Bold text: "Labels. Two words. A colon. Maximum power."
5. (28–38s) Episode title card: `kubernetes · labels & selectors · ep 13`

---

## Segment 2 — What Are Labels & Syntax (90–100s)

**File:** `seg2_labels.html`
**Script (~230 words, ~92s narration):**

> Labels are key-value pairs attached to Kubernetes objects. Any object — Pods, Services, Deployments, Nodes, even Namespaces.
>
> They're meant to carry identifying attributes that are meaningful to users. Not to the Kubernetes control plane itself — just to you, your team, and your tooling.
>
> If information doesn't help identify or select objects — like build timestamps or creator emails — use annotations instead. Labels are for selection. Annotations are for everything else.
>
> Now, label syntax. A label key has two parts: an optional prefix and a name, separated by a slash.
>
> The name is required. It must be 63 characters or less, starting and ending with an alphanumeric character. Dashes, underscores, and dots are allowed in between.
>
> The prefix is optional. If present, it must be a valid DNS subdomain — up to 253 characters. The prefixes kubernetes.io and k8s.io are reserved for Kubernetes core components.
>
> If you're writing an operator or controller that adds labels to user objects, you must use a prefix — so users know the label came from automation, not their own config.
>
> Label values follow similar rules: 63 characters max, can be empty, must start and end with alphanumeric if non-empty.
>
> Here's a real example. A Pod manifest with two labels — environment: production and app: nginx. That's all it takes.
>
> Common patterns you'll see in real clusters: release: stable or canary. Environment: dev, qa, or production. Tier: frontend, backend, or cache. Partition: customerA or customerB.
>
> You can define your own conventions. The constraint is just syntax, not semantics.

**Visual scenes:**
1. (0–8s) Split: left shows YAML with labels block, right shows the rendered pod with label badges
2. (8–20s) Diagram: "Labels vs Annotations" — labels connected to selector arrows, annotations connected to metadata tooltip
3. (20–40s) Label key anatomy: `[prefix/]name` — prefix box shows "kubernetes.io/" in red (reserved), name box shows "app" in green
4. (40–60s) Validation rules animate: name max 63 chars, prefix max 253 chars, alphanumeric boundaries, allowed chars: - _ .
5. (60–80s) YAML example: Pod with environment: production, app: nginx — clean code display
6. (80–95s) Common label table: release, environment, tier, partition, track — each row fades in

---

## Segment 3 — Label Selectors (90–100s)

**File:** `seg3_selectors.html`
**Script (~235 words, ~94s narration):**

> Labels are only useful if you can query them. That's what selectors are for.
>
> There are two types: equality-based and set-based.
>
> Equality-based requirements use the equals, double-equals, or not-equals operators. All three mean what you'd expect. environment=production selects every object where environment equals production. tier!=frontend excludes everything with tier set to frontend — including objects that have no tier label at all.
>
> You combine requirements with a comma, which acts as a logical AND. There is no OR operator. If you need OR — use set-based selectors.
>
> Set-based requirements are more expressive. The in operator selects objects where the label value is in a set. environment in (production, qa) matches both production and qa environments. Notin does the opposite.
>
> The exists operator just checks whether a label key is present, regardless of value. partition selects anything that has a partition label. Exclamation-partition selects anything that does not.
>
> You can mix both types in a single selector. partition in (customerA, customerB), environment != qa — that's a perfectly valid combined selector.
>
> Now, a critical distinction: not all API objects support set-based selectors. Services and ReplicationControllers only support the equality-based form in their selector field. But newer resources — Deployments, ReplicaSets, DaemonSets, Jobs — support both, using matchLabels and matchExpressions.
>
> matchLabels is a simple key-value map. matchExpressions is an array where each entry specifies a key, an operator, and a set of values. All entries are ANDed together.

**Visual scenes:**
1. (0–12s) Two columns appear: "Equality-based" and "Set-based" with operator lists
2. (12–30s) Live demo: filter animation on Pod grid — environment=production highlights matching pods in green
3. (30–48s) Set-based demo: environment in (production, qa) — two groups light up; "No OR operator" warning badge
4. (48–65s) Exists/notin demo: !partition — pods without the label highlighted
5. (65–80s) Table: Services/ReplicationControllers → equality only; Deployments/ReplicaSets/DaemonSets/Jobs → set-based supported
6. (80–95s) YAML example: matchLabels + matchExpressions side-by-side, each field annotated

---

## Segment 4 — API Usage & kubectl (85–95s)

**File:** `seg4_api.html`
**Script (~215 words, ~86s narration):**

> Labels are not just YAML decoration. They're integrated into the Kubernetes API as first-class query parameters.
>
> When you run kubectl get pods with the lowercase L flag, you're passing a label selector to the API server. Under the hood it becomes a URL query parameter: labelSelector equals environment equals production.
>
> The equality-based form looks like this in a URL: labelSelector=environment%3Dproduction,tier%3Dfrontend — percent-encoded equals signs.
>
> Set-based looks like this: labelSelector=environment+in+%28production%2Cqa%29 — the in keyword, percent-encoded parens, percent-encoded commas.
>
> In practice you use kubectl, not raw URLs. Here are the patterns you'll use daily.
>
> kubectl get pods -l environment=production,tier=frontend — multiple equality requirements.
>
> kubectl get pods -l 'environment in (production, qa)' — set-based, quotes required in the shell because of the parentheses.
>
> kubectl get pods -l 'environment,environment notin (frontend)' — exists check combined with notin — a real pattern for finding pods that have an environment label but it's not frontend.
>
> You can also add a label column to any get output with the capital L flag. kubectl get pods -Lapp -Ltier -Lrole prints those label values as extra columns. Invaluable for debugging a cluster with many services.
>
> To update labels on existing objects, use kubectl label. kubectl label pods -l app=nginx tier=fe — finds all nginx pods and applies the tier label. It filters first, then labels.

**Visual scenes:**
1. (0–10s) URL breakdown: raw API query string decoded piece by piece
2. (10–30s) Terminal animation: kubectl get pods -l environment=production — matching pods appear in the output table
3. (30–50s) kubectl get pods -l 'environment in (production, qa)' — two groups shown in output
4. (50–65s) kubectl get pods -Lapp -Ltier -Lrole — output table with label columns animates in
5. (65–80s) kubectl label pods -l app=nginx tier=fe — before/after label state on pods
6. (80–90s) "Labels = API-first querying. Not decoration." callout text

---

## Segment 5 — Field Selectors + Outro (70–80s)

**File:** `seg5_field_selectors.html`
**Script (~185 words, ~74s narration):**

> One more selector type worth knowing: field selectors. These filter objects by resource field values — not labels.
>
> Where label selectors query user-defined metadata, field selectors query the object's actual spec and status fields.
>
> The syntax is similar: kubectl get pods --field-selector status.phase=Running. That returns only pods currently in the Running phase.
>
> All resource types support metadata.name and metadata.namespace as field selector targets. Other fields vary by type — Pods expose spec.nodeName, status.phase, spec.restartPolicy and a handful of others. Services expose spec.clusterIP. Secrets expose type.
>
> The operators are the same three: equals, double-equals, and not-equals. You can chain multiple with commas for AND — same as label selectors.
>
> You can also target multiple resource types at once. kubectl get statefulsets,services --all-namespaces --field-selector metadata.namespace!=default — returns both resource kinds, filtered to non-default namespaces only.
>
> Labels vs field selectors: use labels for your own organizational metadata and to drive controllers and services. Use field selectors when you need to filter on actual runtime state — phase, node, namespace.
>
> Next episode: Namespaces and Names — how Kubernetes scopes and identifies every object in the cluster. See you there.

**Visual scenes:**
1. (0–12s) "Field Selectors" heading, kubectl --field-selector command in terminal
2. (12–30s) Table: resource types and their supported field selector fields
3. (30–45s) Demo: kubectl get pods --field-selector status.phase=Running — pods filtered by actual state
4. (45–60s) Comparison diagram: "Labels" (left, user metadata, drives controllers) vs "Field Selectors" (right, runtime state, debug queries)
5. (60–70s) "Next: Namespaces & Names — ep14" outro card with ep number badge

---

## Production Notes

- TTS: Kokoro bm_george, speed 1.0
- All segments target 90fps-locked animation at 30fps
- Accent color: #61dafb (K8s blue)
- Background: #0d0d1a
- Font: JetBrains Mono
- Episode label: "kubernetes · labels & selectors · ep 13"
