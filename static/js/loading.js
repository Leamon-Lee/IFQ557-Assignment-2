(() => {
  const page = document.querySelector('.loading-page');
  const layer = document.querySelector('.loading-ripple-layer');
  if (!page || !layer) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const target = {
    x: window.innerWidth * 0.68,
    y: window.innerHeight * 0.48
  };
  const current = { ...target };
  let animationFrame = 0;

  const render = () => {
    current.x += (target.x - current.x) * 0.13;
    current.y += (target.y - current.y) * 0.13;

    page.style.setProperty('--cursor-x', `${current.x}px`);
    page.style.setProperty('--cursor-y', `${current.y}px`);

    animationFrame = requestAnimationFrame(render);
  };

  const createPulse = (x, y) => {
    const pulse = document.createElement('span');
    pulse.className = 'loading-soft-pulse';
    pulse.style.left = `${x}px`;
    pulse.style.top = `${y}px`;
    layer.appendChild(pulse);
    pulse.addEventListener('animationend', () => pulse.remove(), { once: true });
  };

  window.addEventListener('pointermove', (event) => {
    target.x = event.clientX;
    target.y = event.clientY;
  }, { passive: true });

  window.addEventListener('pointerdown', (event) => {
    target.x = event.clientX;
    target.y = event.clientY;
    createPulse(event.clientX, event.clientY);
  }, { passive: true });

  window.addEventListener('pagehide', () => {
    cancelAnimationFrame(animationFrame);
  }, { once: true });

  render();
})();
