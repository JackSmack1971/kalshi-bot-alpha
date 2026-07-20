---
paths:
  - "**/*.{js,mjs}"
  - "!**/*.{cjs,cts}"
---

# ES2022+ Plain Modern JavaScript (ESM + Top-Level Await) Rules

- Write every file as an ES module. Never use `require`, `module.exports`, `exports.`, or `__dirname`/`__filename` without `import.meta`.
- Prefer named exports; use `export default` only for a single clear responsibility (class/factory).
- Use top-level `await` for async initialization the module's exports depend on. Never wrap the module body in an async IIFE instead.
- Prefer `const`; use `let` only when reassignment is required. Never `var`.

**Pitfall:** circular dependencies involving top-level await make module evaluation order non-deterministic — break the cycle by moving shared initialization into a module both sides import.
