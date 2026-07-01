(() => {
  const page = document.querySelector('.loading-page');
  const layer = document.querySelector('.loading-ripple-layer');
  const canvas = document.querySelector('.loading-show-canvas');
  if (!page || !layer) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const context = canvas?.getContext('2d', { alpha: true });
  const target = {
    x: window.innerWidth * 0.68,
    y: window.innerHeight * 0.48
  };
  const current = { ...target };
  const lights = [
    { x: 0.69, y: 0.02, color: [56, 189, 248], base: -0.34, swing: 0.3, speed: 0.0012, phase: 0.2, width: 0.2, length: 0.98, alpha: 0.5, blur: 18 },
    { x: 0.76, y: 0.04, color: [168, 85, 247], base: -0.18, swing: 0.34, speed: 0.001, phase: 1.8, width: 0.22, length: 0.92, alpha: 0.48, blur: 20 },
    { x: 0.84, y: 0.05, color: [34, 211, 238], base: -0.02, swing: 0.28, speed: 0.00135, phase: 3.1, width: 0.18, length: 0.88, alpha: 0.42, blur: 17 },
    { x: 0.91, y: 0.07, color: [236, 72, 153], base: 0.12, swing: 0.32, speed: 0.00108, phase: 4.4, width: 0.2, length: 0.86, alpha: 0.44, blur: 19 },
    { x: 0.98, y: 0.1, color: [245, 158, 11], base: 0.22, swing: 0.24, speed: 0.00145, phase: 2.7, width: 0.17, length: 0.84, alpha: 0.38, blur: 18 },
    { x: 0.73, y: 0.26, color: [125, 211, 252], base: -0.54, swing: 0.2, speed: 0.00158, phase: 5.2, width: 0.15, length: 0.64, alpha: 0.34, blur: 16 },
    { x: 0.82, y: 0.31, color: [244, 114, 182], base: -0.3, swing: 0.26, speed: 0.00122, phase: 3.8, width: 0.15, length: 0.58, alpha: 0.3, blur: 17 },
    { x: 0.91, y: 0.35, color: [251, 191, 36], base: 0.2, swing: 0.22, speed: 0.00172, phase: 1.3, width: 0.13, length: 0.56, alpha: 0.28, blur: 16 },
    { x: 0.63, y: 0.42, color: [59, 130, 246], base: -0.82, swing: 0.18, speed: 0.00138, phase: 2.1, width: 0.12, length: 0.44, alpha: 0.28, blur: 15 }
  ];
  const haze = Array.from({ length: 78 }, (_, index) => ({
    x: 0.42 + Math.random() * 0.62,
    y: Math.random(),
    r: 0.8 + Math.random() * 2.6,
    speed: 0.000018 + Math.random() * 0.000045,
    phase: index * 0.77,
    hue: Math.random() > 0.52 ? [56, 189, 248] : [236, 72, 153],
    alpha: 0.05 + Math.random() * 0.14
  }));

  let width = window.innerWidth;
  let height = window.innerHeight;
  let dpr = 1;
  let animationFrame = 0;

  const rgba = ([r, g, b], alpha) => `rgba(${r}, ${g}, ${b}, ${alpha})`;

  const resizeCanvas = () => {
    if (!context) return;
    dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
  };

  const drawGlow = (x, y, radius, color, alpha) => {
    const glow = context.createRadialGradient(x, y, 0, x, y, radius);
    glow.addColorStop(0, rgba(color, alpha));
    glow.addColorStop(0.36, rgba(color, alpha * 0.36));
    glow.addColorStop(1, rgba(color, 0));
    context.fillStyle = glow;
    context.beginPath();
    context.arc(x, y, radius, 0, Math.PI * 2);
    context.fill();
  };

  const drawBeam = (light, time) => {
    const energy = 0.82 + Math.sin(time * light.speed * 2.2 + light.phase) * 0.18;
    const mousePull = (current.x / Math.max(width, 1) - 0.5) * 0.08;
    const angle = light.base
      + Math.sin(time * light.speed + light.phase) * light.swing
      + Math.sin(time * light.speed * 0.47 + light.phase * 1.7) * light.swing * 0.32
      + mousePull;
    const x = width * light.x;
    const y = height * light.y;
    const length = height * light.length;
    const spread = width * light.width;
    const neck = Math.max(8, spread * 0.035);

    context.save();
    context.translate(x, y);
    context.rotate(angle);
    context.globalAlpha = light.alpha * energy;
    context.filter = `blur(${light.blur}px)`;

    const gradient = context.createLinearGradient(0, 0, 0, length);
    gradient.addColorStop(0, rgba(light.color, 0.66));
    gradient.addColorStop(0.2, rgba(light.color, 0.3));
    gradient.addColorStop(0.58, rgba(light.color, 0.1));
    gradient.addColorStop(1, rgba(light.color, 0));

    context.fillStyle = gradient;
    context.beginPath();
    context.moveTo(-neck, 0);
    context.lineTo(neck, 0);
    context.bezierCurveTo(spread * 0.18, length * 0.22, spread * 0.52, length * 0.72, spread * 0.34, length);
    context.lineTo(-spread * 0.34, length);
    context.bezierCurveTo(-spread * 0.52, length * 0.72, -spread * 0.18, length * 0.22, -neck, 0);
    context.closePath();
    context.fill();

    context.globalAlpha = light.alpha * energy * 0.72;
    context.filter = `blur(${Math.max(7, light.blur * 0.45)}px)`;
    const core = context.createLinearGradient(0, 0, 0, length * 0.92);
    core.addColorStop(0, rgba(light.color, 0.56));
    core.addColorStop(0.3, rgba(light.color, 0.2));
    core.addColorStop(1, rgba(light.color, 0));
    context.fillStyle = core;
    context.beginPath();
    context.moveTo(-neck * 0.42, 0);
    context.lineTo(neck * 0.42, 0);
    context.bezierCurveTo(spread * 0.08, length * 0.36, spread * 0.2, length * 0.82, spread * 0.08, length * 0.94);
    context.lineTo(-spread * 0.08, length * 0.94);
    context.bezierCurveTo(-spread * 0.2, length * 0.82, -spread * 0.08, length * 0.36, -neck * 0.42, 0);
    context.closePath();
    context.fill();
    context.restore();

    drawGlow(x, y, Math.max(44, spread * 0.16), light.color, light.alpha * 0.34 * energy);
  };

  const drawHaze = (time) => {
    context.save();
    context.filter = 'blur(1.4px)';
    for (const particle of haze) {
      const driftX = Math.sin(time * 0.00042 + particle.phase) * 18;
      const driftY = Math.cos(time * 0.00028 + particle.phase) * 8;
      const x = particle.x * width + driftX;
      const y = ((particle.y + time * particle.speed) % 1) * height + driftY;
      context.fillStyle = rgba(particle.hue, particle.alpha);
      context.beginPath();
      context.arc(x, y, particle.r, 0, Math.PI * 2);
      context.fill();
    }
    context.restore();
  };

  const drawShow = (time) => {
    if (!context) return;
    context.clearRect(0, 0, width, height);
    context.globalCompositeOperation = 'lighter';

    drawGlow(width * 0.76, height * 0.47, width * 0.28, [56, 189, 248], 0.12);
    drawGlow(width * 0.88, height * 0.52, width * 0.28, [236, 72, 153], 0.14);
    drawGlow(width * 0.78, height * 0.82, width * 0.26, [245, 158, 11], 0.08);

    for (const light of lights) {
      drawBeam(light, time);
    }

    drawHaze(time);
    context.globalCompositeOperation = 'source-over';
  };

  const render = (time = 0) => {
    current.x += (target.x - current.x) * 0.13;
    current.y += (target.y - current.y) * 0.13;

    page.style.setProperty('--cursor-x', `${current.x}px`);
    page.style.setProperty('--cursor-y', `${current.y}px`);

    drawShow(time);
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

  window.addEventListener('resize', resizeCanvas, { passive: true });
  window.addEventListener('pagehide', () => {
    cancelAnimationFrame(animationFrame);
  }, { once: true });

  resizeCanvas();
  render();
})();
