# Security Rules

Security is part of code quality. Apply these rules to any change that touches secrets, authentication, user input, rendering, storage, network calls, or dependencies, and mention relevant security verification in the final response.

## Secrets And Configuration

- Do not expose secrets, tokens, API keys, credentials, or private keys in code, logs, URLs, client bundles, or documentation.
- Treat any value shipped to the client as public; keep server-only secrets behind server-only boundaries.
- Only client-safe values may use client-exposed env prefixes (for example `NEXT_PUBLIC_`, `VITE_`); never put server secrets behind them.
- Read secrets from environment or a secret manager, not hard-coded literals.
- Do not commit `.env` files or credential fixtures; keep them ignored.

## Untrusted Input And Rendering

- Treat all user, URL, query, storage, and third-party data as untrusted.
- Avoid raw HTML injection sinks such as `dangerouslySetInnerHTML`, `innerHTML`, and `document.write`; render text as data instead.
- When rendering untrusted markup is unavoidable, sanitize it with a vetted sanitizer and a strict allowlist.
- Do not build URLs, redirects, `href`, or `src` from untrusted input without validating the scheme; block `javascript:` and other active schemes.
- Validate and narrow external input at the boundary before using it, and prefer schema validation for parsed payloads.

## Authentication And Access Control

- Keep authentication, authorization, role, tenant, and permission assumptions explicit when changing protected flows.
- Do not rely on client-side checks for security decisions; treat the server as the source of truth.
- Never trust client-provided identifiers for ownership; scope data access to the authenticated principal.
- Keep redirect targets after login or logout on an allowlist to avoid open redirects.

## Storage And Transport

- Do not store sensitive tokens in `localStorage` or `sessionStorage` unless the architecture explicitly requires it and the risk is understood.
- Prefer secure, HTTP-only cookies for session tokens when the backend supports it.
- Use HTTPS for all network calls and external resources.
- Set cookie security attributes (`Secure`, `HttpOnly`, `SameSite`) appropriately when the code controls them.

## Logging And Error Exposure

- Avoid logging sensitive request, response, session, token, or user data.
- Do not surface stack traces, internal identifiers, or backend error details to end users.
- Keep error messages actionable for users without leaking system internals.

## Dependencies And Supply Chain

- Review dependency additions and package scripts for supply-chain, bundle, and security implications.
- Prefer maintained, widely used packages over unmaintained or low-trust alternatives for security-sensitive work.
- Avoid loading scripts from untrusted origins; pin and verify third-party sources when they are required.
- Keep Content Security Policy and related headers intact; do not loosen them to make code work.

## Verification

- Include security verification when changing auth, permissions, secret handling, external input parsing, rendering of untrusted data, redirects, downloads, uploads, or dependency boundaries.
- Confirm no secret or sensitive value is exposed in the diff, logs, or client bundle.
- State which security-relevant checks were performed in the final response.
