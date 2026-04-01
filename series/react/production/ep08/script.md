# Episode 08: Conditional Rendering

Intro silence: 2.0s

## Sentences

1. "Your components need to show different things depending on conditions. React handles this with plain JavaScript."
2. "Start with if statements. A function component can return different JSX based on a prop."
3. "isPacked is true? Return the item with a checkmark. isPacked is false? Return it without. Two separate return statements."
4. "You can also return null. If isPacked is true, return null — the component renders nothing. It disappears from the output."
5. "But returning null is rare. Usually you conditionally include or exclude the component from the parent instead."
6. "For inline conditions, use the ternary operator. isPacked question mark, name plus checkmark, colon, name. One expression, two outcomes."
7. "Ternaries keep your JSX compact. But don't nest them — deeply nested ternaries are hard to read."
8. "There's an even shorter pattern: logical AND. isPacked ampersand ampersand, checkmark. If isPacked is true, render the checkmark. If false, render nothing."
9. "Watch out for a common trap. If the left side is zero, React renders the number zero — not nothing. Use a boolean condition, not a number."
10. "You can also assign JSX to a variable. Let itemContent equals name. Then, if isPacked, reassign it to name plus checkmark. Return the variable in your JSX."
11. "This variable approach is the most flexible. You can mix in any logic — if, else if, switch — before your return statement."
12. "Let's recap. Use if and return for completely different JSX. Use ternary for inline either-or choices."
13. "Use logical AND for conditionally including an element. Use variables when the logic gets complex."
14. "All of this is just JavaScript. No special React syntax. That's the point."
15. "Next up: rendering lists."

Outro: 4.0s silence
