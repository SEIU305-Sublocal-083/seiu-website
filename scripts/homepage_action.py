"""Render the homepage campaign from the same data used by its browser update."""

import html
import json


def esc(value):
    return html.escape(str(value), quote=True)


def cta(action, position, style):
    item = next(item for item in action["ctas"] if item["id"] == position)
    analytics = item.get("analytics", {})
    return (f'<a class="btn {style}" href="{esc(item["href"])}" data-action-{position}'
            f' data-ph-event="{esc(analytics.get("event", "take_action_click"))}"'
            f' data-ph-label="{esc(analytics.get("label", item["label"]))}"'
            f' data-ph-metadata="{esc(json.dumps(analytics.get("metadata", {})))}">{esc(item["label"])}</a>')


def render_hero(action):
    clock = action["strikeClock"]
    inactive = clock["status"] != "confirmed"
    headline = clock.get("resolutionHeadline", "STRIKE UPDATE") if inactive else action["headline"]
    summary = clock.get("resolutionMessage", "Read our union’s latest instructions before reporting to work or a picket line.") if inactive else action["summary"]
    image = action["image"]
    config = json.dumps({"clock": clock, "headline": action["headline"], "summary": action["summary"]}, ensure_ascii=False).replace("<", "\\u003c")
    details = "\n".join(f'<div><dt>{esc(item["label"])}</dt><dd>{esc(item["value"])}</dd></div>' for item in action["details"])
    hidden = ' hidden' if inactive else ''
    return f'''        <div class="container mx-auto px-6 home-strike-inner">
            <div class="home-strike-grid">
                <div class="home-strike-copy">
                    <p class="home-strike-union">SEIU Local 503 at Oregon State University · Local 083</p>
                    <p class="home-strike-eyebrow" data-action-eyebrow>{esc(action["eyebrow"])}</p>
                    <h1 class="home-strike-title" data-action-headline>{esc(headline)}</h1>
                    <p class="home-strike-summary" data-action-summary>{esc(summary)}</p>
                    <div class="home-strike-ctas" data-strike-mobilization{hidden}>
                        {cta(action, "primary", "btn-primary")}
                        {cta(action, "secondary", "btn-secondary")}
                    </div>
                    <p class="home-strike-update"><a href="{esc(clock['updateUrl'])}" data-strike-update-link>Read our union’s latest strike instructions →</a></p>
                </div>
                <div class="home-strike-visual">
                    <section class="home-strike-clock" data-home-strike-clock aria-labelledby="home-strike-clock-title">
                        <p class="home-strike-clock-kicker" data-home-clock-status>{'Latest union update' if inactive else 'The strike begins at 6 a.m.'}</p>
                        <h2 id="home-strike-clock-title" data-home-clock-heading>{'Strike status updated' if inactive else 'Countdown to strike'}</h2>
                        <div class="home-strike-digits" role="timer" aria-live="off" hidden>
                            <div><strong data-home-clock-unit="days">00</strong><span>Days</span></div>
                            <div><strong data-home-clock-unit="hours">00</strong><span>Hours</span></div>
                            <div><strong data-home-clock-unit="minutes">00</strong><span>Minutes</span></div>
                            <div><strong data-home-clock-unit="seconds">00</strong><span>Seconds</span></div>
                        </div>
                        <p class="home-strike-date"><span data-home-clock-date-label>Strike start:</span> <time datetime="{esc(clock['startsAt'])}">{esc(clock['startLabel'])}</time></p>
                        <p class="home-strike-clock-message" data-home-clock-message>{esc(summary) if inactive else 'Management: settle a fair contract.'}</p>
                        <noscript><p>The live timer needs JavaScript. Use the strike page for the latest status and instructions.</p></noscript>
                    </section>
                    <figure class="home-strike-photo"><img src="{esc(image['src'])}" alt="{esc(image['alt'])}" width="{image['width']}" height="{image['height']}" decoding="async" fetchpriority="high" data-action-image><figcaption>Our work makes OSU work. Our solidarity makes us strong.</figcaption></figure>
                </div>
            </div>
            <dl class="home-strike-details" data-action-details data-strike-mobilization{hidden}>{details}</dl>
        </div>
        <script type="application/json" id="homepage-strike-config">{config}</script>'''


def render_promo(action):
    hidden = ' hidden' if action["strikeClock"]["status"] != "confirmed" else ''
    return f'''        <div class="container mx-auto px-6 home-strike-promo" data-strike-mobilization{hidden}>
            <div><p class="home-strike-promo-kicker" data-action-promo-eyebrow>{esc(action['promoEyebrow'])}</p><h2 data-action-promo-headline>{esc(action['promoHeadline'])}</h2><p data-action-promo-body>{esc(action['promoBody'])}</p></div>
            {cta(action, 'tertiary', 'btn-secondary')}
        </div>'''
