# Episode 02: Importing and Exporting Components

Intro silence: 2.0s

## Sentences

1. "Components are powerful because they're reusable. But as your app grows, you need to split them across files."
2. "Right now, everything lives in one file — the root component file. Usually called App.js."
3. "App.js is where your app starts. It's the top of the component tree."
4. "But putting every component in one file gets messy fast. Time to split them up."
5. "Moving a component to its own file takes three steps."
6. "Step one: create a new file. Step two: export the component from that file. Step three: import it where you need it."
7. "There are two ways to export: default exports and named exports."
8. "A default export uses the keyword default. A file can only have one."
9. "Export default function Gallery — that makes Gallery the main thing this file provides."
10. "To import a default export, write import Gallery from Gallery.js. No curly braces."
11. "Here's the key: with default imports, you can rename freely. Import Banana from Gallery.js works."
12. "Named exports are different. No default keyword. Just export function Profile."
13. "To import a named export, you must use curly braces: import Profile in curly braces from Gallery.js."
14. "With named imports, the name must match exactly. That's why they're called named imports."
15. "So when do you use each? Default exports for the main component. Named exports for everything else in the file."
16. "A single file can mix both. Gallery.js can have a default Gallery export and a named Profile export."
17. "App.js then imports both: import Gallery from Gallery.js, and import Profile in curly braces from Gallery.js."
18. "One rule: a file can have at most one default export, but as many named exports as you want."
19. "Some teams pick one style and stick with it. Either all default, or all named. Both work."
20. "The important thing: always give your components meaningful names. No anonymous arrow functions as exports."
21. "Let's recap. Root component file: where your app starts, usually App.js."
22. "Three steps to move a component: create file, export, import."
23. "Default exports: one per file, import without braces, can rename."
24. "Named exports: unlimited per file, import with braces, name must match."
25. "Next up: writing markup with JSX."

Outro: 4.0s silence
