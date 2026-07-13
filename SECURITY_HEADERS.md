# Production Security Headers

The live domain is fronted by Cloudflare/GitHub Pages, so these response headers must be configured at the edge. They cannot be made effective with HTML meta tags alone.

## Enable before launch

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
X-Frame-Options: DENY
```

Start Content Security Policy in report-only mode, review reports, then enforce it:

```text
Content-Security-Policy-Report-Only: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; img-src 'self' https: data:; font-src 'self'; connect-src 'self' https://us.i.posthog.com https://us-assets.i.posthog.com; script-src 'self' 'unsafe-inline' https://us-assets.i.posthog.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; form-action 'self' https://seiu503signup.org https://seiu503.tfaforms.net; upgrade-insecure-requests
```

The temporary `'unsafe-inline'` allowances are needed because legacy public pages still contain inline styles, UI scripts and event handlers. Removing those should be a follow-up hardening project. Do not enforce a stricter policy until the report-only logs show that navigation, analytics, calendar controls and archive pages still work.

## Verification

After the Cloudflare rule is deployed, run:

```bash
curl -sSI https://www.local083.org/ | grep -Ei 'strict-transport|content-security|x-content-type|x-frame|referrer-policy|permissions-policy'
```

The web maintainer owns this configuration. Review it whenever a third-party script, form destination, analytics host or hosting provider changes, and at least quarterly.
