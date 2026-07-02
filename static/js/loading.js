(() => {
  const page = document.querySelector('.loading-page');
  const layer = document.querySelector('.loading-ripple-layer');
  const canvas = document.querySelector('.loading-show-canvas');
  if (!page || !layer) return;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduceMotion) return;

  const context = canvas?.getContext('2d', { alpha: true, desynchronized: true });
  const target = { x: window.innerWidth * 0.68, y: window.innerHeight * 0.48 };
  const current = { ...target };
  const lights = [
    { x: 0.68, y: 0.02, color: [56, 189, 248], base: -0.4, swing: 0.34, speed: 0.00165, phase: 0.2, width: 0.22, length: 1.02, alpha: 0.68 },
    { x: 0.76, y: 0.03, color: [168, 85, 247], base: -0.18, swing: 0.38, speed: 0.00135, phase: 1.9, width: 0.24, length: 0.96, alpha: 0.62 },
    { x: 0.85, y: 0.04, color: [34, 211, 238], base: 0.02, swing: 0.34, speed: 0.0018, phase: 3.2, width: 0.2, length: 0.9, alpha: 0.54 },
    { x: 0.93, y: 0.06, color: [236, 72, 153], base: 0.18, swing: 0.36, speed: 0.0015, phase: 4.5, width: 0.22, length: 0.9, alpha: 0.58 },
    { x: 1.01, y: 0.09, color: [245, 158, 11], base: 0.34, swing: 0.28, speed: 0.00195, phase: 2.5, width: 0.18, length: 0.84, alpha: 0.48 },
    { x: 0.72, y: 0.25, color: [125, 211, 252], base: -0.62, swing: 0.22, speed: 0.002, phase: 5.1, width: 0.15, length: 0.62, alpha: 0.4 },
    { x: 0.82, y: 0.31, color: [244, 114, 182], base: -0.32, swing: 0.28, speed: 0.00165, phase: 3.7, width: 0.16, length: 0.58, alpha: 0.36 },
    { x: 0.91, y: 0.35, color: [251, 191, 36], base: 0.24, swing: 0.24, speed: 0.0021, phase: 1.2, width: 0.14, length: 0.56, alpha: 0.34 },
    { x: 0.62, y: 0.42, color: [59, 130, 246], base: -0.86, swing: 0.2, speed: 0.00172, phase: 2.2, width: 0.13, length: 0.46, alpha: 0.34 }
  ];
  const haze = Array.from({ length: 42 }, (_, index) => ({
    x: 0.42 + Math.random() * 0.62,
    y: Math.random(),
    size: 8 + Math.random() * 22,
    speed: 0.000018 + Math.random() * 0.00004,
    phase: index * 0.73,
    alpha: 0.08 + Math.random() * 0.12
  }));

  let width = window.innerWidth;
  let height = window.innerHeight;
  let pixelRatio = 1;
  let animationFrame = 0;
  let beamTextures = [];
  let glowTextures = [];
  let hazeTexture;

  const rgba = ([r, g, b], alpha) => `rgba(${r}, ${g}, ${b}, ${alpha})`;

  const createBeamTexture = (color) => {
    const texture = document.createElement('canvas');
    texture.width = 360;
    texture.height = 980;
    const ctx = texture.getContext('2d');
    const center = texture.width / 2;
    const bottom = texture.height - 18;

    ctx.filter = 'blur(16px)';
    const outer = ctx.createLinearGradient(0, 0, 0, texture.height);
    outer.addColorStop(0, rgba(color, 0.72));
    outer.addColorStop(0.18, rgba(color, 0.36));
    outer.addColorStop(0.54, rgba(color, 0.12));
    outer.addColorStop(1, rgba(color, 0));
    ctx.fillStyle = outer;
    ctx.beginPath();
    ctx.moveTo(center - 10, 18);
    ctx.lineTo(center + 10, 18);
    ctx.bezierCurveTo(center + 54, 250, center + 166, 710, center + 154, bottom);
    ctx.lineTo(center - 154, bottom);
    ctx.bezierCurveTo(center - 166, 710, center - 54, 250, center - 10, 18);
    ctx.closePath();
    ctx.fill();

    ctx.filter = 'blur(6px)';
    const core = ctx.createLinearGradient(0, 0, 0, texture.height);
    core.addColorStop(0, rgba(color, 0.62));
    core.addColorStop(0.26, rgba(color, 0.24));
    core.addColorStop(0.78, rgba(color, 0.06));
    core.addColorStop(1, rgba(color, 0));
    ctx.fillStyle = core;
    ctx.beginPath();
    ctx.moveTo(center - 4, 10);
    ctx.lineTo(center + 4, 10);
    ctx.bezierCurveTo(center + 22, 260, center + 74, 740, center + 54, bottom);
    ctx.lineTo(center - 54, bottom);
    ctx.bezierCurveTo(center - 74, 740, center - 22, 260, center - 4, 10);
    ctx.closePath();
    ctx.fill();

    return texture;
  };

  const createGlowTexture = (color) => {
    const texture = document.createElement('canvas');
    texture.width = 256;
    texture.height = 256;
    const ctx = texture.getContext('2d');
    const center = texture.width / 2;
    const glow = ctx.createRadialGradient(center, center, 0, center, center, center);
    glow.addColorStop(0, rgba(color, 0.72));
    glow.addColorStop(0.28, rgba(color, 0.26));
    glow.addColorStop(1, rgba(color, 0));
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, texture.width, texture.height);
    return texture;
  };

  const createHazeTexture = () => {
    const texture = document.createElement('canvas');
    texture.width = 48;
    texture.height = 48;
    const ctx = texture.getContext('2d');
    const glow = ctx.createRadialGradient(24, 24, 0, 24, 24, 24);
    glow.addColorStop(0, 'rgba(255,255,255,0.32)');
    glow.addColorStop(0.36, 'rgba(125,211,252,0.12)');
    glow.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, 48, 48);
    return texture;
  };

  const buildTextures = () => {
    beamTextures = lights.map((light) => createBeamTexture(light.color));
    glowTextures = lights.map((light) => createGlowTexture(light.color));
    hazeTexture = createHazeTexture();
  };

  const resizeCanvas = () => {
    if (!context) return;
    pixelRatio = Math.min(window.devicePixelRatio || 1, 1);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * pixelRatio);
    canvas.height = Math.round(height * pixelRatio);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    context.imageSmoothingEnabled = true;
  };

  const drawTexture = (texture, x, y, size, alpha) => {
    context.globalAlpha = alpha;
    context.drawImage(texture, x - size / 2, y - size / 2, size, size);
  };

  const drawBeam = (light, texture, glow, time) => {
    const energy = 0.86 + Math.sin(time * light.speed * 2.4 + light.phase) * 0.14;
    const mousePull = (current.x / Math.max(width, 1) - 0.5) * 0.08;
    const angle = light.base
      + Math.sin(time * light.speed + light.phase) * light.swing
      + Math.sin(time * light.speed * 0.42 + light.phase * 1.6) * light.swing * 0.28
      + mousePull;
    const x = width * light.x;
    const y = height * light.y;
    const beamWidth = width * light.width;
    const beamLength = height * light.length;

    context.save();
    context.translate(x, y);
    context.rotate(angle);
    context.globalAlpha = light.alpha * energy;
    context.drawImage(texture, -beamWidth / 2, -8, beamWidth, beamLength);
    context.globalAlpha = light.alpha * energy * 0.42;
    context.drawImage(texture, -beamWidth * 0.34, -4, beamWidth * 0.68, beamLength * 0.92);
    context.restore();

    drawTexture(glow, x, y, Math.max(78, beamWidth * 0.46), light.alpha * 0.62 * energy);
  };

  const drawHaze = (time) => {
    for (const particle of haze) {
      const driftX = Math.sin(time * 0.00042 + particle.phase) * 18;
      const driftY = Math.cos(time * 0.00028 + particle.phase) * 8;
      const x = particle.x * width + driftX;
      const y = ((particle.y + time * particle.speed) % 1) * height + driftY;
      drawTexture(hazeTexture, x, y, particle.size, particle.alpha);
    }
  };

  const drawShow = (time) => {
    if (!context) return;
    context.clearRect(0, 0, width, height);
    context.globalCompositeOperation = 'lighter';

    drawTexture(glowTextures[0], width * 0.76, height * 0.46, width * 0.44, 0.16);
    drawTexture(glowTextures[3], width * 0.88, height * 0.52, width * 0.42, 0.17);
    drawTexture(glowTextures[4], width * 0.8, height * 0.82, width * 0.36, 0.1);

    for (let index = 0; index < lights.length; index += 1) {
      drawBeam(lights[index], beamTextures[index], glowTextures[index], time);
    }

    drawHaze(time);
    context.globalCompositeOperation = 'source-over';
    context.globalAlpha = 1;
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

  buildTextures();
  resizeCanvas();
  render();
})();
