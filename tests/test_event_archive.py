import json
import shutil
import subprocess
import sys
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import generate_static_content as static


def event(day, slug, **extra):
    return {'date': day, 'title': slug, 'url': f'/events/{slug}.html', **extra}


class EventArchiveTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            event('2026-09-11', 'future'), event('2026-09-10', 'today'),
            event('2026-09-09', 'recent'), event('2026-08-27', 'workshop'),
            event('2026-08-26', 'workshop'), event('2026-08-23', 'council'),
            event('2026-08-20', 'older'),
            event('2026-09-08', 'ongoing', schema_end_date='2026-09-12T17:00:00-07:00'),
            event('2026-02-30', 'bad-date'),
            event('2026-09-09', 'bad-link', url='javascript:alert(1)'),
            None,
        ]

    def test_newest_three_unique_pages_exclude_today_future_and_ongoing_events(self):
        chosen = static.past_events(self.items, datetime(2026, 9, 10))
        self.assertEqual([item['title'] for item in chosen], ['recent', 'workshop', 'council'])

    def test_empty_archive_and_untrusted_text(self):
        self.assertIn('No past events', static.render_past_events([], datetime(2026, 9, 10)))
        rendered = static.render_past_events([
            event('2026-09-09', 'safe', title='<img src=x onerror=alert(1)>', location_detail='A & B'),
        ], datetime(2026, 9, 10))
        self.assertNotIn('<img', rendered)
        self.assertIn('&lt;img', rendered)
        self.assertIn('A &amp; B', rendered)

    @unittest.skipUnless(shutil.which('node'), 'Node is needed to test browser archive logic')
    def test_browser_matches_fallback_and_uses_pacific_midnight(self):
        script = '''
const fs = require('node:fs');
const archive = require('./js/event-archive.js');
const events = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify({
    selected: archive.selectPastEvents(events, '2026-09-10').map(e => e.url),
    before: archive.pacificDate(new Date('2026-09-10T06:59:59Z')),
    after: archive.pacificDate(new Date('2026-09-10T07:00:00Z')),
    empty: archive.renderPastEvents([], '2026-09-10'),
    escaped: archive.renderPastEvents([{date:'2026-09-09',title:'<img src=x>',url:'/events/safe.html'}], '2026-09-10')
}));
'''
        result = json.loads(subprocess.check_output(['node', '-e', script], input=json.dumps(self.items), text=True, cwd=ROOT))
        self.assertEqual(result['selected'], [e['url'] for e in static.past_events(self.items, datetime(2026, 9, 10))])
        self.assertEqual(result['before'], '2026-09-09')
        self.assertEqual(result['after'], '2026-09-10')
        self.assertIn('No past events', result['empty'])
        self.assertNotIn('<img', result['escaped'])
        self.assertIn('&lt;img', result['escaped'])


if __name__ == '__main__':
    unittest.main()
