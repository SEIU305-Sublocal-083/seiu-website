# Local 083 Mailchimp email templates

These four templates are separate, production-ready starting points for short Local 083 emails. They preserve the familiar structure members already recognize: a pale-purple header, concise copy, one clear purple action button and a quiet compliance footer.

The browser gallery is [`index.html`](./index.html). Open each template directly before copying its HTML into Mailchimp.

## Which template to use

### 1. Classic + Status

File: [`classic-status.html`](./classic-status.html)

Use for bargaining updates, proposal summaries and meeting invitations where members need the stakes immediately. Its signature element is the compact **At a glance** strip.

Good examples:

- A new economic proposal
- A short bargaining report
- An invitation tied to an urgent contract issue

### 2. Classic + Agenda

File: [`classic-agenda.html`](./classic-agenda.html)

Use for membership meetings, trainings and other events where logistical certainty matters. Its signature elements are the **When / Where / Food** details table and the three-row **What we'll cover** agenda.

Good examples:

- General membership meetings
- CAT meetings
- Steward trainings
- New employee orientation

### 3. Classic + Alert

File: [`classic-alert.html`](./classic-alert.html)

Use when one important fact has changed or needs immediate attention. Its signature element is the gold alert strip above the familiar header.

Good examples:

- Room or time changes
- Day-of reminders
- Deadlines
- Cancellations or late-breaking updates

Keep the alert to one short fact. If everything is highlighted, nothing is highlighted.

### 4. Classic + Member Voice

File: [`classic-member-voice.html`](./classic-member-voice.html)

Use when a common coworker question or member experience provides the clearest entry point. Its signature element is the compact purple question block.

Good examples:

- Explaining a COLA, step or contract proposal
- Answering a recurring workplace question
- Introducing a member story
- Connecting bargaining language to a worker's day-to-day life

Use an attributed quote only with the speaker's permission. A clearly labeled common or composite question can be used without naming a person.

## Combining elements

The modules are intentionally table-based and can be copied between templates. Keep the overall email short and normally use no more than **two signature modules**.

| Combination | Best use | Guidance |
| --- | --- | --- |
| Status + Agenda | Bargaining meeting | Put Status first, then event details or Agenda. Avoid repeating the same facts in the body. |
| Alert + Agenda | Changed meeting details | Put Alert first. Use the details table for the full confirmed information. |
| Alert + Member Voice | Urgent action explained through a worker question | Keep the alert factual and the question human. Use only one CTA. |
| Status + Member Voice | Proposal explainer | Lead with the question, then use Status to summarize the verified numbers. |
| Details + Member Voice | Training or rights meeting | Use the question to explain why the event matters, followed by logistics. |

Avoid stacking Alert, Status, Agenda and Member Voice in one message. That makes a quick email feel like a newsletter and weakens the primary action.

## Elements that should stay consistent

- One clear subject line and hidden preview text
- One primary headline
- Short paragraphs written for scanning
- One primary purple CTA
- Verified dates, times, rooms and bargaining claims
- `Lora, Georgia, serif` for display headings
- `Inter, Helvetica, Arial, sans-serif` for body copy
- A maximum email width of 600 pixels
- Table-based layout and inline styles for email-client compatibility
- Descriptive link text instead of “click here”

## Mandatory Mailchimp footer variables

**Do not remove or replace the footer when combining templates.** Every saved template includes the following Mailchimp merge tags:

```text
*|ARCHIVE|*
*|UPDATE_PROFILE|*
*|UNSUB|*
*|LIST:ADDRESS|*
*|IF:REWARDS|**|HTML:REWARDS|**|END:IF|*
```

Their purposes are:

- `*|ARCHIVE|*` — hosted “view online” version
- `*|UPDATE_PROFILE|*` — subscriber preference link
- `*|UNSUB|*` — required unsubscribe link
- `*|LIST:ADDRESS|*` — the mailing list's physical postal address
- `*|IF:REWARDS|**|HTML:REWARDS|**|END:IF|*` — conditionally displays Mailchimp's referral badge when required by the account plan

The permission reminder must also remain:

> You are receiving this email because you subscribed to Local 083 updates.

When building a new message, copy the complete footer from one of these files rather than reconstructing it. Confirm that the Mailchimp campaign preview renders the physical address, unsubscribe link and preference link before sending.

## Safe editing checklist

1. Duplicate the closest template; do not overwrite the reusable original.
2. Update the subject and preview-text comments near the top of the HTML.
3. Update the hidden preheader text inside the `<body>`.
4. Replace the headline, body, date and CTA destination.
5. Remove any module that does not help the email's single purpose.
6. Preserve the entire footer and every merge tag listed above.
7. Send a Mailchimp test to desktop and mobile inboxes.
8. Check links, names, dates, rooms, spelling and accessibility before scheduling.
