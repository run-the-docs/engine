# Episode 06: State — A Component's Memory

Intro silence: 2.0s

## Sentences

1. "Components need to remember things. The current input value, which image is showing, what's in the cart. That's state."
2. "Regular variables don't work. When React re-renders a component, local variables are created fresh every time."
3. "Two problems: local variables don't persist between renders, and changing them doesn't trigger a re-render."
4. "You need two things: a way to keep data between renders, and a way to tell React to render again."
5. "That's what useState gives you. Import it from React: import useState from react."
6. "Call it like this: const, open bracket, index comma setIndex, close bracket, equals useState, open paren, zero, close paren."
7. "useState returns an array with exactly two items. The current value, and a function to update it."
8. "The square brackets are array destructuring. You're naming the two items: index and setIndex."
9. "When you call setIndex, React stores the new value and re-renders the component with fresh data."
10. "That's the key difference. Regular variables reset on re-render. State persists."
11. "You can have multiple state variables. Each useState call is independent."
12. "const index, setIndex equals useState zero. const showMore, setShowMore equals useState false. Totally fine."
13. "Hooks are special functions that start with use. useState is a Hook. There are others: useEffect, useContext, useRef."
14. "One important rule: only call Hooks at the top level of your component. Never inside loops, conditions, or nested functions."
15. "Why? React relies on the order of Hook calls to know which state belongs to which useState call."
16. "State is local to the component. If you render the same component twice, each copy gets its own state."
17. "Changing state in one instance doesn't affect the other. They're completely independent."
18. "Let's recap. State is a component's memory — it persists between renders."
19. "useState returns a value and a setter. Calling the setter triggers a re-render."
20. "You can have multiple state variables. Each is independent."
21. "Hooks must be called at the top level. State is local to each component instance."
22. "Next up: responding to events."

Outro: 4.0s silence
