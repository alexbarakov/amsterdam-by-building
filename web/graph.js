// The ontology graph: people, events and organisations, linked to the buildings (places) where a checked story ties
// them (pipeline/s13_graph.py). Select points and open their buildings on the map: ./?focus=<id>,<id>.
const TYPES = [
  { key: 'person', en: 'Residents', nl: 'Bewoners' },
  { key: 'architect', en: 'Architects', nl: 'Architecten' },
  { key: 'event', en: 'Events', nl: 'Gebeurtenissen' },
  { key: 'organisation', en: 'Organisations', nl: 'Organisaties' },
  { key: 'place', en: 'Buildings', nl: 'Gebouwen' },
];
const NL = {
  'Map': 'Kaart', 'Graph': 'Graaf', 'People, events and the buildings they touched': 'Mensen, gebeurtenissen en de gebouwen die ze raakten',
  'lede': 'Elke lijn is een gecontroleerd verhaal over een gebouw. Kies een of meer punten en open ze op de kaart.',
  'hint': 'Vierkantjes zijn gebouwen. Klik op een punt om het te kiezen; klik op meer om ze toe te voegen.',
  'Find a name': 'Zoek een naam', 'Clear': 'Wissen', 'Source': 'Bron',
  'Show {n} buildings on the map': 'Toon {n} gebouwen op de kaart', 'Show 1 building on the map': 'Toon 1 gebouw op de kaart',
  '{n} places': '{n} plekken', '1 place': '1 plek', 'Linked to': 'Verbonden met',
};
let LANG = (() => {
  const q = new URLSearchParams(location.search).get('lang');
  if (q === 'nl' || q === 'en') return q;
  try { const s = localStorage.getItem('lang'); if (s === 'nl' || s === 'en') return s; } catch {}
  return 'en';
})();
const EN = {
  'lede': 'Every line is a checked story about a building. Pick one or more points, then open them on the map.',
  'hint': 'Squares are buildings. Click a point to select it; click more to add them.',
};
const t = (s, n) => ((LANG === 'nl' && NL[s]) || EN[s] || s).replace('{n}', n);
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const COLOR = { person: '#1f3f9a', architect: '#0f8a7e', event: '#d0312d', organisation: '#c98a0f', place: '#7d858c' };
// The order points are selected in gives their colour on the map, as in the map's layers.
const SEL_COLORS = ['#ec0000', '#1f4e8c', '#d99a12', '#2e8b57', '#7b3fa0', '#00909a', '#8c5a2b', '#d6336c'];  // the map's GROUP_COLORS

fetch('data/graph.json').then(r => r.json()).then(init);

