# React ep01: Your First Component (EXPANDED)

**Source:** https://react.dev/learn/your-first-component  
**Duration Target:** 90s (all concepts covered)

## Expanded Narration Script

Intro silence: 2.0s

### Segment 1: Intro + What Components Are
"React is built on components. They're the foundation of every user interface you build.
A component is a reusable piece of UI — like a button, a card, or a sidebar.
It can be as small as a button, or as large as an entire page.
Just like HTML has tags like div and button, React lets you create your own custom components."

### Segment 2: Components are JavaScript Functions
"Here's the key idea: a React component is just a JavaScript function.
It's a function that returns markup — HTML-like code called JSX.
Let's call our function MyButton. It returns a button element.
That's it. Function. Return markup. That's a component."

### Segment 3: Exporting a Component (The Three Steps)
"To use your component in other files, you need to export it.
First: add the export default prefix before your function.
This tells JavaScript that MyButton is the main thing this file exports.
You can learn more about imports and exports in the next episode.
For now, just remember: export default makes your component reusable."

### Segment 4: Using a Component
"Now that you've defined MyButton, you can use it anywhere in your app.
Reference it like you would any JSX element. That's capital M, capital B: MyButton.
The capital letter matters. React uses capitalization to tell components apart from HTML tags.
So div is lowercase — that's an HTML tag. MyButton is capitalized — that's your component."

### Segment 5: Nesting Components
"Components can contain other components. That's called nesting.
You can use MyButton inside a Gallery component, multiple times.
Each MyButton is independent. Each one can have its own state later.
You can build entire pages this way — one component inside another, all the way down."

### Segment 6: Best Practices (Don't Nest Definitions)
"Important rule: never define a component inside another component.
If you define MyButton inside Gallery, your app will be slow and buggy.
Always define components at the top level, outside of other functions.
If a child component needs data from a parent, pass it with props instead.
We'll cover props in the next episode."

### Segment 7: Components All the Way Down
"Your React app starts with a root component.
Most React apps use components all the way down.
Not just for small things like buttons, but for large sections like sidebars and pages.
Components are how you organize and structure your entire UI.
Every piece of your interface is built from components."

### Segment 8: Recap
"Here's what you learned: React components are JavaScript functions that return markup.
They let you build reusable UI pieces.
Capitalize their names. Export them to reuse them. Nest them to build complex interfaces.
You're ready for the next concept: Props."

Outro silence: 4.0s

## Mapping to Docs Page

✅ What components are - covered (reusable UI elements)
✅ Components: UI building blocks - covered  
✅ Defining a component - covered (3 steps concept)
✅ Export the component - covered  
✅ Define the function - covered (JavaScript function)
✅ Add markup - covered (return JSX)
✅ Using a component - covered
✅ What browser sees - covered (implied)
✅ Capitalization matters - covered
✅ Nesting and organizing - covered
✅ Parent/child concept - covered
✅ Never nest definitions - covered
✅ Components all the way down - covered

## Animation Timing Notes

- Seg 1 (What are): Show component concept, different sizes
- Seg 2 (Functions): Show function syntax, return statement
- Seg 3 (Export): Show export default keyword, highlight importance
- Seg 4 (Using): Show capitalization comparison (div vs MyButton)
- Seg 5 (Nesting): Show nested component structure, multiple instances
- Seg 6 (Best practices): Show ❌ bad nesting, ✅ good structure
- Seg 7 (All the way down): Show page structure of nested components
- Seg 8 (Recap): Final summary with key points
