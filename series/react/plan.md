# React Series — Full Coverage Plan

Based on: https://react.dev/learn (llms.txt crawled 2026-04-01)

**Length estimates:** ~90–115s per episode at Kokoro bm_george narration pace.

---

## Section 1: Describing the UI — 10 episodes ✅ COMPLETE

All 10 published. Playlist: [PLdv4kqmXd-vXCpWN_G3CDkmzGpjZIA4K8](https://www.youtube.com/playlist?list=PLdv4kqmXd-vXCpWN_G3CDkmzGpjZIA4K8)

| Ep | Title | Docs Link | YouTube | Length |
|----|-------|-----------|---------|--------|
| 01 | Your First Component | [your-first-component](https://react.dev/learn/your-first-component) | [youtu.be/qQ5uCIAF5P8](https://youtu.be/qQ5uCIAF5P8) | 180s |
| 02 | Importing and Exporting Components | [importing-and-exporting-components](https://react.dev/learn/importing-and-exporting-components) | [youtu.be/XeQM8-wRM0E](https://youtu.be/XeQM8-wRM0E) | 165s |
| 03 | Writing Markup with JSX | [writing-markup-with-jsx](https://react.dev/learn/writing-markup-with-jsx) | [youtu.be/qAcfUe5X3a8](https://youtu.be/qAcfUe5X3a8) | 174s |
| 04 | JavaScript in JSX with Curly Braces | [javascript-in-jsx-with-curly-braces](https://react.dev/learn/javascript-in-jsx-with-curly-braces) | [youtu.be/7KCZN2CMdt0](https://youtu.be/7KCZN2CMdt0) | 168s |
| 05 | Passing Props to a Component | [passing-props-to-a-component](https://react.dev/learn/passing-props-to-a-component) | [youtu.be/hTlsm55viAI](https://youtu.be/hTlsm55viAI) | 165s |
| 06 | State — A Component's Memory | [state-a-components-memory](https://react.dev/learn/state-a-components-memory) | [youtu.be/9YJpxIVBOTA](https://youtu.be/9YJpxIVBOTA) | 153s |
| 07 | Responding to Events | [responding-to-events](https://react.dev/learn/responding-to-events) | [youtu.be/x6_Hpeieaqo](https://youtu.be/x6_Hpeieaqo) | 147s |
| 08 | Conditional Rendering | [conditional-rendering](https://react.dev/learn/conditional-rendering) | [youtu.be/QfthhBdbZik](https://youtu.be/QfthhBdbZik) | 133s |
| 09 | Rendering Lists | [rendering-lists](https://react.dev/learn/rendering-lists) | [youtu.be/PwQudt1sm7o](https://youtu.be/PwQudt1sm7o) | 110s |
| 10 | Keeping Components Pure | [keeping-components-pure](https://react.dev/learn/keeping-components-pure) | [youtu.be/q-4DpHmUUxo](https://youtu.be/q-4DpHmUUxo) | 130s |

**Missing from Section 1:**

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 11 | Your UI as a Tree | [understanding-your-ui-as-a-tree](https://react.dev/learn/understanding-your-ui-as-a-tree) | Render tree vs module dependency tree, why tree shape matters, root/leaf components | ~90s |

---

## Section 2: Adding Interactivity — 7 episodes 🔲 NOT STARTED

> **Note:** ep06 (State) and ep07 (Events) technically belong here but were produced as part of our "Describing the UI" run. They are already published and adequate — no need to redo.

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| — | ~~State: A Component's Memory~~ | already covered (ep06) | — | — |
| — | ~~Responding to Events~~ | already covered (ep07) | — | — |
| 12 | Render and Commit | [render-and-commit](https://react.dev/learn/render-and-commit) | Trigger → render → commit phases, what "rendering" actually means, no DOM mutation during render | ~95s |
| 13 | State as a Snapshot | [state-as-a-snapshot](https://react.dev/learn/state-as-a-snapshot) | State is a snapshot at render time, stale closures, why setState in async looks wrong | ~100s |
| 14 | Queueing State Updates | [queueing-a-series-of-state-updates](https://react.dev/learn/queueing-a-series-of-state-updates) | Batching, updater functions `n => n+1`, React 18 automatic batching | ~95s |
| 15 | Updating Objects in State | [updating-objects-in-state](https://react.dev/learn/updating-objects-in-state) | Immutability rule, spread syntax for updates, Immer intro | ~100s |
| 16 | Updating Arrays in State | [updating-arrays-in-state](https://react.dev/learn/updating-arrays-in-state) | Avoid push/pop/splice, use map/filter/spread, nested array gotchas | ~95s |

---

## Section 3: Managing State — 7 episodes 🔲 NOT STARTED

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 17 | Reacting to Input with State | [reacting-to-input-with-state](https://react.dev/learn/reacting-to-input-with-state) | Declarative vs imperative UI, mapping UI states, state machine thinking | ~100s |
| 18 | Choosing the State Structure | [choosing-the-state-structure](https://react.dev/learn/choosing-the-state-structure) | Group related state, avoid redundant/duplicated state, avoid deep nesting | ~100s |
| 19 | Sharing State Between Components | [sharing-state-between-components](https://react.dev/learn/sharing-state-between-components) | Lifting state up, controlled vs uncontrolled components | ~95s |
| 20 | Preserving and Resetting State | [preserving-and-resetting-state](https://react.dev/learn/preserving-and-resetting-state) | Same position = preserved state, key prop to reset, component identity | ~105s |
| 21 | Extracting State into a Reducer | [extracting-state-logic-into-a-reducer](https://react.dev/learn/extracting-state-logic-into-a-reducer) | useReducer, action objects, reducer function, when to switch from useState | ~110s |
| 22 | Passing Data Deeply with Context | [passing-data-deeply-with-context](https://react.dev/learn/passing-data-deeply-with-context) | createContext, useContext, Provider, avoiding prop drilling | ~105s |
| 23 | Scaling Up with Reducer and Context | [scaling-up-with-reducer-and-context](https://react.dev/learn/scaling-up-with-reducer-and-context) | Combining useReducer + Context, dispatch via context, app-scale state | ~95s |

---

## Section 4: Escape Hatches — 8 episodes 🔲 NOT STARTED

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 24 | Referencing Values with Refs | [referencing-values-with-refs](https://react.dev/learn/referencing-values-with-refs) | useRef, ref vs state (no re-render), mutable box, when to use | ~90s |
| 25 | Manipulating the DOM with Refs | [manipulating-the-dom-with-refs](https://react.dev/learn/manipulating-the-dom-with-refs) | ref on DOM node, focus/scroll/measure, forwardRef, ref callbacks | ~95s |
| 26 | Synchronizing with Effects | [synchronizing-with-effects](https://react.dev/learn/synchronizing-with-effects) | useEffect, setup + cleanup, dependency array, external system sync | ~115s |
| 27 | You Might Not Need an Effect | [you-might-not-need-an-effect](https://react.dev/learn/you-might-not-need-an-effect) | Derived state, event handlers vs effects, common anti-patterns | ~110s |
| 28 | Lifecycle of Reactive Effects | [lifecycle-of-reactive-effects](https://react.dev/learn/lifecycle-of-reactive-effects) | Mount/update/unmount, effect lifecycle vs component lifecycle, reactive values | ~105s |
| 29 | Separating Events from Effects | [separating-events-from-effects](https://react.dev/learn/separating-events-from-effects) | useEffectEvent (experimental), event vs reactive code, reading non-reactive values | ~100s |
| 30 | Removing Effect Dependencies | [removing-effect-dependencies](https://react.dev/learn/removing-effect-dependencies) | Linter rules, moving objects/functions inside effects, useCallback | ~105s |
| 31 | Reusing Logic with Custom Hooks | [reusing-logic-with-custom-hooks](https://react.dev/learn/reusing-logic-with-custom-hooks) | Custom hook conventions (use prefix), extracting hook logic, composability | ~100s |

---

## Coverage Summary

| Section | Episodes | Published | Missing |
|---------|----------|-----------|---------|
| Describing the UI | 11 | 10 ✅ | 1 (UI as a Tree) |
| Adding Interactivity | 7 | 2 ✅ (ep06+07) | 5 |
| Managing State | 7 | 0 | 7 |
| Escape Hatches | 8 | 0 | 8 |
| **Total** | **33** | **12** | **21** |

**21 new episodes needed** to complete the React `learn/` section.

---

## Sections Not Covered (out of scope for now)

| Section | Reason |
|---------|--------|
| Quick Start / Tutorial (Tic-Tac-Toe) / Thinking in React | Introductory overviews — good as standalone shorts, not full episodes |
| Installation / Editor Setup / TypeScript / DevTools | Tooling, not concepts |
| React Compiler | Still experimental/beta; docs still evolving |
| API Reference | Reference content, not conceptual — better as a separate "API Quick Ref" series |

---

## Recommended Priority Order (next 10)

1. **Your UI as a Tree** (#11) — completes Section 1, short and foundational
2. **Render and Commit** (#12) — most misunderstood React concept
3. **State as a Snapshot** (#13) — explains stale state bugs
4. **Queueing State Updates** (#14) — batching is a React 18 key feature
5. **Sharing State Between Components** (#19) — very practical, lifting state
6. **Preserving and Resetting State** (#20) — key prop usage, often surprising
7. **Referencing Values with Refs** (#24) — useRef, natural after state
8. **Synchronizing with Effects** (#26) — useEffect is essential
9. **You Might Not Need an Effect** (#27) — prevents the most common anti-pattern
10. **Custom Hooks** (#31) — series finale, ties everything together

---

## Notes

- ep06 (State) and ep07 (Events) appear in the "Adding Interactivity" section of react.dev but were produced in our "Describing the UI" run. They cover the same content — no redo needed.
- "Updating Objects/Arrays in State" (#15, #16) could be combined into one episode if length allows.
- "Reducer + Context" (#23) is a capstone episode — produces best after both #21 and #22 are done.
- "Separating Events from Effects" (#29) covers `useEffectEvent` which is still experimental. Flag in video.
