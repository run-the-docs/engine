#!/usr/bin/env python3
"""Build the ep5 HTML renderer"""
import base64

with open('/tmp/k8s-logo.png','rb') as f:
    k8s_b64 = base64.b64encode(f.read()).decode()

js = r"""
const W = 1920, H = 1080, CX = 960, CY = 540;

const BG      = '#080810';
const ACCENT  = '#326CE5';
const ACCENT2 = '#60a5fa';
const TEXT    = '#f8fafc';
const CODE_BG = '#0d1117';
const GREEN   = '#22c55e';
const YELLOW  = '#eab308';
const SUBTLE  = '#334155';
const RED     = '#ef4444';

const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');

let TIMING = [];
let TOTAL_DURATION = 83.99;

const ease = {
  out:    function(t) { return 1 - Math.pow(1-t, 3); },
  inOut:  function(t) { return t < 0.5 ? 4*t*t*t : 1-Math.pow(-2*t+2,3)/2; },
  spring: function(t) {
    if(t===0) return 0; if(t===1) return 1;
    const c4 = (2*Math.PI)/2.5;
    return Math.pow(2,-10*t)*Math.sin((t*10-0.75)*c4)+1;
  },
};

function seg(t, start, end) {
  return Math.max(0, Math.min(1, (t - start) / (end - start)));
}

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x+r, y); ctx.lineTo(x+w-r, y);
  ctx.quadraticCurveTo(x+w, y, x+w, y+r);
  ctx.lineTo(x+w, y+h-r);
  ctx.quadraticCurveTo(x+w, y+h, x+w-r, y+h);
  ctx.lineTo(x+r, y+h);
  ctx.quadraticCurveTo(x, y+h, x, y+h-r);
  ctx.lineTo(x, y+r);
  ctx.quadraticCurveTo(x, y, x+r, y);
  ctx.closePath();
}

function hexToRgba(hex, a) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return 'rgba('+r+','+g+','+b+','+a+')';
}

function setFont(ctx, size, weight) {
  weight = weight || '400';
  ctx.font = weight + ' ' + size + 'px "JetBrains Mono", monospace';
}

function fitText(ctx, text, maxWidth, startSize, weight) {
  weight = weight || '400';
  let size = startSize;
  ctx.font = weight + ' ' + size + 'px "JetBrains Mono", monospace';
  while (ctx.measureText(text).width > maxWidth && size > 10) {
    size -= 1;
    ctx.font = weight + ' ' + size + 'px "JetBrains Mono", monospace';
  }
  return size;
}

function drawPod(ctx, cx, cy, r, label, ip, alpha, glowColor) {
  if(alpha <= 0) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.beginPath();
  for(let i=0; i<6; i++) {
    const angle = (Math.PI/6) + i*(Math.PI/3);
    const x = cx + r * Math.cos(angle);
    const y = cy + r * Math.sin(angle);
    if(i===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
  }
  ctx.closePath();
  const col = glowColor || ACCENT;
  ctx.fillStyle = hexToRgba(CODE_BG, 0.9);
  ctx.fill();
  ctx.strokeStyle = col;
  ctx.lineWidth = 2.5;
  ctx.stroke();
  setFont(ctx, 20, '700');
  ctx.fillStyle = TEXT;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(label, cx, cy - 10);
  setFont(ctx, 16, '400');
  ctx.fillStyle = hexToRgba(ACCENT2, 0.85);
  ctx.fillText(ip, cx, cy + 12);
  ctx.restore();
}

function drawArrow(ctx, x1, y1, x2, y2, color, alpha) {
  alpha = alpha === undefined ? 1 : alpha;
  if(alpha <= 0) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.strokeStyle = color || ACCENT;
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.stroke();
  const angle = Math.atan2(y2-y1, x2-x1);
  const al = 12;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - al*Math.cos(angle-0.4), y2 - al*Math.sin(angle-0.4));
  ctx.lineTo(x2 - al*Math.cos(angle+0.4), y2 - al*Math.sin(angle+0.4));
  ctx.closePath();
  ctx.fillStyle = color || ACCENT;
  ctx.fill();
  ctx.restore();
}

function renderFrame(frameNum) {
  const t = frameNum / 30;
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);

  // Subtle grid
  ctx.save();
  ctx.strokeStyle = hexToRgba(ACCENT, 0.04);
  ctx.lineWidth = 1;
  for(let x=0; x<=W; x+=80) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,H); ctx.stroke(); }
  for(let y=0; y<=H; y+=80) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke(); }
  ctx.restore();

  // === SCENE 1: HOOK (0-8.5s) ===
  const hookAlpha = t < 7.5 ? 1 : Math.max(0, 1 - seg(t, 7.5, 8.5));

  if(hookAlpha > 0) {
    ctx.save();
    ctx.globalAlpha = hookAlpha;
    setFont(ctx, 28, '400');
    ctx.fillStyle = hexToRgba(ACCENT2, 0.6);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    ctx.fillText('Run the Docs \u2014 Kubernetes', CX, 40);
    ctx.restore();

    const pod1Alpha = hookAlpha * (1 - ease.out(seg(t, 3.2, 4.0)));
    const pod2Alpha = hookAlpha * ease.out(seg(t, 2.0, 2.6));
    const pod3Alpha = hookAlpha * ease.out(seg(t, 2.0, 2.8));
    const pod4Alpha = hookAlpha * ease.spring(seg(t, 4.2, 5.2));

    drawPod(ctx, 560, 480, 65, 'pod-1', '10.0.0.1', pod1Alpha, ACCENT);
    drawPod(ctx, 960, 480, 65, 'pod-2', '10.0.0.2', pod2Alpha, ACCENT);
    drawPod(ctx, 1360, 480, 65, 'pod-3', '10.0.0.3', pod3Alpha, ACCENT);
    drawPod(ctx, 560, 480, 65, 'pod-4', '10.0.0.7', pod4Alpha, YELLOW);

    const line1Alpha = ease.out(seg(t, 2.0, 2.5));
    ctx.save();
    ctx.globalAlpha = hookAlpha * line1Alpha;
    setFont(ctx, 52, '700');
    ctx.fillStyle = TEXT;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Pods die and get replaced.', CX, 280);
    setFont(ctx, 48, '400');
    ctx.fillStyle = hexToRgba(ACCENT2, 0.9);
    ctx.fillText('Their IPs change.', CX, 345);
    ctx.restore();

    const errorAlpha = hookAlpha * ease.out(seg(t, 3.0, 3.3)) * (1 - ease.out(seg(t, 3.5, 4.0)));
    if(errorAlpha > 0) {
      ctx.save();
      ctx.globalAlpha = errorAlpha * 0.7;
      ctx.fillStyle = hexToRgba(RED, 0.15);
      ctx.fillRect(380, 390, 380, 90);
      setFont(ctx, 20, '700');
      ctx.fillStyle = RED;
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('frontend: hardcoded 10.0.0.1', 570, 420);
      ctx.fillText('ERR_CONNECTION_REFUSED', 570, 455);
      ctx.restore();
    }

    const line2Alpha = hookAlpha * ease.out(seg(t, 6.1, 6.6));
    ctx.save();
    ctx.globalAlpha = line2Alpha;
    setFont(ctx, 72, '700');
    ctx.fillStyle = GREEN;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText("Services don't.", CX, 780);
    ctx.restore();
  }

  // === SCENE 2: PROBLEM (7.5-24.8s) ===
  const problemAlpha = t > 7.5
    ? ease.out(seg(t, 7.5, 8.5)) * (t < 23.8 ? 1 : Math.max(0, 1 - seg(t, 23.8, 24.8)))
    : 0;

  if(problemAlpha > 0) {
    ctx.save();
    ctx.globalAlpha = problemAlpha;

    setFont(ctx, 26, '400');
    ctx.fillStyle = hexToRgba(ACCENT2, 0.5);
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText('the problem', 80, 80);

    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    ctx.globalAlpha = problemAlpha * ease.out(seg(t, 7.8, 8.3));
    setFont(ctx, 58, '700');
    ctx.fillStyle = TEXT;
    ctx.fillText("Here's the problem.", CX, 200);

    ctx.globalAlpha = problemAlpha * ease.out(seg(t, 9.5, 10.0));
    setFont(ctx, 44, '400');
    ctx.fillStyle = hexToRgba(YELLOW, 0.9);
    ctx.fillText('Frontend hardcodes a backend Pod IP.', CX, 320);

    const p2Alpha = ease.out(seg(t, 13.4, 14.0));
    ctx.globalAlpha = problemAlpha * p2Alpha;
    setFont(ctx, 38, '400');
    ctx.fillStyle = hexToRgba(RED, 0.9);
    ctx.fillText('That Pod dies.', CX, 430);

    ctx.globalAlpha = problemAlpha * p2Alpha * ease.out(seg(t, 14.2, 14.8));
    ctx.fillStyle = hexToRgba(RED, 0.75);
    ctx.fillText('New Pod. Different IP. Frontend breaks.', CX, 490);

    ctx.globalAlpha = problemAlpha * ease.out(seg(t, 18.8, 19.5));
    roundRect(ctx, CX-560, 570, 1120, 100, 12);
    ctx.fillStyle = hexToRgba(GREEN, 0.1);
    ctx.fill();
    ctx.strokeStyle = hexToRgba(GREEN, 0.6);
    ctx.lineWidth = 2;
    ctx.stroke();
    setFont(ctx, 38, '700');
    ctx.fillStyle = GREEN;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Services: stable virtual IP + DNS name', CX, 620);

    ctx.restore();
  }

  // === SCENE 3: HOW IT WORKS (23.8-46.5s) ===
  const howAlpha = t > 23.8
    ? ease.out(seg(t, 23.8, 24.8)) * (t < 45.6 ? 1 : Math.max(0, 1 - seg(t, 45.6, 46.5)))
    : 0;

  if(howAlpha > 0) {
    ctx.save();

    setFont(ctx, 26, '400');
    ctx.globalAlpha = howAlpha;
    ctx.fillStyle = hexToRgba(ACCENT2, 0.5);
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText('how it works', 80, 80);

    const svcA = howAlpha * ease.out(seg(t, 24.1, 24.8));
    ctx.globalAlpha = svcA;
    roundRect(ctx, CX-180, 220, 360, 130, 16);
    ctx.fillStyle = hexToRgba(ACCENT, 0.2);
    ctx.fill();
    ctx.strokeStyle = hexToRgba(ACCENT, 0.9);
    ctx.lineWidth = 3;
    ctx.stroke();
    setFont(ctx, 32, '700');
    ctx.fillStyle = ACCENT2;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Service', CX, 265);
    setFont(ctx, 22, '400');
    ctx.fillStyle = hexToRgba(TEXT, 0.85);
    ctx.fillText('ClusterIP: 10.96.0.1', CX, 305);

    ctx.globalAlpha = howAlpha * svcA * ease.out(seg(t, 24.8, 25.5));
    setFont(ctx, 19, '400');
    ctx.fillStyle = hexToRgba(ACCENT2, 0.7);
    ctx.fillText('my-service.default.svc.cluster.local', CX, 385);

    // Pods
    const podDefs = [
      {x: 560, ip: '10.0.0.1', label: 'pod-1', d: 0},
      {x: 960, ip: '10.0.0.2', label: 'pod-2', d: 0.15},
      {x: 1360, ip: '10.0.0.3', label: 'pod-3', d: 0.3},
    ];
    podDefs.forEach(function(p) {
      const pa = howAlpha * ease.out(seg(t, 24.3+p.d, 25.0+p.d));
      drawPod(ctx, p.x, 700, 55, p.label, p.ip, pa, ACCENT);
      const aa = howAlpha * ease.out(seg(t, 24.5+p.d, 25.2+p.d));
      drawArrow(ctx, CX, 355, p.x, 640, ACCENT, aa * 0.6);
    });

    // Client
    const clientA = howAlpha * ease.out(seg(t, 24.8, 25.5));
    ctx.globalAlpha = clientA;
    roundRect(ctx, 80, 250, 160, 65, 8);
    ctx.fillStyle = hexToRgba(SUBTLE, 0.8);
    ctx.fill();
    setFont(ctx, 22, '700');
    ctx.fillStyle = TEXT;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('client', 160, 282);
    drawArrow(ctx, 242, 282, CX-183, 282, ACCENT2, clientA * 0.8);

    // Selector badge
    const selA = howAlpha * ease.out(seg(t, 24.1, 24.7));
    ctx.globalAlpha = selA;
    roundRect(ctx, CX+200, 215, 390, 60, 8);
    ctx.fillStyle = hexToRgba(YELLOW, 0.1);
    ctx.fill();
    ctx.strokeStyle = hexToRgba(YELLOW, 0.5);
    ctx.lineWidth = 1.5;
    ctx.stroke();
    setFont(ctx, 19, '400');
    ctx.fillStyle = YELLOW;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('selector: app: MyApp', CX+395, 245);

    // kube-proxy badge
    const kpA = howAlpha * ease.out(seg(t, 32.2, 33.0));
    ctx.globalAlpha = kpA;
    roundRect(ctx, 80, 500, 380, 65, 8);
    ctx.fillStyle = hexToRgba(ACCENT, 0.12);
    ctx.fill();
    ctx.strokeStyle = hexToRgba(ACCENT, 0.5);
    ctx.lineWidth = 1.5;
    ctx.stroke();
    setFont(ctx, 22, '700');
    ctx.fillStyle = ACCENT2;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('kube-proxy', 270, 520);
    setFont(ctx, 18, '400');
    ctx.fillStyle = hexToRgba(TEXT, 0.7);
    ctx.fillText('network rules on each node', 270, 548);

    // EndpointSlice badge
    const epA = howAlpha * ease.out(seg(t, 40.4, 41.2));
    ctx.globalAlpha = epA;
    roundRect(ctx, 1450, 480, 410, 90, 8);
    ctx.fillStyle = hexToRgba(GREEN, 0.1);
    ctx.fill();
    ctx.strokeStyle = hexToRgba(GREEN, 0.5);
    ctx.lineWidth = 1.5;
    ctx.stroke();
    setFont(ctx, 22, '700');
    ctx.fillStyle = GREEN;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('EndpointSlice', 1655, 510);
    setFont(ctx, 17, '400');
    ctx.fillStyle = hexToRgba(TEXT, 0.7);
    ctx.fillText('tracks healthy Pod IPs', 1655, 537);
    ctx.fillText('auto-updated on Pod change', 1655, 558);

    ctx.restore();
  }

  // === SCENE 4: SERVICE TYPES (45.6-68.5s) ===
  const typesAlpha = t > 45.6
    ? ease.out(seg(t, 45.6, 46.5)) * (t < 67.7 ? 1 : Math.max(0, 1 - seg(t, 67.7, 68.5)))
    : 0;

  if(typesAlpha > 0) {
    ctx.save();

    ctx.globalAlpha = typesAlpha;
    setFont(ctx, 26, '400');
    ctx.fillStyle = hexToRgba(ACCENT2, 0.5);
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    ctx.fillText('service types', 80, 80);

    ctx.globalAlpha = typesAlpha * ease.out(seg(t, 45.9, 46.5));
    setFont(ctx, 58, '700');
    ctx.fillStyle = TEXT;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Four Service types.', CX, 195);

    const cards = [
      {icon: 'ClusterIP', emoji: '[default]', name: 'ClusterIP', desc: 'internal only (default)', color: ACCENT, time: 47.8},
      {icon: 'NodePort',  emoji: '[ext]',     name: 'NodePort',  desc: 'node port 30000-32767',  color: ACCENT2, time: 51.5},
      {icon: 'LB',        emoji: '[cloud]',   name: 'LoadBalancer', desc: 'cloud external LB',   color: GREEN,   time: 59.1},
      {icon: 'ExtName',   emoji: '[dns]',     name: 'ExternalName', desc: 'DNS alias',            color: YELLOW,  time: 64.1},
    ];

    const cardW = 405, cardH = 140;
    const cardY = 320;
    const cardXs = [55, 510, 965, 1420];

    cards.forEach(function(card, i) {
      const ca = typesAlpha * ease.spring(seg(t, card.time, card.time + 0.5));
      if(ca <= 0) return;
      const x = cardXs[i];
      ctx.globalAlpha = ca;
      roundRect(ctx, x, cardY, cardW, cardH, 12);
      ctx.fillStyle = hexToRgba(CODE_BG, 0.95);
      ctx.fill();
      roundRect(ctx, x, cardY, 5, cardH, 3);
      ctx.fillStyle = card.color;
      ctx.fill();
      setFont(ctx, 30, '700');
      ctx.fillStyle = card.color;
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText(card.name, x + 20, cardY + cardH/2 - 18);
      setFont(ctx, 22, '400');
      ctx.fillStyle = hexToRgba(TEXT, 0.85);
      ctx.fillText(card.desc, x + 20, cardY + cardH/2 + 20);
    });

    // YAML snippet
    const yamlAlpha = typesAlpha * ease.out(seg(t, 47.8, 48.5));
    ctx.globalAlpha = yamlAlpha;
    const yamlX = 100, yamlY = 510, yamlW = 820, yamlH = 440;
    roundRect(ctx, yamlX, yamlY, yamlW, yamlH, 12);
    ctx.fillStyle = hexToRgba(CODE_BG, 0.98);
    ctx.fill();
    ctx.strokeStyle = hexToRgba(SUBTLE, 0.8);
    ctx.lineWidth = 1.5;
    ctx.stroke();

    const lines = [
      {text: 'apiVersion: v1',          color: hexToRgba(TEXT, 0.5)},
      {text: 'kind: Service',           color: TEXT},
      {text: 'metadata:',               color: hexToRgba(TEXT, 0.5)},
      {text: '  name: my-service',      color: hexToRgba(TEXT, 0.5)},
      {text: 'spec:',                   color: hexToRgba(TEXT, 0.5)},
      {text: '  selector:',             color: YELLOW},
      {text: '    app: MyApp',          color: hexToRgba(YELLOW, 0.8)},
      {text: '  ports:',                color: hexToRgba(TEXT, 0.5)},
      {text: '  - port: 80',            color: GREEN},
      {text: '    targetPort: 9376',    color: hexToRgba(GREEN, 0.8)},
    ];
    setFont(ctx, 22, '400');
    ctx.textAlign = 'left';
    ctx.textBaseline = 'top';
    lines.forEach(function(line, i) {
      ctx.fillStyle = line.color;
      ctx.fillText(line.text, yamlX + 30, yamlY + 30 + i * 40);
    });

    ctx.restore();
  }

  // === SCENE 5: PAYOFF (67.7-77.5s) ===
  const payoffAlpha = t > 67.7
    ? ease.out(seg(t, 67.7, 68.5)) * (t < 76.7 ? 1 : Math.max(0, 1 - seg(t, 76.7, 77.5)))
    : 0;

  if(payoffAlpha > 0) {
    ctx.save();

    const glow = ctx.createRadialGradient(CX, CY, 0, CX, CY, 600);
    glow.addColorStop(0, hexToRgba(ACCENT, 0.12));
    glow.addColorStop(1, hexToRgba(ACCENT, 0));
    ctx.globalAlpha = payoffAlpha;
    ctx.fillStyle = glow;
    ctx.fillRect(0, 0, W, H);

    ctx.globalAlpha = payoffAlpha * ease.out(seg(t, 68.0, 68.6));
    setFont(ctx, 68, '700');
    ctx.fillStyle = TEXT;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('One Service. Many Pods.', CX, CY - 50);
    ctx.fillStyle = GREEN;
    ctx.fillText('Zero hardcoded IPs.', CX, CY + 40);

    ctx.globalAlpha = payoffAlpha * ease.out(seg(t, 72.4, 73.0));
    setFont(ctx, 36, '400');
    ctx.fillStyle = hexToRgba(ACCENT2, 0.9);
    ctx.fillText("That's how K8s decouples frontend from backend.", CX, CY + 150);

    ctx.restore();
  }

  // === SCENE 6: OUTRO (76.7-84s) ===
  const outroAlpha = t > 76.7 ? ease.out(seg(t, 76.7, 78.0)) : 0;

  if(outroAlpha > 0) {
    ctx.save();
    ctx.globalAlpha = outroAlpha;

    const bgGlow = ctx.createRadialGradient(CX, CY, 0, CX, CY, 500);
    bgGlow.addColorStop(0, hexToRgba(ACCENT, 0.15));
    bgGlow.addColorStop(1, hexToRgba(ACCENT, 0));
    ctx.fillStyle = bgGlow;
    ctx.fillRect(0, 0, W, H);

    const logo = document.getElementById('k8sLogo');
    if(logo && logo.complete && logo.naturalWidth > 0) {
      ctx.drawImage(logo, CX - 60, CY - 205, 120, 120);
    }

    setFont(ctx, 72, '700');
    ctx.fillStyle = TEXT;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Run the Docs', CX, CY - 25);

    setFont(ctx, 32, '400');
    ctx.fillStyle = hexToRgba(ACCENT2, 0.9);
    ctx.fillText('kubernetes \u00b7 services', CX, CY + 45);

    const pill1Text = 'kubernetes.io/docs/concepts/services-networking/service/';
    const pill2Text = 'github.com/run-the-docs/kubernetes';

    ctx.save();
    ctx.globalAlpha = outroAlpha * ease.out(seg(t, 77.5, 79.0));
    const sz1 = fitText(ctx, pill1Text, 1600, 22, '400');
    const p1W = ctx.measureText(pill1Text).width + 48;
    roundRect(ctx, CX - p1W/2, CY + 115, p1W, 42, 21);
    ctx.fillStyle = hexToRgba(ACCENT, 0.2);
    ctx.fill();
    ctx.strokeStyle = hexToRgba(ACCENT, 0.8);
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.fillStyle = ACCENT2;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(pill1Text, CX, CY + 136);
    ctx.restore();

    ctx.save();
    ctx.globalAlpha = outroAlpha * ease.out(seg(t, 78.0, 79.5));
    setFont(ctx, 22, '400');
    const p2W = ctx.measureText(pill2Text).width + 48;
    roundRect(ctx, CX - p2W/2, CY + 180, p2W, 42, 21);
    ctx.fillStyle = hexToRgba(GREEN, 0.15);
    ctx.fill();
    ctx.strokeStyle = hexToRgba(GREEN, 0.8);
    ctx.lineWidth = 1.5;
    ctx.stroke();
    ctx.fillStyle = GREEN;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(pill2Text, CX, CY + 201);
    ctx.restore();

    ctx.restore();
  }
}

window.renderFrame = renderFrame;
window.setTiming = function(segs, totalDur) {
  TIMING = segs;
  TOTAL_DURATION = totalDur;
};

renderFrame(0); // frame 0 = t=0
"""

html = (
    '<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n'
    '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
    '<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">\n'
    '<style>\n  * { margin: 0; padding: 0; box-sizing: border-box; }\n'
    '  body { background: #080810; width: 1920px; height: 1080px; overflow: hidden; }\n'
    '  canvas { display: block; }\n  img { display: none; }\n</style>\n</head>\n<body>\n'
    '<canvas id="c" width="1920" height="1080"></canvas>\n'
    '<img id="k8sLogo" src="data:image/png;base64,' + k8s_b64 + '">\n'
    '<script>\n' + js + '\n</script>\n</body>\n</html>'
)

with open('/tmp/k8s_ep5.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Written:', len(html), 'bytes')
