# Performance review

Reviewed July 12, 2026.

## Delivery changes completed

- Replaced the browser-loaded Tailwind compiler with a 47 KB compiled stylesheet (8.6 KB gzip).
- Self-hosted Inter and Lora, eliminating Google Fonts requests.
- Added responsive WebP sources for large homepage, about, bargaining, news and rally imagery.
- Added 192-pixel news thumbnails so compact lists do not download full-size artwork.
- Added intrinsic image dimensions to public pages to reduce layout shift.
- Preserved server-rendered event and news content when JSON requests fail.
- Disabled analytics autocapture, session recording and automatic page-view collection.

## Core transfer snapshot

The main HTML documents are approximately 7.6–14.5 KB gzip. The compiled Tailwind stylesheet is 8.6 KB gzip, the font declarations are 0.3 KB gzip, and the analytics loader is 3.3 KB gzip. Fonts total approximately 86 KB before HTTP compression.

## Remaining browser measurement

Run Lighthouse or WebPageTest against the deployed HTTPS URL on a production-like connection. Record mobile LCP, CLS, INP and total transfer size. This repository review cannot certify Core Web Vitals because no rendered browser was available to the task.

Targets before launch:

- LCP at or below 2.5 seconds at the 75th percentile.
- CLS at or below 0.1.
- INP at or below 200 milliseconds.
- No render-blocking third-party font or CSS compiler requests.
