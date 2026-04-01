# Episode 03: Writing Markup with JSX

Intro silence: 2.0s

## Sentences

1. "JSX is how React lets you write HTML-like markup inside JavaScript. Most React developers use it every day."
2. "Traditionally, web developers kept HTML, CSS, and JavaScript in separate files."
3. "But as apps got more interactive, logic started controlling the markup. JavaScript decided what HTML to show."
4. "React embraces this. In React, rendering logic and markup live together in the same component."
5. "A sidebar component contains both the layout markup and the logic that controls it."
6. "This isn't HTML though. It's JSX — a syntax extension for JavaScript that looks like HTML but has stricter rules."
7. "JSX and React are separate things. JSX is the syntax, React is the library. You can use them independently."
8. "Let's convert some HTML to JSX. Here's valid HTML: an h1, an image tag, and a list."
9. "If you paste this directly into a React component, it won't work. JSX has three rules you need to follow."
10. "Rule one: return a single root element. You can't return multiple tags side by side."
11. "Wrap everything in a div. Or better yet, use a Fragment — that's the empty angle bracket syntax."
12. "Fragments group elements without adding extra nodes to the DOM. No leftover divs in your HTML."
13. "Rule two: close all tags. In HTML, image tags and br tags can be left open. In JSX, every tag must close."
14. "img becomes img slash. li needs a closing li tag. br becomes br slash. No exceptions."
15. "Rule three: camelCase your attributes. class becomes className. stroke-width becomes strokeWidth."
16. "Why? Because JSX compiles to JavaScript objects, and JavaScript doesn't allow dashes in property names."
17. "There are two exceptions: aria dash attributes and data dash attributes keep their dashes. Everything else is camelCase."
18. "Don't memorize every attribute. React will tell you in the console when you get one wrong."
19. "Let's recap. JSX lets you write markup inside JavaScript, because logic and markup belong together."
20. "Three rules: one root element, close every tag, camelCase attributes."
21. "Fragments avoid extra wrapper divs. className replaces class. And React's error messages guide you."
22. "Next up: JavaScript in JSX with curly braces."

Outro: 4.0s silence
