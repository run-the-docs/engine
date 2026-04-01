# Hono Series — Full Coverage Plan

Based on: https://hono.dev/docs/ (llms.txt crawled 2026-04-01)

**Audience:** Web developers building APIs/apps on edge runtimes (Cloudflare Workers, Deno, Bun, Node.js)
**Angle:** "The fastest way to build for the edge" — one concept per episode, code-first

---

## Section 1: What is Hono? (3 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 01 | What is Hono? | [motivation](https://hono.dev/docs/concepts/motivation) + [web-standard](https://hono.dev/docs/concepts/web-standard) | Why Hono exists, Web Standard APIs (Request/Response/Fetch), ultra-fast + tiny | ~90s |
| 02 | Hono Routers | [routers](https://hono.dev/docs/concepts/routers) | RegExpRouter vs TrieRouter vs SmartRouter, why router choice matters for perf | ~85s |
| 03 | Middleware in Hono | [middleware](https://hono.dev/docs/concepts/middleware) | Middleware as `(c, next) => Promise<Response>`, built-in vs custom vs third-party | ~90s |

---

## Section 2: Core API (5 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 04 | Routing | [api/routing](https://hono.dev/docs/api/routing) | Path params, wildcards, grouping, `app.route()`, method chaining | ~100s |
| 05 | Context | [api/context](https://hono.dev/docs/api/context) | `c.req`, `c.res`, `c.json()`, `c.text()`, `c.html()`, environment bindings | ~95s |
| 06 | Request | [api/request](https://hono.dev/docs/api/request) | `c.req.param()`, `c.req.query()`, `c.req.json()`, `c.req.valid()` | ~90s |
| 07 | Hono Instance | [api/hono](https://hono.dev/docs/api/hono) | `new Hono()`, `app.use()`, `app.fetch()`, chaining, sub-apps | ~85s |
| 08 | Error Handling | [api/exception](https://hono.dev/docs/api/exception) | `HTTPException`, `app.onError()`, `app.notFound()`, status codes | ~85s |

---

## Section 3: Validation (2 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 09 | Validation with Zod | [guides/validation](https://hono.dev/docs/guides/validation) | `zValidator`, body/query/param validation, typed routes | ~100s |
| 10 | RPC — Type-Safe API | [guides/rpc](https://hono.dev/docs/guides/rpc) | `hc` client, end-to-end type safety, share types between server and client | ~100s |

---

## Section 4: Built-in Middleware (6 episodes — grouped by purpose)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 11 | Auth Middleware | [bearer-auth](https://hono.dev/docs/middleware/builtin/bearer-auth) + [basic-auth](https://hono.dev/docs/middleware/builtin/basic-auth) + [jwt](https://hono.dev/docs/middleware/builtin/jwt) | Bearer tokens, Basic auth, JWT verify — protecting routes | ~100s |
| 12 | CORS & CSRF | [cors](https://hono.dev/docs/middleware/builtin/cors) + [csrf](https://hono.dev/docs/middleware/builtin/csrf) | Cross-origin config, allowed origins/methods, CSRF token validation | ~90s |
| 13 | Logging & Timing | [logger](https://hono.dev/docs/middleware/builtin/logger) + [timing](https://hono.dev/docs/middleware/builtin/timing) | Request logging, Server-Timing headers, performance observability | ~80s |
| 14 | Caching | [cache](https://hono.dev/docs/middleware/builtin/cache) + [etag](https://hono.dev/docs/middleware/builtin/etag) | Cache-Control, ETag generation, CDN edge caching patterns | ~85s |
| 15 | Security Headers | [secure-headers](https://hono.dev/docs/middleware/builtin/secure-headers) | CSP, HSTS, X-Frame-Options, one-line security hardening | ~80s |
| 16 | Rate Limiting & IP | [ip-restriction](https://hono.dev/docs/middleware/builtin/ip-restriction) + [body-limit](https://hono.dev/docs/middleware/builtin/body-limit) + [timeout](https://hono.dev/docs/middleware/builtin/timeout) | IP allowlist/blocklist, payload size limits, request timeouts | ~85s |

---

## Section 5: Helpers (4 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 17 | Streaming | [helpers/streaming](https://hono.dev/docs/helpers/streaming) | `streamText()`, `streamSSE()`, server-sent events, chunked responses | ~95s |
| 18 | Cookies | [helpers/cookie](https://hono.dev/docs/helpers/cookie) | `getCookie()`, `setCookie()`, `deleteCookie()`, signed cookies | ~80s |
| 19 | WebSockets | [helpers/websocket](https://hono.dev/docs/helpers/websocket) | `upgradeWebSocket()`, message handlers, runtime support matrix | ~90s |
| 20 | JSX in Hono | [guides/jsx](https://hono.dev/docs/guides/jsx) + [helpers/html](https://hono.dev/docs/helpers/html) | Server-side JSX, `html\`\`` tagged template, components without React | ~90s |

---

## Section 6: Deploy Anywhere (5 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 21 | Cloudflare Workers | [getting-started/cloudflare-workers](https://hono.dev/docs/getting-started/cloudflare-workers) | Wrangler setup, bindings (KV/D1/R2), `c.env`, deploy | ~95s |
| 22 | Cloudflare Pages | [getting-started/cloudflare-pages](https://hono.dev/docs/getting-started/cloudflare-pages) | Pages Functions, `_worker.js`, full-stack with Pages | ~85s |
| 23 | Deno & Bun | [getting-started/deno](https://hono.dev/docs/getting-started/deno) + [getting-started/bun](https://hono.dev/docs/getting-started/bun) | Runtime adapters, `Deno.serve()`, `Bun.serve()`, same code different runtimes | ~85s |
| 24 | Node.js | [getting-started/nodejs](https://hono.dev/docs/getting-started/nodejs) | `@hono/node-server`, adapter pattern, migration from Express | ~85s |
| 25 | Next.js & Vercel | [getting-started/nextjs](https://hono.dev/docs/getting-started/nextjs) + [getting-started/vercel](https://hono.dev/docs/getting-started/vercel) | Route handlers, `handle()` adapter, API routes | ~85s |

---

## Section 7: Guides & Best Practices (3 episodes)

| # | Title | Docs Link | Key Concepts | Est. Length |
|---|-------|-----------|--------------|-------------|
| 26 | Testing Hono Apps | [guides/testing](https://hono.dev/docs/guides/testing) | `app.request()`, no server needed, testClient, mocking bindings | ~90s |
| 27 | Best Practices | [guides/best-practices](https://hono.dev/docs/guides/best-practices) | Factory pattern, large apps, controller structure, avoid globals | ~85s |
| 28 | Building a Hono Stack | [concepts/stacks](https://hono.dev/docs/concepts/stacks) | HonoX, Remix + Hono, full-stack patterns | ~90s |

---

## Coverage Summary

| Section | Episodes |
|---------|----------|
| What is Hono? | 3 |
| Core API | 5 |
| Validation | 2 |
| Built-in Middleware | 6 |
| Helpers | 4 |
| Deploy Anywhere | 5 |
| Guides | 3 |
| **Total** | **28** |

**0 published. 28 episodes for full coverage (~42 min total)**

---

## Sections Excluded

| Section | Reason |
|---------|--------|
| Third-party middleware | Too many, rapidly changing — mention in overview episode |
| All `getting-started/` runtimes individually | Combined into 2-3 deploy episodes covering major platforms |
| `helpers/ssg`, `helpers/dev`, `helpers/factory` | Niche — brief mention in best practices episode |
| API reference (`/docs/api/presets`, `/docs/api/index`) | Reference content, not conceptual |

---

## Recommended Priority Order (first 10)

1. **What is Hono?** (#01) — hook episode, why edge matters
2. **Routing** (#04) — core concept every user needs
3. **Context** (#05) — the `c` object is everything in Hono
4. **Middleware in Hono** (#03) — explains the middleware model
5. **Validation with Zod** (#09) — most searched Hono topic
6. **Auth Middleware** (#11) — immediate practical value
7. **CORS & CSRF** (#12) — every real API needs this
8. **Cloudflare Workers** (#21) — primary deployment target
9. **Error Handling** (#08) — often neglected
10. **RPC — Type-Safe API** (#10) — Hono's killer feature
