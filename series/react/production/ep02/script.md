# React — Importing and Exporting Components (ep02)

Narration script. One sentence per line for TTS timing.

As your React app grows, you'll want to split components into separate files.

Importing and exporting lets you move components around and reuse them across your project.

There are two ways to export a component: default export, and named export.

Default export is best when a file has only one main component.

Named exports are useful when you want to export multiple components or values from the same file.

Here's an example. We have a Gallery component in one file, and a Profile component in another.

In Gallery.js, we import Profile from Profile.js, then use it to create multiple profiles.

In App.js, we import Gallery, and now we can use it anywhere in our app.

The same file can have one default export and multiple named exports.

This pattern lets you organize your code logically and keep components easy to find and reuse.

Next episode: learn about Props to pass data between components.