function init(G) {
  const nodes = [
    ...G.nodes.map(n => ({ ...n, kind: 'entity' })),
    ...Object.entries(G.places).map(([id, p]) => ({ id, type: 'place', kind: 'place', label: p.name, ...p })),
  ];
  const byId = new Map(nodes.map(n => [n.id, n]));
  // Tier 1: a point linked to four or more places; tier 2: two or three; tier 3: one.
  const tier = d => d.kind === 'place' ? 3 : d.deg >= 4 ? 1 : d.deg >= 2 ? 2 : 3;
  const r = d => d.kind === 'place' ? 0 : [0, Math.min(30, 9 + 3.4 * Math.sqrt(d.deg)), 8, 5.5][tier(d)];
  const links = G.links.map(l => ({ source: l.e, target: l.p, texts: l.texts }));
  for (const n of nodes) n.deg = 0;
  for (const l of links) { byId.get(l.source).deg++; byId.get(l.target).deg++; }
  const nbrs = new Map(nodes.map(n => [n.id, new Set()]));
  for (const l of links) { nbrs.get(l.source).add(l.target); nbrs.get(l.target).add(l.source); }

  const svg = d3.select('.g-svg');
  const root = svg.append('g');
  const linkSel = root.append('g').selectAll('line').data(links).join('line').attr('class', 'link');
  // Buildings are drawn first, so the people's and events' labels always sit on top of the squares.
  const drawOrder = [...nodes.filter(n => n.kind === 'place'), ...nodes.filter(n => n.kind !== 'place')];
  const nodeSel = root.append('g').selectAll('g').data(drawOrder).join('g')
    .attr('class', d => `node ${d.kind} t${tier(d)}${d.kind === 'place' && d.deg >= 3 ? ' big' : ''}`);
  // Size and label weight follow how many places a point touches: the hubs read first, the single links last.
  nodeSel.filter(d => d.kind === 'entity').append('circle').attr('r', r).attr('fill', d => COLOR[d.type]);
  nodeSel.filter(d => d.kind === 'place').append('rect')
    .attr('x', -3.5).attr('y', -3.5).attr('width', 7).attr('height', 7).attr('rx', 1.5).attr('fill', COLOR.place);
  nodeSel.append('text').attr('dx', d => d.kind === 'place' ? 8 : r(d) + 5).attr('dy', d => tier(d) === 1 ? 5 : 4);

  const W = () => innerWidth, H = () => innerHeight;
  const panelW = () => innerWidth > 720 ? 380 : 0;
  const sim = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(links).id(d => d.id).distance(l => 46 + 8 * Math.sqrt(l.source.deg || 1)).strength(.6))
    .force('charge', d3.forceManyBody().strength(d => d.kind === 'place' ? -60 : -300).distanceMax(260))
    .force('collide', d3.forceCollide(d => d.kind === 'place' ? 12 : r(d) + [0, 46, 30, 20][tier(d)]).strength(.9))
    .force('x', d3.forceX(0).strength(.12))
    .force('y', d3.forceY(0).strength(.16))
    .on('tick', () => {
      linkSel.attr('x1', d => d.source.x).attr('y1', d => d.source.y).attr('x2', d => d.target.x).attr('y2', d => d.target.y);
      nodeSel.attr('transform', d => `translate(${d.x},${d.y})`);
    });
  // Zoomed in well past the fitted view, the single links and all buildings get their labels too.
  let homeK = 1;
  const zoom = d3.zoom().scaleExtent([.3, 4]).on('zoom', e => {
    root.attr('transform', e.transform);
    svg.classed('close', e.transform.k >= homeK * 1.5);
  });
  svg.call(zoom).on('dblclick.zoom', null);
  // The graph is laid out around 0,0; the view centres it in the space right of the panel.
  // Lay the graph out before it is shown, then fit it into the space right of the panel.
  sim.stop();
  for (let i = 0; i < 600; i++) sim.tick();
  sim.on('tick')();
  const home = () => {
    // the box of the dots and of the labels that are drawn, so no name runs off the screen
    let [x0, x1, y0, y1] = [Infinity, -Infinity, Infinity, -Infinity];
    nodeSel.each(function (n) {
      x0 = Math.min(x0, n.x - r(n)); x1 = Math.max(x1, n.x + r(n)); y0 = Math.min(y0, n.y - r(n)); y1 = Math.max(y1, n.y + r(n));
      const el = this.querySelector('text');
      if (!el || el.classList.contains('clash') || getComputedStyle(el).display === 'none') return;
      const bb = el.getBBox();
      x1 = Math.max(x1, n.x + bb.x + bb.width); x0 = Math.min(x0, n.x + bb.x); y0 = Math.min(y0, n.y + bb.y);
    });
    // a phone gets the whole graph on screen, smaller; a wide screen keeps it readable and leaves room for labels
    const wide = innerWidth > 720;
    const sheet = document.querySelector('.g-panel')?.getBoundingClientRect();
    const top = 70, bottom = wide ? 20 : sheet && sheet.top > innerHeight * .3 ? innerHeight - sheet.top + 12 : innerHeight * .46, left = wide ? panelW() + 20 : 12, right = wide ? 140 : 12;
    const k = Math.max(wide ? .7 : .3, Math.min(1.2, (W() - left - right) / (x1 - x0 + 1), (H() - top - bottom) / (y1 - y0 + 1)));
    homeK = k;
    return d3.zoomIdentity.translate(left + (W() - left - right - k * (x1 + x0)) / 2 + k * 0, top + (H() - top - bottom - k * (y1 + y0)) / 2).scale(k);
  };
  svg.call(zoom.transform, home());
  nodeSel.call(d3.drag()
    .on('start', (e, d) => { if (!e.active) sim.alphaTarget(.2).restart(); d.fx = d.x; d.fy = d.y; })
    .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on('end', (e, d) => { if (!e.active) sim.alphaTarget(0); d.fx = null; d.fy = null; }));

  // ---------- state ----------
  const shown = { person: true, architect: true, event: true, organisation: true, place: true };
  let selected = (new URLSearchParams(location.search).get('select') || '').split(',').filter(id => byId.has(id));
  let query = '';
  const label = n => n.kind === 'place' ? n.name : (LANG === 'nl' && n.label_nl) || n.label;

  function render() {
    nodeSel.select('text').text(label);
    const vis = n => shown[n.type];
    nodeSel.classed('hidden', d => !vis(d));
    linkSel.classed('hidden', d => !vis(d.source) || !vis(d.target));
    // Focus: the selection and its neighbours, or the names that match the search.
    const near = new Set();
    for (const id of selected) { near.add(id); nbrs.get(id).forEach(x => near.add(x)); }
    if (query) nodes.filter(n => label(n).toLowerCase().includes(query)).forEach(n => { near.add(n.id); nbrs.get(n.id).forEach(x => near.add(x)); });
    const focused = near.size > 0;
    svg.classed('focused', focused);
    nodeSel.classed('near', d => near.has(d.id)).classed('selected', d => selected.includes(d.id));
    nodeSel.filter(d => d.kind === 'entity').select('circle')
      .attr('fill', d => selected.includes(d.id) ? SEL_COLORS[selected.indexOf(d.id) % SEL_COLORS.length] : COLOR[d.type]);
    linkSel.classed('near', d => (selected.includes(d.source.id) || selected.includes(d.target.id)) ||
      (query && near.has(d.source.id) && near.has(d.target.id)));
    renderTypes(); renderSelection(); renderEvidence();
    const u = new URL(location.href);
    if (selected.length) u.searchParams.set('select', selected.join(',')); else u.searchParams.delete('select');
    history.replaceState(null, '', u);
  }

  // Labels that would overlap a more important label or a hub's dot are dropped (they come back on hover, when
  // selected or close up). Greedy, most important first; the layout is static, so this runs once per language.
  function declutter() {
    const order = nodes.filter(n => shown[n.type]).sort((a, b) => tier(a) - tier(b) || b.deg - a.deg);
    const boxes = nodes.filter(n => n.kind === 'entity' && tier(n) === 1)
      .map(n => [n.x - r(n), n.y - r(n), n.x + r(n), n.y + r(n), n.id]);
    const hit = (a, b) => a[0] < b[2] && a[2] > b[0] && a[1] < b[3] && a[3] > b[1];
    nodeSel.each(function (d) { d._text = this.querySelector('text'); });
    for (const n of order) {
      const el = n._text;
      const shownNow = getComputedStyle(el).display !== 'none';
      el.classList.remove('clash');
      if (!shownNow) continue;
      const bb = el.getBBox();
      const box = [n.x + bb.x - 2, n.y + bb.y - 1, n.x + bb.x + bb.width + 2, n.y + bb.y + bb.height + 1, n.id];
      // every label, a hub's too, gives way to a more important label and to any hub's dot but its own
      if (boxes.some(b => b[4] !== n.id && hit(box, b))) el.classList.add('clash');
      else boxes.push(box);
    }
  }

  function renderTypes() {
    const box = document.querySelector('.g-types');
    box.innerHTML = TYPES.map(ty => `<button data-type="${ty.key}" aria-pressed="${shown[ty.key]}">
      <i class="${ty.key === 'place' ? 'place' : ''}" style="background:${COLOR[ty.key]}"></i>${ty[LANG]}
      <span>${nodes.filter(n => n.type === ty.key).length}</span></button>`).join('');
    box.querySelectorAll("button").forEach(b => b.onclick = () => { shown[b.dataset.type] = !shown[b.dataset.type]; render(); declutter(); });
  }

  // The buildings of the selection: an entity brings the places it is linked to, a place brings itself.
  function bagsOf(id) {
    const n = byId.get(id);
    if (n.kind === 'place') return n.bags;
    return [...nbrs.get(id)].flatMap(p => byId.get(p).bags || []);
  }
  function renderSelection() {
    const sec = document.querySelector('.g-selection');
    sec.hidden = !selected.length;
    if (!selected.length) return;
    sec.querySelector('.g-chips').innerHTML = selected.map((id, i) =>
      `<li><button data-id="${esc(id)}" style="background:${SEL_COLORS[i % SEL_COLORS.length]}">${esc(label(byId.get(id)))}</button></li>`).join('');
    sec.querySelectorAll('.g-chips button').forEach(b => b.onclick = () => toggle(b.dataset.id));
    const n = new Set(selected.flatMap(bagsOf)).size;
    const open = sec.querySelector('.g-open');
    open.textContent = t(n === 1 ? 'Show 1 building on the map' : 'Show {n} buildings on the map', n);
    open.href = `./?focus=${encodeURIComponent(selected.join(','))}${LANG === 'nl' ? '&lang=nl' : ''}`;
  }

  function renderEvidence() {
    const box = document.querySelector('.g-evidence');
    box.innerHTML = selected.map(id => {
      const n = byId.get(id);
      if (n.kind === 'place') {
        const ents = [...nbrs.get(id)].map(e => byId.get(e));
        return `<h2>${esc(n.name)} <small>${n.year}</small></h2>
          <p class="g-lede">${t('Linked to')}: ${ents.map(e => `<button class="g-link" data-id="${e.id}">${esc(label(e))}</button>`).join(', ')}</p>`;
      }
      const places = [...nbrs.get(id)].map(p => byId.get(p));
      const items = places.map(p => {
        const l = links.find(l => l.source.id === id && l.target.id === p.id);
        const txt = l.texts.map(x => `<p>${esc(LANG === 'nl' && x.text_nl ? x.text_nl : x.text)} <a href="${esc(x.source)}" target="_blank" rel="noopener">${t('Source')}</a></p>`).join('');
        return `<li>${p.photo ? `<img src="${esc(p.photo)}" alt="">` : '<span class="ph"></span>'}
          <div><button data-id="${p.id}"><b>${esc(p.name)}</b></button>${txt}</div></li>`;
      }).join('');
      return `<h2>${esc(label(n))} <small>${esc(n.years || '')} · ${t(places.length === 1 ? '1 place' : '{n} places', places.length)}</small></h2><ul>${items}</ul>`;
    }).join('');
    box.querySelectorAll('[data-id]').forEach(b => b.onclick = () => toggle(b.dataset.id));
  }

  function toggle(id) {
    selected = selected.includes(id) ? selected.filter(x => x !== id) : [...selected, id];
    render();
  }
  nodeSel.on('click', (e, d) => { e.stopPropagation(); toggle(d.id); });
  svg.on('click', () => { if (selected.length) { selected = []; render(); } });
  document.querySelector('.g-clear').onclick = () => { selected = []; render(); };
  const search = document.querySelector('.g-search');
  search.oninput = () => { query = search.value.trim().toLowerCase(); render(); };

  const tip = document.querySelector('.g-tip');
  nodeSel.on('mouseenter', (e, d) => {
    tip.innerHTML = `<b>${esc(label(d))}</b><span>${d.kind === 'place' ? d.year : esc(d.years || '')}${d.desc ? ' · ' + esc(d.desc) : ''}</span>`;
    tip.hidden = false;
  }).on('mousemove', e => { tip.style.left = e.clientX + 14 + 'px'; tip.style.top = e.clientY + 12 + 'px'; })
    .on('mouseleave', () => { tip.hidden = true; });

  function applyLang() {
    document.documentElement.lang = LANG;
    document.querySelectorAll('[data-i18n]').forEach(el => { el.textContent = t(el.dataset.i18n); });
    search.placeholder = t('Find a name');
    document.querySelectorAll('.g-lang button').forEach(b => b.setAttribute('aria-pressed', b.dataset.lang === LANG));
    document.querySelectorAll('.g-nav a').forEach(a => { const u = new URL(a.href); if (LANG === 'nl') u.searchParams.set('lang', 'nl'); else u.searchParams.delete('lang'); a.href = u; });
    render();
    declutter();
  }
  document.querySelectorAll('.g-lang button').forEach(b => b.onclick = () => {
    LANG = b.dataset.lang;
    try { localStorage.setItem('lang', LANG); } catch {}
    applyLang();
  });
  addEventListener('resize', () => svg.call(zoom.transform, home()));
  applyLang();
  svg.call(zoom.transform, home());  // again, now that crowded labels are hidden and the box is known
}
