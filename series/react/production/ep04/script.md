# Episode 04: JavaScript in JSX with Curly Braces

Intro silence: 2.0s

## Sentences

1. "JSX lets you write markup inside JavaScript. But sometimes you need JavaScript inside that markup."
2. "Curly braces are the escape hatch. They open a window from JSX back into JavaScript."
3. "Start simple. String attributes use quotes: src equals quote, URL, quote. That's a fixed string."
4. "But what if the URL comes from a variable? Replace the quotes with curly braces: src equals open brace, avatar, close brace."
5. "Now React reads the avatar variable instead of a literal string. That's the core idea."
6. "Any JavaScript expression works inside curly braces. Variables, function calls, math — anything that produces a value."
7. "Here's a function call: open brace, formatDate, parentheses, today, close brace. React runs the function and inserts the result."
8. "Where can you use curly braces? Two places only."
9. "First: as text inside a JSX tag. Open brace, name, close brace — renders the variable as text content."
10. "Second: as an attribute value, right after the equals sign. src equals open brace, avatar, close brace."
11. "You cannot use curly braces for tag names. Open angle bracket, open brace, tag, close brace won't work."
12. "Now for the confusing part: double curly braces. They look special, but they're not."
13. "The outer braces say: this is JavaScript. The inner braces say: this is a JavaScript object."
14. "You see this most with inline styles. style equals open brace, open brace, backgroundColor colon black, close brace, close brace."
15. "The first brace enters JavaScript. The second brace is just an object literal. That's all double curlies are."
16. "Remember: inline style properties use camelCase too. backgroundColor, not background-color. fontSize, not font-size."
17. "You can also extract data into an object variable. person dot theme for styles, person dot name for text."
18. "This keeps your JSX clean. All the data lives in one place, and curly braces reference it."
19. "Let's recap. Curly braces are your escape hatch from JSX into JavaScript."
20. "Quotes for fixed strings. Curly braces for dynamic values — variables, expressions, function calls."
21. "Double curlies: just an object inside curly braces. Nothing magical."
22. "Next up: passing props to a component."

Outro: 4.0s silence
