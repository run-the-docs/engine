#!/usr/bin/env python3
"""Build k8s_ep9.html with embedded K8s logo"""
import base64, json

with open('/tmp/k8s-logo.png', 'rb') as f:
    logo_b64 = base64.b64encode(f.read()).decode()

with open('/tmp/k8s_ep9_timing.json') as f:
    timing = json.load(f)

TOTAL = timing['total_duration']
segs = timing['segments']

html = f'''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #080810; width: 1920px; height: 1080px; overflow: hidden; }}
  canvas {{ display: block; }}
  img {{ display: none; }}
</style>
</head>
<body>
<canvas id="c" width="1920" height="1080"></canvas>
<img id="k8sLogo" src="data:image/png;base64,{logo_b64}">
<script>
const W = 1920, H = 1080, CX = 960, CY = 540;
const BG = '#080810';
const ACCENT = '#326CE5';
const ACCENT2 = '#60a5fa';
const TEXT = '#f8fafc';
const CODE_BG = '#0d1117';
const GREEN = '#22c55e';
const YELLOW = '#eab308';
const RED = '#ef4444';
const ORANGE = '#f97316';
const SUBTLE = '#334155';

const TOTAL_DURATION = {TOTAL};

const ease = {{
  out: t => 1 - Math.pow(1-t, 3),
  spring: t => {{
    if(t===0) return 0; if(t===1) return 1;
    const c4 = (2*Math.PI)/2.5;
    return Math.pow(2,-10*t)*Math.sin((t*10-0.75)*c4)+1;
  }},
}};

function seg(t, start, end) {{
  return Math.max(0, Math.min(1, (t - start) / (end - start)));
}}

function roundRect(ctx, x, y, w, h, r) {{
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
}}

function hex2rgba(hex, a) {{
  const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
  return `rgba(${{r}},${{g}},${{b}},${{a}})`;
}}

function fitText(ctx, text, maxWidth, startSize) {{
  let size = startSize;
  ctx.font = `${{size}}px "JetBrains Mono", monospace`;
  while (ctx.measureText(text).width > maxWidth && size > 10) {{
    size -= 1;
    ctx.font = `${{size}}px "JetBrains Mono", monospace`;
  }}
  return size;
}}

function setFont(ctx, size, weight) {{
  ctx.font = `${{weight||400}} ${{size}}px "JetBrains Mono", monospace`;
}}

function drawBG(ctx) {{
  ctx.fillStyle = BG;
  ctx.fillRect(0, 0, W, H);
  ctx.strokeStyle = 'rgba(50,108,229,0.05)';
  ctx.lineWidth = 1;
  for(let x=0; x<W; x+=80) {{ ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,H); ctx.stroke(); }}
  for(let y=0; y<H; y+=80) {{ ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(W,y); ctx.stroke(); }}
}}

function drawEpLabel(ctx, alpha) {{
  ctx.save();
  ctx.globalAlpha = (alpha||1) * 0.45;
  setFont(ctx, 22, 400);
  ctx.fillStyle = SUBTLE;
  ctx.textAlign = 'left';
  ctx.textBaseline = 'bottom';
  ctx.fillText('run the docs · kubernetes · ep09', 48, H - 32);
  ctx.restore();
}}

function drawArrow(ctx, x1, y1, x2, y2, color, dash) {{
  ctx.save();
  ctx.strokeStyle = color || ACCENT;
  ctx.lineWidth = 3;
  if (dash) ctx.setLineDash(dash);
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  ctx.setLineDash([]);
  const angle = Math.atan2(y2-y1, x2-x1);
  ctx.fillStyle = color || ACCENT;
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - 18*Math.cos(angle-0.4), y2 - 18*Math.sin(angle-0.4));
  ctx.lineTo(x2 - 18*Math.cos(angle+0.4), y2 - 18*Math.sin(angle+0.4));
  ctx.closePath(); ctx.fill();
  ctx.restore();
}}

// SCENE 1: HOOK (0-9.5s) — Internet splits to 3 services
function drawScene1(ctx, t) {{
  const tSec = t * TOTAL_DURATION;
  drawBG(ctx);

  const globeA = ease.out(seg(tSec, 2.0, 2.8));
  ctx.save();
  ctx.globalAlpha = globeA;
  ctx.beginPath();
  ctx.arc(220, CY, 110, 0, Math.PI*2);
  ctx.fillStyle = hex2rgba(ACCENT, 0.15);
  ctx.fill();
  ctx.strokeStyle = ACCENT; ctx.lineWidth = 3; ctx.stroke();
  setFont(ctx, 64, 400);
  ctx.fillStyle = ACCENT2; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('🌐', 220, CY - 14);
  setFont(ctx, 26, 600);
  ctx.fillText('Internet', 220, CY + 66);
  ctx.restore();

  const services = [
    {{ name: 'api-svc', y: CY - 200, color: GREEN,   t0: 3.0 }},
    {{ name: 'app-svc', y: CY,       color: ACCENT2, t0: 3.25 }},
    {{ name: 'web-svc', y: CY + 200, color: YELLOW,  t0: 3.5 }},
  ];
  services.forEach(svc => {{
    const a = ease.out(seg(tSec, svc.t0, svc.t0 + 0.9));
    ctx.save(); ctx.globalAlpha = a;
    drawArrow(ctx, 342, CY, 750, svc.y, svc.color, [8,5]);
    roundRect(ctx, 760, svc.y - 50, 320, 100, 12);
    ctx.fillStyle = hex2rgba(svc.color, 0.12); ctx.fill();
    ctx.strokeStyle = svc.color; ctx.lineWidth = 2; ctx.stroke();
    setFont(ctx, 32, 700);
    ctx.fillStyle = svc.color; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(svc.name, 920, svc.y);
    ctx.restore();
  }});

  const txtA = ease.out(seg(tSec, 5.0, 5.8));
  ctx.save();
  ctx.globalAlpha = txtA;
  setFont(ctx, 52, 700);
  ctx.fillStyle = TEXT;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  const hookTxt = 'One IP. Multiple services. Different domains.';
  const sz = fitText(ctx, hookTxt, W - 500, 52);
  ctx.font = `700 ${{sz}}px "JetBrains Mono", monospace`;
  ctx.fillText(hookTxt, CX + 180, H - 200);
  setFont(ctx, 40, 400);
  ctx.fillStyle = ACCENT2;
  ctx.fillText("That's what Ingress does.", CX + 180, H - 140);
  ctx.restore();

  drawEpLabel(ctx, 1);
}}

// SCENE 2: WITHOUT INGRESS (9.5-22.5s)
function drawScene2(ctx, t) {{
  const tSec = t * TOTAL_DURATION;
  drawBG(ctx);

  const titleA = ease.out(seg(tSec, 9.6, 10.2));
  ctx.save(); ctx.globalAlpha = titleA;
  setFont(ctx, 48, 700); ctx.fillStyle = RED;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('Without Ingress: every Service = separate cloud cost', CX, 40);
  ctx.restore();

  const lbs = [
    {{ sub: 'api.example.com', color: ORANGE, x: 130, t0: 9.6 }},
    {{ sub: 'app.example.com', color: ORANGE, x: 690, t0: 10.0 }},
    {{ sub: 'web.example.com', color: ORANGE, x: 1250, t0: 10.4 }},
  ];
  lbs.forEach(lb => {{
    const a = ease.spring(seg(tSec, lb.t0, lb.t0 + 0.8));
    ctx.save(); ctx.globalAlpha = Math.min(a, 1);
    roundRect(ctx, lb.x, 165, 500, 250, 14);
    ctx.fillStyle = hex2rgba(ORANGE, 0.1); ctx.fill();
    ctx.strokeStyle = ORANGE; ctx.lineWidth = 2.5; ctx.stroke();
    setFont(ctx, 30, 700); ctx.fillStyle = ORANGE;
    ctx.textAlign = 'center'; ctx.textBaseline = 'top';
    ctx.fillText('type: LoadBalancer', lb.x + 250, 180);
    setFont(ctx, 22, 400); ctx.fillStyle = TEXT;
    ctx.fillText(lb.sub, lb.x + 250, 220);
    setFont(ctx, 80, 700); ctx.fillStyle = RED;
    ctx.textBaseline = 'middle';
    ctx.fillText('$', lb.x + 250, 320);
    ctx.restore();
  }});

  const billA = ease.out(seg(tSec, 11.0, 11.7));
  ctx.save(); ctx.globalAlpha = billA;
  setFont(ctx, 40, 700); ctx.fillStyle = RED;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('3 cloud load balancers = 3× the bill', CX, 460);
  ctx.restore();

  const npA = ease.out(seg(tSec, 13.96, 14.7));
  ctx.save(); ctx.globalAlpha = npA;
  roundRect(ctx, 380, 570, 1160, 110, 14);
  ctx.fillStyle = hex2rgba(YELLOW, 0.1); ctx.fill();
  ctx.strokeStyle = YELLOW; ctx.lineWidth = 2; ctx.stroke();
  setFont(ctx, 34, 700); ctx.fillStyle = YELLOW;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('NodePort: myapp.com:31042 ← ugly port numbers', CX, 625);
  ctx.restore();

  const ingrA = ease.spring(seg(tSec, 17.31, 18.2));
  ctx.save(); ctx.globalAlpha = Math.min(ingrA, 1);
  setFont(ctx, 44, 700); ctx.fillStyle = GREEN;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('Ingress: one entry point, route by hostname and path', CX, 750);
  ctx.restore();

  drawEpLabel(ctx, 1);
}}

// SCENE 3: HOW IT WORKS (22.5-37.5s)
function drawScene3(ctx, t) {{
  const tSec = t * TOTAL_DURATION;
  drawBG(ctx);

  const titleA = ease.out(seg(tSec, 22.12, 22.7));
  ctx.save(); ctx.globalAlpha = titleA;
  setFont(ctx, 48, 700); ctx.fillStyle = GREEN;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('With Ingress: one IP, many services', CX, 40);
  ctx.restore();

  // Internet box
  const baseA = ease.out(seg(tSec, 22.12, 23.0));
  ctx.save(); ctx.globalAlpha = baseA;
  roundRect(ctx, 30, CY - 80, 200, 160, 14);
  ctx.fillStyle = hex2rgba(ACCENT, 0.12); ctx.fill();
  ctx.strokeStyle = ACCENT; ctx.lineWidth = 2; ctx.stroke();
  setFont(ctx, 42, 400); ctx.fillStyle = ACCENT2;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('🌐', 130, CY - 18);
  setFont(ctx, 24, 600); ctx.fillText('Internet', 130, CY + 34);
  ctx.restore();

  // Arrow to controller
  ctx.save(); ctx.globalAlpha = baseA;
  drawArrow(ctx, 236, CY, 400, CY, ACCENT);
  ctx.restore();

  // Ingress Controller box  
  const ctrlA = ease.out(seg(tSec, 25.94, 26.8));
  ctx.save(); ctx.globalAlpha = ctrlA;
  roundRect(ctx, 410, CY - 150, 380, 300, 16);
  ctx.fillStyle = hex2rgba(ACCENT, 0.18); ctx.fill();
  ctx.strokeStyle = ACCENT; ctx.lineWidth = 3;
  ctx.shadowColor = ACCENT; ctx.shadowBlur = 24; ctx.stroke(); ctx.shadowBlur = 0;
  setFont(ctx, 26, 700); ctx.fillStyle = ACCENT2;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('Ingress Controller', 600, CY - 130);
  setFont(ctx, 22, 400); ctx.fillStyle = TEXT;
  ctx.fillText('nginx / Traefik', 600, CY - 94);
  ctx.fillText('HAProxy / ALB / GKE', 600, CY - 60);
  setFont(ctx, 48, 400); ctx.fillStyle = ACCENT;
  ctx.textBaseline = 'middle';
  ctx.fillText('⚙', 600, CY + 36);
  ctx.restore();

  // YAML bubble above controller
  ctx.save(); ctx.globalAlpha = ease.out(seg(tSec, 22.12, 22.8));
  roundRect(ctx, 410, 130, 380, 90, 10);
  ctx.fillStyle = hex2rgba(ACCENT, 0.08); ctx.fill();
  setFont(ctx, 20, 400); ctx.fillStyle = ACCENT2;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('kind: Ingress', 600, 162);
  ctx.fillText('rules: [...]', 600, 190);
  ctx.restore();

  // Services
  const svcs = [
    {{ name: 'api-svc', y: CY - 230, color: GREEN,   t0: 32.80 }},
    {{ name: 'app-svc', y: CY,       color: ACCENT2, t0: 33.2 }},
    {{ name: 'web-svc', y: CY + 230, color: YELLOW,  t0: 33.6 }},
  ];
  svcs.forEach(svc => {{
    const a = ease.out(seg(tSec, svc.t0, svc.t0 + 0.8));
    ctx.save(); ctx.globalAlpha = a;
    drawArrow(ctx, 796, CY, 960, svc.y, svc.color, [6,4]);
    roundRect(ctx, 970, svc.y - 50, 280, 100, 10);
    ctx.fillStyle = hex2rgba(svc.color, 0.1); ctx.fill();
    ctx.strokeStyle = svc.color; ctx.lineWidth = 2; ctx.stroke();
    setFont(ctx, 30, 700); ctx.fillStyle = svc.color;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(svc.name, 1110, svc.y - 12);
    setFont(ctx, 20, 400); ctx.fillStyle = TEXT;
    ctx.fillText('→ Pods', 1110, svc.y + 22);
    ctx.restore();
  }});

  drawEpLabel(ctx, 1);
}}

// SCENE 4: ROUTING RULES (37.5-52.5s)
function drawScene4(ctx, t) {{
  const tSec = t * TOTAL_DURATION;
  drawBG(ctx);

  const titleA = ease.out(seg(tSec, 37.39, 37.9));
  ctx.save(); ctx.globalAlpha = titleA;
  setFont(ctx, 48, 700); ctx.fillStyle = ACCENT2;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('Routing Rules', CX, 40);
  ctx.restore();

  // Host-based
  const hostLabelA = ease.out(seg(tSec, 37.39, 37.9));
  ctx.save(); ctx.globalAlpha = hostLabelA;
  setFont(ctx, 30, 700); ctx.fillStyle = SUBTLE;
  ctx.textAlign = 'left'; ctx.textBaseline = 'top';
  ctx.fillText('By hostname:', 80, 130);
  ctx.restore();

  const hostRules = [
    {{ host: 'api.example.com', svc: 'api-svc:80',      color: GREEN   }},
    {{ host: 'app.example.com', svc: 'frontend-svc:80', color: ACCENT2 }},
  ];
  hostRules.forEach((rule, i) => {{
    const a = ease.out(seg(tSec, 37.39 + i*0.3, 38.1 + i*0.3));
    ctx.save(); ctx.globalAlpha = a;
    const ry = 180 + i * 110;
    roundRect(ctx, 80, ry, 860, 90, 10);
    ctx.fillStyle = hex2rgba(rule.color, 0.1); ctx.fill();
    ctx.strokeStyle = rule.color; ctx.lineWidth = 1.5; ctx.stroke();
    setFont(ctx, 30, 700); ctx.fillStyle = rule.color;
    ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
    ctx.fillText(rule.host, 110, ry + 26);
    setFont(ctx, 26, 400); ctx.fillStyle = TEXT;
    ctx.fillText('→  ' + rule.svc, 110, ry + 62);
    ctx.restore();
  }});

  // Path-based
  const pathLabelA = ease.out(seg(tSec, 47.34, 47.9));
  ctx.save(); ctx.globalAlpha = pathLabelA;
  setFont(ctx, 30, 700); ctx.fillStyle = SUBTLE;
  ctx.textAlign = 'left'; ctx.textBaseline = 'top';
  ctx.fillText('By path:', 80, 430);
  ctx.restore();

  const pathRules = [
    {{ path: '/api/',  svc: 'api-svc:80',      color: GREEN   }},
    {{ path: '/app/',  svc: 'frontend-svc:80', color: ACCENT2 }},
  ];
  pathRules.forEach((rule, i) => {{
    const a = ease.out(seg(tSec, 47.34 + i*0.3, 48.1 + i*0.3));
    ctx.save(); ctx.globalAlpha = a;
    const ry = 480 + i * 110;
    roundRect(ctx, 80, ry, 860, 90, 10);
    ctx.fillStyle = hex2rgba(rule.color, 0.1); ctx.fill();
    ctx.strokeStyle = rule.color; ctx.lineWidth = 1.5; ctx.stroke();
    setFont(ctx, 34, 700); ctx.fillStyle = rule.color;
    ctx.textAlign = 'left'; ctx.textBaseline = 'middle';
    ctx.fillText(rule.path, 110, ry + 26);
    setFont(ctx, 26, 400); ctx.fillStyle = TEXT;
    ctx.fillText('→  ' + rule.svc, 110, ry + 62);
    ctx.restore();
  }});

  // TLS badge
  const tlsA = ease.out(seg(tSec, 52.87, 53.8));
  ctx.save(); ctx.globalAlpha = tlsA;
  roundRect(ctx, 1060, 155, 800, 400, 16);
  ctx.fillStyle = hex2rgba(GREEN, 0.08); ctx.fill();
  ctx.strokeStyle = GREEN; ctx.lineWidth = 2.5; ctx.stroke();
  setFont(ctx, 36, 700); ctx.fillStyle = GREEN;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('🔒  TLS Termination', 1460, 172);
  setFont(ctx, 26, 400); ctx.fillStyle = ACCENT2;
  ctx.fillText('tls:', 1460, 224);
  ctx.fillText('  - hosts: [api.example.com]', 1460, 258);
  ctx.fillText('    secretName: tls-secret', 1460, 292);
  setFont(ctx, 24, 400); ctx.fillStyle = SUBTLE;
  ctx.fillText('Controller terminates TLS.', 1460, 362);
  ctx.fillText('Services stay plain HTTP inside.', 1460, 396);
  ctx.restore();

  drawEpLabel(ctx, 1);
}}

// SCENE 5: FROZEN (60-68.5s)
function drawScene5(ctx, t) {{
  const tSec = t * TOTAL_DURATION;
  drawBG(ctx);

  const bannerA = ease.out(seg(tSec, 60.39, 61.0));
  ctx.save(); ctx.globalAlpha = bannerA;
  roundRect(ctx, 120, 100, W - 240, 130, 14);
  ctx.fillStyle = hex2rgba(YELLOW, 0.12); ctx.fill();
  ctx.strokeStyle = YELLOW; ctx.lineWidth = 3;
  ctx.shadowColor = YELLOW; ctx.shadowBlur = 20; ctx.stroke(); ctx.shadowBlur = 0;
  setFont(ctx, 56, 700); ctx.fillStyle = YELLOW;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('⚠  Ingress API: FROZEN', CX, 165);
  ctx.restore();

  const detailA = ease.out(seg(tSec, 61.0, 61.8));
  ctx.save(); ctx.globalAlpha = detailA;
  setFont(ctx, 36, 400); ctx.fillStyle = TEXT;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('Generally Available. No new features. No further development.', CX, 280);
  ctx.restore();

  const gwA = ease.spring(seg(tSec, 62.5, 63.5));
  ctx.save(); ctx.globalAlpha = Math.min(gwA, 1);
  const gx = CX - 400, gy = 380, gw = 800, gh = 200;
  roundRect(ctx, gx, gy, gw, gh, 16);
  ctx.fillStyle = hex2rgba(GREEN, 0.12); ctx.fill();
  ctx.strokeStyle = GREEN; ctx.lineWidth = 3;
  ctx.shadowColor = GREEN; ctx.shadowBlur = 20; ctx.stroke(); ctx.shadowBlur = 0;
  setFont(ctx, 48, 700); ctx.fillStyle = GREEN;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('Gateway API', CX, gy + 68);
  setFont(ctx, 28, 400); ctx.fillStyle = TEXT;
  ctx.fillText('For new projects — more powerful routing', CX, gy + 124);
  ctx.restore();

  const arrowA = ease.out(seg(tSec, 62.2, 63.0));
  ctx.save(); ctx.globalAlpha = arrowA;
  setFont(ctx, 40, 700); ctx.fillStyle = GREEN;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText('→', CX, 345);
  ctx.restore();

  const catchA = ease.out(seg(tSec, 64.5, 65.2));
  ctx.save(); ctx.globalAlpha = catchA;
  setFont(ctx, 32, 400); ctx.fillStyle = SUBTLE;
  ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  ctx.fillText('Ingress still works. Existing clusters keep it. New projects: Gateway API.', CX, 650);
  ctx.restore();

  drawEpLabel(ctx, 1);
}}

// SCENE 6: OUTRO (68.5+)
function drawScene6(ctx, t) {{
  const tSec = t * TOTAL_DURATION;
  drawBG(ctx);

  const p = ease.out(seg(tSec, 68.6, 70.5));

  const logo = document.getElementById('k8sLogo');
  if (logo && logo.complete && p > 0) {{
    ctx.save();
    ctx.globalAlpha = p;
    ctx.drawImage(logo, CX - 80, 190, 160, 160);
    ctx.restore();
  }}

  ctx.save();
  ctx.globalAlpha = p;
  setFont(ctx, 80, 700);
  ctx.fillStyle = TEXT;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('kubernetes · ingress', CX, CY - 10);
  setFont(ctx, 34, 400);
  ctx.fillStyle = SUBTLE;
  ctx.fillText('run the docs', CX, CY + 60);
  ctx.restore();

  const pillA = ease.out(seg(tSec, 69.5, 71.0)) * p;
  const pills = [
    {{ label: 'kubernetes.io/docs/concepts/services-networking/ingress/', color: ACCENT }},
    {{ label: 'github.com/run-the-docs/kubernetes', color: ACCENT2 }},
  ];
  pills.forEach((pill, i) => {{
    const py = CY + 140 + i * 86;
    ctx.save(); ctx.globalAlpha = pillA;
    roundRect(ctx, CX - 480, py, 960, 56, 28);
    ctx.fillStyle = hex2rgba(pill.color, 0.12); ctx.fill();
    ctx.strokeStyle = pill.color; ctx.lineWidth = 1.5; ctx.stroke();
    setFont(ctx, 24, 400); ctx.fillStyle = pill.color;
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(pill.label, CX, py + 28);
    ctx.restore();
  }});

  drawEpLabel(ctx, p);
}}

const SCENE_BOUNDS = [
  {{ start: 0,    end: 9.5  }},
  {{ start: 9.5,  end: 22.5 }},
  {{ start: 22.5, end: 37.5 }},
  {{ start: 37.5, end: 60.0 }},
  {{ start: 60.0, end: 68.5 }},
  {{ start: 68.5, end: 999  }},
];
const SCENE_FNS = [drawScene1, drawScene2, drawScene3, drawScene4, drawScene5, drawScene6];

window.renderFrame = function(frameNum) {{
  const canvas = document.getElementById('c');
  const ctx = canvas.getContext('2d');
  const tSec = frameNum / 30;
  const t = tSec / TOTAL_DURATION;
  let sceneIdx = 0;
  for (let i = 0; i < SCENE_BOUNDS.length; i++) {{
    if (tSec >= SCENE_BOUNDS[i].start && tSec < SCENE_BOUNDS[i].end) {{ sceneIdx = i; break; }}
  }}
  SCENE_FNS[sceneIdx](ctx, t);
}};

// Preview
renderFrame(60);
</script>
</body>
</html>'''

with open('/tmp/k8s_ep9.html', 'w') as f:
    f.write(html)

print(f"Written /tmp/k8s_ep9.html ({len(html)} bytes)")
print(f"Total duration: {TOTAL}s, frames at 30fps: {int(TOTAL*30)+1}")
