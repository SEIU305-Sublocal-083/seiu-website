(() => {
  const countdown = document.querySelector('[data-strike-countdown]');
  if (!countdown) return;

  // The explicit Pacific offset keeps the deadline identical in every viewer's timezone.
  const start = Date.parse(countdown.querySelector('time[datetime]')?.dateTime);
  if (!Number.isFinite(start)) return;

  const digits = countdown.querySelector('[role="timer"]');
  const heading = countdown.querySelector('[data-countdown-heading]');
  const status = countdown.querySelector('[data-countdown-status]');
  const message = countdown.querySelector('[data-countdown-message]');
  const toggle = countdown.querySelector('[data-countdown-toggle]');
  const units = ['days', 'hours', 'minutes', 'seconds'];
  let paused = false;
  let interval;

  function render() {
    if (paused) return;
    const remaining = Math.max(0, Math.ceil((start - Date.now()) / 1000));
    if (remaining === 0) {
      // A deadline alone cannot establish that a strike actually went ahead.
      countdown.dataset.state = 'elapsed';
      heading.textContent = 'Scheduled start time reached';
      status.textContent = 'Check the latest update';
      message.textContent = 'Follow our union’s latest update for strike status and instructions.';
      message.hidden = false;
      digits.hidden = true;
      toggle.hidden = true;
      clearInterval(interval);
      return;
    }

    const values = [
      Math.floor(remaining / 86400),
      Math.floor((remaining % 86400) / 3600),
      Math.floor((remaining % 3600) / 60),
      remaining % 60,
    ];
    countdown.dataset.state = 'running';
    units.forEach((unit, index) => {
      countdown.querySelector(`[data-countdown-unit="${unit}"]`).textContent = String(values[index]).padStart(2, '0');
    });
    digits.setAttribute('aria-label', values.map((value, index) => `${value} ${units[index]}`).join(', ') + ' until the intended strike start');
    heading.textContent = 'Strike starts in';
    digits.hidden = false;
    toggle.hidden = false;
  }

  toggle.addEventListener('click', () => {
    paused = !paused;
    countdown.dataset.paused = String(paused);
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.textContent = paused ? 'Resume countdown' : 'Pause countdown';
    if (paused) heading.textContent = 'Countdown paused';
    else render();
  });
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) render();
  });

  render();
  if (countdown.dataset.state !== 'elapsed') interval = setInterval(render, 1000);
})();
