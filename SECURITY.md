# Security

This site is a read-only landing page: no forms, no database, no user input, no cookies.

## Hardening in place

- **Strict Content-Security-Policy**: `default-src 'none'`, no inline scripts or styles, no `eval`, only first-party JS and Google Fonts.
- **Clickjacking protection**: `frame-ancestors 'none'` + `X-Frame-Options: DENY`.
- **Other headers**: `X-Content-Type-Options: nosniff`, `Referrer-Policy`, `Permissions-Policy` (camera, mic, geolocation… disabled), `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`.
- **HSTS** when served over HTTPS (`BEHIND_HTTPS=1` behind a TLS proxy).
- **Only GET/HEAD** accepted; other methods return 405. Request bodies capped at 1 KB.
- **Generic error pages**: no stack traces, versions or paths. `Server` header removed.
- **Debug off by default**; the Werkzeug debugger only runs with `FLASK_DEBUG=1` and only on `127.0.0.1`.
- **Production server**: waitress instead of the Flask dev server; binds to `127.0.0.1` unless `HOST` is set.
- **Jinja autoescaping** on all templates (no `|safe`).
- **No email address published**: contact goes through LinkedIn, so there is nothing for scrapers to harvest.
- **Cache-busted assets** (`?v=<hash>`) so visitors always get the current JS/CSS.
- **External links** use `rel="noopener noreferrer"`.
- **Pinned dependencies**, weekly Dependabot updates, and `pip-audit` + tests in CI with read-only token permissions.
- **Static build** (`python app.py --build`) ships the CSP as `<meta>` and a `_headers` file for Netlify / Cloudflare Pages.

Note: GitHub Pages cannot send custom HTTP headers, so on Pages the CSP is delivered via `<meta>` (without `frame-ancestors`). For full header protection, host on Netlify/Cloudflare Pages (uses `_headers`) or run the Flask app.

## Reporting a vulnerability

Please open a private security advisory on this repository (Security → Advisories → Report a vulnerability).
