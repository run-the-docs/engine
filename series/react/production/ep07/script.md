# Episode 07: Responding to Events

Intro silence: 2.0s

## Sentences

1. "React lets you respond to user interactions: clicks, hovers, form inputs. That's event handling."
2. "Three steps. Define a function inside your component. Add your logic. Pass it to the JSX element."
3. "onClick equals open brace, handleClick, close brace. That tells React: call this function when the button is clicked."
4. "By convention, name handlers as handle plus the event name. handleClick, handleMouseEnter, handleSubmit."
5. "You can also define handlers inline. onClick equals arrow function, alert, hello. Works the same."
6. "Critical mistake: don't call the function. onClick equals handleClick — correct. onClick equals handleClick parentheses — wrong."
7. "With parentheses, the function fires immediately during render, not on click. Pass the function, don't call it."
8. "Event handlers have access to the component's props. They're defined inside the component, so they can read everything."
9. "You can pass event handlers as props too. Parent passes onClick to a Button component. The Button attaches it to the real button."
10. "This is how design systems work. A generic Button component handles styling. The parent decides what happens on click."
11. "Name your handler props starting with on. onPlay, onClick, onSubmit. The handler function starts with handle."
12. "Events propagate up the tree. A click on a button inside a div triggers both the button's and the div's onClick."
13. "This is called bubbling. The event fires on the target, then moves up to each parent."
14. "To stop propagation, call e dot stopPropagation in your handler. The event object e is the first argument."
15. "There's also e dot preventDefault. Use it to stop the browser's default action, like a form submission refreshing the page."
16. "Let's recap. Event handlers are functions you pass to JSX elements: onClick, onChange, onSubmit."
17. "Pass functions, don't call them. No parentheses after the name."
18. "Events propagate upward. Use stopPropagation to stop bubbling, preventDefault to stop browser defaults."
19. "Next up: conditional rendering."

Outro: 4.0s silence
