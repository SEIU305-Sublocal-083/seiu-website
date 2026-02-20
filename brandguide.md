# SEIU Local 503 at Oregon State University - Web Brand Book

This guide is the operational standard for writing, designing, drafting, and publishing Local 083 web content.

## 1) Union Voice Standard

### Core rule
Always speak as **our union**. Never describe the union as a separate outside group.

### Required framing
- Use: "our union," "we," "us," "our members," "our bargaining team."
- Center member agency and collective action.
- Use direct, plain language and clear next steps.

### Do/Don't examples
- Do: "Our union is bargaining for fair wages and stronger workplace protections."
- Do: "We won this because members showed up."
- Don't: "The union is bargaining for employees."
- Don't: "The union says members should attend."

### Voice traits
- Empowering: make clear what members can do now.
- Unified: emphasize solidarity and shared ownership.
- Clear and direct: avoid vague or technical wording when plain wording works.
- Supportive: assume members are busy and need practical guidance.
- Credible: use specific dates, facts, and commitments.

### Page-type voice patterns
- Event pages: practical logistics first, then why attending matters for our union.
- News pages: clear update + impact on members + explicit action.
- Resource pages: rights-first, step-by-step, reusable language.
- About/evergreen pages: who we are, how our union is member-run, how to participate.

### Copy examples
- Headline: "Our Union Bargaining Update: Member Actions This Week"
- CTA: "Join Our Membership Meeting"
- Bargaining update lead: "Our bargaining team met with management on [date] and pushed proposals on wages, workload, and safety."
- Event promo: "Wear purple so management sees our union's strength across campus."
- Spotlight lead: "Meet a member helping build our union at OSU."

## 2) Web Style System

Use the existing implementation as source of truth.

### Color tokens (CSS vars)
- `--brand-purple-dark: #4C1D95`
- `--brand-purple: #7C3AED`
- `--brand-purple-light: #EDE9FE`
- `--brand-dark: #111827`
- `--brand-light: #F9FAFB`
- `--text-primary: #1F2937`
- `--text-secondary: #374151`
- `--border-color: #D1D5DB`

### Typography
- Headings: `Lora`, serif
- Body/UI text: `Inter`, sans-serif

### Layout patterns
- Primary content wrapper: `container mx-auto px-6`
- Use strong vertical rhythm (`py-16`/`mt-24` style spacing)
- Sticky header + mobile menu pattern used in current templates
- Card pattern: white background, rounded corners, border, optional hover shadow
- Footer: consistent multi-column structure and quick links

### Button standards
Use the shared button classes and behavior:
- Base: `.btn` for weight, spacing, rounded corners, motion
- Primary: `.btn-primary` for main conversion action
- Secondary: `.btn-secondary` for dark-background alternatives
- Outline: `.btn-outline` for less dominant actions

Behavior expectations:
- Hover: subtle elevation/scale only
- Focus: visible focus ring (`focus-visible` outline)
- Contrast: maintain accessible text/background contrast

## 3) SEO and Publishing Standards (Required)

Production pages must include complete metadata and structured data.

### Required metadata
- `<title>` with page-specific wording
- `<meta name="description">` (target ~140-160 chars)
- Canonical URL (`<link rel="canonical">`) using final production URL
- Open Graph: `og:type`, `og:url`, `og:title`, `og:description`, `og:image`, `og:site_name`
- Twitter: `twitter:card`, `twitter:url`, `twitter:title`, `twitter:description`, `twitter:image`

### Required JSON-LD
- `Organization`
- `WebSite`
- `WebPage`
- `Event` when content is event-specific

### URL and content quality rules
- Canonical URL must match final deployed page path.
- No placeholders, TODOs, or dummy links on publish (`#`, `[LINK]`, etc.).
- Internal links and asset paths must resolve.
- Use meaningful `alt` text on content images.

### Required operational checks before publish
1. Update content index files where applicable:
   - `events/events.json` for events
   - `news/news.json` for news
2. Regenerate sitemap and update robots entry if needed:
   - `bash ./generate_sitemap.sh`
3. Run quality checks:
   - `python scripts/site_quality_check.py --strict-placeholders`
4. Confirm RSS automation expectations:
   - changes to `events/events.json` or `news/news.json` trigger `.github/workflows/rss-feeds.yml` to update:
     - `events/rss.xml`
     - `news/rss.xml`
     - `feed.xml`

## 4) Content Lifecycle

All new pages should begin as drafts in `test-pages/` and be promoted only after QA and checklist completion.

See full workflow: `DRAFTING_WORKFLOW.md`.
