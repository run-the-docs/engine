# Episode 05: Passing Props to a Component

Intro silence: 2.0s

## Sentences

1. "React components communicate through props. Parents pass data down to children — that's the flow."
2. "You already know props. Every HTML attribute is a prop: className, src, alt, width, height."
3. "But your custom components can accept any props you define. That's what makes them configurable."
4. "Passing props happens in two steps. Step one: pass them from the parent. Step two: read them in the child."
5. "In the parent: Avatar, person equals open brace, the object, close brace, size equals open brace, 100, close brace."
6. "In the child: function Avatar, open paren, open brace, person comma size, close brace, close paren."
7. "That's destructuring. You're unpacking the props object into named variables."
8. "You can also write it as function Avatar props, then use props dot person and props dot size. Same result."
9. "Props are like function arguments. React components are functions, and props are the single argument they receive."
10. "Default values are easy. size equals 100 in the destructuring means: if no size prop is passed, use 100."
11. "One catch: null and zero are not missing. Default values only kick in for undefined or absent props."
12. "Sometimes you forward all props from parent to child. The spread syntax does that: Avatar, dot dot dot props."
13. "But use spread sparingly. If you use it everywhere, your components are probably too tangled."
14. "Now the powerful one: children. When you nest JSX inside a component, it arrives as a prop called children."
15. "Card, open angle bracket, Avatar, close. Card receives Avatar as its children prop."
16. "The Card component renders open brace children close brace inside a wrapper div. It doesn't need to know what's inside."
17. "Think of children as a slot. The parent fills it, the child renders it. Panels, grids, layouts — all use this pattern."
18. "Props are read-only. A component never modifies its own props. It reads them and renders accordingly."
19. "If something needs to change over time, that's state — the next topic."
20. "Let's recap. Props flow from parent to child — one direction only."
21. "Destructure them in the function signature. Set defaults with equals."
22. "Use children for flexible wrappers. Never mutate props."
23. "Next up: state — a component's memory."

Outro: 4.0s silence
