# Mailchimp Segment Strategy

This playbook defines how Local 083 should treat the main Mailchimp audience segments in campaign planning.

## Segment Roles

### Broad member list
- Purpose: inform, orient, invite, and recap.
- Typical content: event details, union updates, newsletters, reminders, and recap emails.
- Message style: clear context first, then the CTA.
- Default use: the standard version of a campaign.

### Engaged subscribers
- Purpose: mobilize, recruit, escalate, and close the loop.
- Typical content: turnout asks, petitions, volunteer asks, rapid-response actions, survey completion, and recruit-a-coworker asks.
- Message style: action-first, deadline-aware, and specific about what we need members to do next.
- Cadence: roughly the same as the broad list, but with more action-oriented versions of the same campaign.
- Default use: the mobilization version of a campaign.

### Disengaged subscribers
- Purpose: reactivate, simplify, and protect list quality.
- Typical content: re-engagement sends, one-thing-to-know updates, preference resets, and major-moment-only sends.
- Message style: short, relevant, and low-friction. Start with value, not guilt.
- Cadence: lower than the broad list. Do not include in every general campaign by default.
- Default use: the reactivation or low-frequency version of a campaign.

## Same-Campaign Versioning

For the same campaign, build the audience versions this way:

- Broad member list: standard version with context, logistics, and invitation.
- Engaged subscribers: action version with urgency, a stronger CTA, and a higher-commitment ask.
- Disengaged subscribers: shortened version with one relevance hook and one low-friction CTA.

## Engaged Subscriber Rules

- Lead with the action, not the background.
- Use stronger subject lines and buttons such as `RSVP now`, `Take action today`, `Help fill the room`, and `Bring one coworker`.
- Ask for higher-commitment actions than the broad list gets.
- Include secondary asks when useful:
  `bring one coworker`, `reply if you can help`, `forward this to a colleague`, `help fill your department`.
- Send follow-up or results emails after actions so the segment stays in an organizer pipeline.
- Judge success by action metrics, not just opens:
  click rate, RSVP completion, petition signatures, volunteer conversions, and reply rate.

## Disengaged Subscriber Rules

- Reduce volume. Do not send every newsletter or reminder by default.
- Use one clear message and one clear CTA per email.
- Start with low-friction actions:
  `Read this update`, `Keep me subscribed`, `Update preferences`, `See details`.
- Use "best of" or "most important update" framing instead of full campaign volume.
- Avoid punitive or guilt-based language.
- Judge success by reactivation and list quality:
  reactivation rate, unsubscribe rate, spam complaints, and downstream engagement after reactivation.

## Disengaged Sunset Flow

### Step 1: Re-engagement
- Goal: win attention back with value.
- Recommended framing:
  `Still want updates from SEIU Local 083?`
  `The most important union update this month`
  `One thing to know this week`

### Step 2: Confirmation or preference reset
- If Step 1 gets no engagement, send one final confirmation-style email.
- Recommended CTAs:
  `Stay on the list`
  `Update preferences`

### Step 3: Suppress or downgrade frequency
- If Step 2 still gets no engagement, suppress from regular campaigns or move into a low-frequency segment.

### Step 4: Major moments only
- Optionally reintroduce this segment only for high-value campaigns such as bargaining, voting, or contract campaigns.

## Segment-Specific Examples

### Membership meeting
- Broad member list: `Join the membership meeting on April 16.`
- Engaged subscribers: `Help us pack the room. RSVP and bring one coworker.`
- Disengaged subscribers: `One upcoming union meeting to know about.`

### Petition
- Broad member list: share the issue, context, and link.
- Engaged subscribers: `We need 25 more signatures by Thursday. Add your name today.`
- Disengaged subscribers: `A quick update and one action you can take in under a minute.`

### Rally
- Broad member list: event logistics and why it matters.
- Engaged subscribers: `Can you attend, volunteer, or help fill your department?`
- Disengaged subscribers: `The most important bargaining event coming up.`

### Newsletter or digest
- Broad member list: full recap or digest.
- Engaged subscribers: `3 things we need this week`
- Disengaged subscribers: `The one update we do not want you to miss`

## Subject Line Guidance

### Engaged subscribers
- Use urgency, deadlines, collective power, and concrete asks.
- Good patterns:
  `RSVP now`
  `Help fill the room`
  `Take action today`
  `We need 25 more signatures by Thursday`

### Disengaged subscribers
- Use relevance, clarity, and curiosity without sounding punitive or desperate.
- Good patterns:
  `Still want union updates?`
  `A quick update from SEIU Local 083`
  `One thing to know this week`
  `Choose the updates you want`

## Testing Expectations

- Engaged tests should focus on:
  stronger CTA, deadline-based subject line, recruit-one-coworker ask.
- Disengaged tests should focus on:
  re-engagement subject line, "most important update" format, preference-update CTA.
- Review disengaged unsubscribes and spam complaints after each send before continuing the sunset flow.

## Working Assumptions

- `Engaged subscribers` and `Disengaged subscribers` are behavioral Mailchimp segments based on recent opens or clicks.
- The engaged segment is for organizing and turnout.
- The disengaged segment is for reactivation or cleaner list quality.
- Segment differences should come from message type and commitment level more than sharp increases in frequency.
