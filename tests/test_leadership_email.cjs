const assert = require('node:assert/strict');
const test = require('node:test');
const data = require('../data/leadership-email-drafts.json');
const { nextDraft, emailUrl } = require('../js/leadership-email.js');

test('30 complete, distinct drafts have an issue and supporting sources', () => {
  assert.equal(data.drafts.length, 30);
  for (const key of ['id', 'subject', 'body']) {
    assert.equal(new Set(data.drafts.map(draft => draft[key])).size, 30);
  }
  for (const draft of data.drafts) {
    assert.equal(typeof draft.id, 'string');
    assert(draft.issue);
    assert(draft.goal);
    assert.equal(draft.sourceUrls.length, 2);
    assert(!/[\[\]]/.test(draft.body), 'No fill-in prompts');
    for (const source of draft.sourceUrls) assert(draft.body.includes(source));
    assert(emailUrl(data.to, draft).length < 2400, 'Keep mailto URLs manageable');
  }
});

test('each cycle uses every draft once, including across saved state reloads', () => {
  let state;
  let last;
  for (let cycle = 0; cycle < 3; cycle += 1) {
    const seen = new Set();
    for (let i = 0; i < 30; i += 1) {
      const result = nextDraft(data.drafts, state, () => 0.4);
      assert(!seen.has(result.draft.id));
      assert.notEqual(last, result.draft.id);
      seen.add(result.draft.id);
      last = result.draft.id;
      state = JSON.parse(JSON.stringify(result.state));
    }
    assert.equal(seen.size, 30);
  }
});

test('stale or malformed saved state still produces a usable draft', () => {
  for (const state of [null, {}, { remaining: ['missing'] },
    { remaining: ['01', '01'] }, { remaining: 'bad' }]) {
    assert(nextDraft(data.drafts, state).draft);
  }
});

test('all email drafts preserve both recipients and the complete text', () => {
  for (const draft of data.drafts) {
    const url = new URL(emailUrl(data.to, draft));
    assert.equal(url.pathname, 'pres.office@oregonstate.edu,trustees@oregonstate.edu');
    assert.equal(url.searchParams.get('subject'), draft.subject);
    assert.equal(url.searchParams.get('body').replace(/\r\n/g, '\n'), draft.body);
  }
});
