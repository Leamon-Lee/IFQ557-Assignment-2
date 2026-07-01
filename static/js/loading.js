(() => {
  const layer = document.querySelector('.loading-ripple-layer');
  const canvas = document.querySelector('.loading-neon-canvas');
  if (!layer || !canvas) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const context = canvas.getContext('2d', { alpha: true });
  const pointer = { x: 0.72, y: 0.52, active: false };
  const particles = [];
  let animationFrame = 0;
  let lastMove = 0;
  let width = 0;
  let height = 0;
  let dpr = 1;

  const resizeCanvas = () => {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(dpr, 0, 0, dpr, 0, 0);
    particles.length = 0;

    const count = Math.min(120, Math.max(56, Math.round(width / 12)));
    for (let i = 0; i < count; i += 1) {
      particles.push({
        x: Math.random() * width,
        y: Math.random() * height,
        radius: 0.65 + Math.random() * 1.75,
        alpha: 0.1 + Math.random() * 0.28,
        speed: 0.28 + Math.random() * 0.85,
        hue: Math.random() > 0.5 ? 194 : 305
      });
    }
  };

  const drawRibbon = (time, index, baseY, amplitude, colorA, colorB) => {
    const gradient = context.createLinearGradient(0, 0, width, 0);
    gradient.addColorStop(0, 'rgba(255,255,255,0)');
    gradient.addColorStop(0.2, colorA);
    gradient.addColorStop(0.58, colorB);
    gradient.addColorStop(1, 'rgba(255,255,255,0)');

    context.beginPath();
    for (let x = -48; x <= width + 48; x += 16) {
      const drift = Math.sin(x * 0.006 + time * (0.00105 + index * 0.00016));
      const pulse = Math.sin(x * 0.013 - time * (0.00155 + index * 0.00011));
      const pointerPull = pointer.active ? Math.max(0, 1 - Math.abs(x - pointer.x * width) / 440) * 22 : 0;
      const y = baseY + drift * amplitude + pulse * amplitude * 0.36 - pointerPull;
      if (x === -48) context.moveTo(x, y);
      else context.lineTo(x, y);
    }

    context.strokeStyle = gradient;
    context.lineWidth = 1.6 + index * 1.25;
    context.shadowBlur = 20 + index * 8;
    context.shadowColor = index % 2 ? 'rgba(56,189,248,0.7)' : 'rgba(236,72,153,0.62)';
    context.stroke();
  };

  const drawStageCore = (time) => {
    const coreX = width * (0.72 + Math.sin(time * 0.00028) * 0.035);
    const coreY = height * (0.49 + Math.cos(time * 0.00034) * 0.025);
    const radius = 72 + Math.sin(time * 0.0018) * 18;

    for (let i = 0; i < 5; i += 1) {
      context.beginPath();
      context.arc(coreX, coreY, radius + i * 34, time * 0.0009 + i, time * 0.0009 + Math.PI * 1.35 + i);
      context.strokeStyle = `rgba(${i % 2 ? '56,189,248' : '236,72,153'},${0.3 - i * 0.043})`;
      context.lineWidth = 1.1 + i * 0.58;
      context.shadowBlur = 26;
      context.shadowColor = i % 2 ? 'rgba(56,189,248,0.62)' : 'rgba(236,72,153,0.52)';
      context.stroke();
    }
  };

  const drawParticles = () => {
    for (const particle of particles) {
      particle.x += particle.speed * 0.18;
      particle.y -= particle.speed * 0.06;
      if (particle.x > width + 12) particle.x = -12;
      if (particle.y < -12) particle.y = height + 12;

      context.beginPath();
      context.fillStyle = `hsla(${particle.hue}, 95%, 72%, ${particle.alpha})`;
      context.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
      context.fill();
    }
  };

  const animate = (time = 0) => {
    context.clearRect(0, 0, width, height);
    context.globalCompositeOperation = 'lighter';

    drawRibbon(time, 0, height * 0.56, 26, 'rgba(56,189,248,0.2)', 'rgba(236,72,153,0.44)');
    drawRibbon(time, 1, height * 0.66, 34, 'rgba(168,85,247,0.34)', 'rgba(251,191,36,0.26)');
    drawRibbon(time, 2, height * 0.47, 21, 'rgba(14,165,233,0.22)', 'rgba(244,114,182,0.32)');
    drawStageCore(time);
    drawParticles();

    context.globalCompositeOperation = 'source-over';
    animationFrame = requestAnimationFrame(animate);
  };

  const createRipple = (x, y, strong = false) => {
    const ripple = document.createElement('span');
    ripple.className = strong ? 'sound-ripple sound-ripple-strong' : 'sound-ripple';
    ripple.style.left = `${x}px`;
    ripple.style.top = `${y}px`;
    layer.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
  };

  window.addEventListener('pointermove', (event) => {
    const now = Date.now();
    if (now - lastMove < 85) return;
    lastMove = now;
    pointer.x = event.clientX / window.innerWidth;
    pointer.y = event.clientY / window.innerHeight;
    pointer.active = true;
    createRipple(event.clientX, event.clientY);
  }, { passive: true });

  window.addEventListener('pointerdown', (event) => {
    pointer.x = event.clientX / window.innerWidth;
    pointer.y = event.clientY / window.innerHeight;
    pointer.active = true;
    createRipple(event.clientX, event.clientY, true);
  }, { passive: true });

  document.addEventListener('pointerleave', () => {
    pointer.active = false;
  }, { passive: true });

  window.addEventListener('resize', resizeCanvas, { passive: true });
  window.addEventListener('pagehide', () => cancelAnimationFrame(animationFrame), { once: true });

  resizeCanvas();
  animationFrame = requestAnimationFrame(animate);
})();
