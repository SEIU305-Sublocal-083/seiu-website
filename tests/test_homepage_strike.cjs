const { test } = require('node:test');
const assert = require('node:assert/strict');
const { clockState } = require('../js/homepage-strike.js');
const clock = { status: 'confirmed', startsAt: '2026-09-28T06:00:00-07:00' };
const start = Date.parse('2026-09-28T13:00:00Z');

test('Pacific start counts down to the same instant in any timezone', () => {
    assert.deepEqual(clockState(clock, start - 1000), { phase: 'countdown', hour: null, values: [0, 0, 0, 1] });
    assert.deepEqual(clockState(clock, start - 1).values, [0, 0, 0, 1]);
    assert.deepEqual(clockState(clock, start - 90061000).values, [1, 1, 1, 1]);
});

test('exact start enters hour one and continues through hour and day boundaries', () => {
    assert.deepEqual(clockState(clock, start), { phase: 'active', hour: 1, values: [0, 0, 0, 0] });
    assert.equal(clockState(clock, start + 3599999).hour, 1);
    assert.deepEqual(clockState(clock, start + 3600000), { phase: 'active', hour: 2, values: [0, 1, 0, 0] });
    assert.deepEqual(clockState(clock, start + 86400000), { phase: 'active', hour: 25, values: [1, 0, 0, 0] });
    assert.equal(clockState(clock, start + 72 * 3600000).hour, 73);
});

test('resolution, pause, missing status and invalid dates never announce an active strike', () => {
    for (const status of ['resolved', 'paused', undefined, 'unexpected']) {
        for (const now of [start - 1, start, start + 86400000]) {
            assert.deepEqual(clockState({ ...clock, status }, now), { phase: 'update' });
        }
    }
    assert.deepEqual(clockState({ ...clock, startsAt: 'invalid' }, start), { phase: 'update' });
    assert.deepEqual(clockState(null, start), { phase: 'update' });
});
