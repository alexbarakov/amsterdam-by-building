import * as THREE from './vendor/three.module.js';
import { MapControls } from './vendor/MapControls.js';

// Colours are authored in sRGB and drawn as they are.
THREE.ColorManagement.enabled = false;

const SKY = '#e4e8ea';
const LAND = '#f4f3ef';
const WATER = '#b5c7c6';
const MAQUETTE = '#efeee9';
const GROUP_COLORS = ['#ec0000', '#1f4e8c', '#d99a12', '#2e8b57', '#7b3fa0', '#00909a', '#8c5a2b', '#d6336c'];
const MAX_GROUPS = GROUP_COLORS.length;
const ATTR_W = 256;
const WORKERS = Math.min(4, navigator.hardwareConcurrency || 2);
const MODE = { period: 0, floors: 1, energy: 2, layers: 3 };
// Energy labels G … A+++++ (index 1–12; 0 = no label), from red through yellow to deep green.
const ENERGY_COLORS = ['#efeee9', '#c1272d', '#e4572e', '#f08a24', '#f6c445', '#c9d64a', '#8cc152', '#4caf50',
  '#2e9a49', '#1d8040', '#126b35', '#0b5a2c', '#064a24'];

const [config, layers, attrBuf] = await Promise.all([
  fetch('data/amsterdam.json').then(r => r.json()),
  fetch('data/layers.json').then(r => r.json()),
  fetch('data/attrs.bin').then(r => r.arrayBuffer()),
]);
const attrs = new DataView(attrBuf);

// ---------- Language ----------
// English and Dutch. Data carries `<field>_nl` next to each English text; the interface strings are below.
const NL_UI = {
  'steps': 'stappen',
  'Best': 'Beste',
  'Your points': 'Je punten',
  'pts': 'pnt',
  'Find buildings from riddles and old photos, point to them on the map, guess their age with the colours switched off. Up to 100 points an answer; hints cost points.': 'Vind gebouwen aan de hand van raadsels en oude foto’s, wijs ze aan op de kaart, raad hun leeftijd met de kleuren uit. Tot 100 punten per antwoord; hints kosten punten.',
  'Score to beat': 'Te verslaan',
  'A photo of the building': 'Een foto van het gebouw',
  'Tap the map where you think it stands.': 'Tik op de kaart waar je denkt dat het staat.',
  'Spot on.': 'Precies raak.',
  'off': 'ernaast',
  'Shown, not found: no points.': 'Getoond, niet gevonden: geen punten.',
  'Challenge a friend': 'Daag iemand uit',
  'Link copied': 'Link gekopieerd',
  'You beat your friend': 'Je wint',
  'A draw with your friend': 'Gelijkspel',
  'Your friend wins this time': 'Deze keer wint de ander',
  'Quests': 'Speurtochten',
  'Easy': 'Makkelijk',
  'Medium': 'Gemiddeld',
  'Hard': 'Moeilijk',
  'Start': 'Begin',
  'Continue': 'Verder',
  'Play again': 'Opnieuw',
  
  'Find buildings from riddles and old photos, guess their age with the colours switched off. Every answer is worth three crosses; hints and wrong answers cost one.': 'Vind gebouwen aan de hand van raadsels en oude foto’s, raad hun leeftijd met de kleuren uit. Elk antwoord is drie kruisjes waard; hints en foute antwoorden kosten er een.',
  'Your crosses': 'Je kruisjes',
  'Look inside the red circle.': 'Kijk binnen de rode cirkel.',
  'Find it on the map and click it.': 'Zoek het op de kaart en klik erop.',
  'Hint': 'Hint',
  'Colour by floors': 'Kleur naar verdiepingen',
  'Colour by period': 'Kleur naar periode',
  'Show me': 'Laat zien',
  'Your guess': 'Jouw gok',
  'Guess': 'Raad',
  'A photo of the building to find': 'Een foto van het gebouw dat je zoekt',
  'Built': 'Gebouwd',
  'Exactly right.': 'Precies goed.',
  'year off': 'jaar ernaast',
  'years off': 'jaar ernaast',
  'Shown, not found: no crosses.': 'Getoond, niet gevonden: geen kruisjes.',
  'Full marks.': 'Alle kruisjes.',
  'See the result': 'Bekijk het resultaat',
  'Next': 'Volgende',
  'Open its card': 'Open de kaart van het gebouw',
  'Not that one.': 'Die niet.',
  'A true Amsterdammer.': 'Een echte Amsterdammer.',
  'You know your way around.': 'Je weet de weg.',
  'A good walk.': 'Een mooie wandeling.',
  'Time for a walk through town.': 'Tijd voor een wandeling door de stad.',
  'Copy result': 'Kopieer resultaat',
  'Copied': 'Gekopieerd',
  'More quests': 'Meer speurtochten',
  'Not this one, but right next to it.': 'Deze niet, maar het staat ernaast.',
  'Not this one. Very warm.': 'Deze niet. Heel warm.',
  'Not this one. A few streets away.': 'Deze niet. Een paar straten verderop.',
  'Not this one. Far off.': 'Deze niet. Ver weg.',
  'Warmer than before.': 'Warmer dan net.',
  'Colder than before.': 'Kouder dan net.',
  'Every building standing today, by age and historical context.': 'Elk gebouw dat er nu staat, naar leeftijd en historische context.',
  'About': 'Over', 'Did you know': 'Wist je dat', 'Today': 'Nu', 'Earlier': 'Eerder', 'Later': 'Later', 'This photo did not load.': 'Deze foto laadde niet.', 'Open it in the archive': 'Open hem in het archief', 'Add a layer on GitHub': 'Voeg een laag toe op GitHub',
  'Wikidata records this building as their residence.': 'Volgens Wikidata woonde deze persoon hier.',
  'Wikidata records this building as their place of work.': 'Volgens Wikidata werkte deze persoon hier.',
  'Wikidata records this building as their birthplace.': 'Volgens Wikidata werd deze persoon hier geboren.',
  'Wikidata records this building as the place where they died.': 'Volgens Wikidata overleed deze persoon hier.',
  'Period': 'Periode', 'Layers': 'Lagen', 'Floors': 'Verdiepingen', 'Energy': 'Energie',
  'buildings': 'gebouwen', 'Building the city': 'De stad wordt gebouwd',
  'Drag to turn. Right-drag or Shift-drag to move. Scroll to zoom.': 'Sleep om te draaien. Rechts slepen of Shift-slepen om te verschuiven. Scroll om te zoomen.',
  'Show legend': 'Legenda tonen', 'Hide legend': 'Legenda verbergen', 'Legend': 'Legenda',
  'Built in': 'Gebouwd in', 'Click a period to see it alone. Paler buildings have an approximate year.': 'Klik op een periode om alleen die te zien. Lichtere gebouwen hebben een geschat bouwjaar.',
  'Storeys': 'Verdiepingen', 'Energy label': 'Energielabel',
  'RVO energy labels, via Atlas Leefomgeving': 'Energielabels van RVO, via Atlas Leefomgeving',
  'All layers': 'Alle lagen', 'Find a person': 'Zoek een persoon', 'Buildings and their stories': 'Gebouwen en hun verhalen',
  'Height': 'Hoogte', 'from the 3D BAG model': 'uit het 3D BAG-model', 'height ÷ 3.2 m': 'hoogte ÷ 3,2 m',
  'Architect': 'Architect', 'Architects': 'Architecten', 'Style': 'Stijl', 'National monument': 'Rijksmonument',
  'In layers': 'In lagen', 'Dating': 'Datering', 'Read more': 'Meer lezen', 'From the street': 'Vanaf de straat',
  'Lived or worked here': 'Woonde of werkte hier', 'Source': 'Bron', 'Photo': 'Foto', 'Street view': 'Straatbeeld',
  'Wikipedia': 'Wikipedia', 'Dutch Wikipedia': 'Nederlandstalige Wikipedia', 'Monument register': 'Monumentenregister',
  'BAG register': 'BAG-register', 'BAG gives': 'De BAG geeft',
  'Click for the story and sources': 'Klik voor het verhaal en de bronnen', 'Click to keep this card open': 'Klik om deze kaart open te houden',
  'Play the city\'s growth': 'Speel de groei van de stad af', 'Pause': 'Pauze', 'Close': 'Sluiten',
  'The register gives a round year here, more often than neighbouring years predict. Read it as “around then”.': 'Het register geeft hier een rond jaartal, vaker dan de omliggende jaren doen verwachten. Lees het als ‘rond die tijd’.',
  'The register has no real year (placeholder 1005, or one of the surplus 1905s of the old centre). Estimated from the nearest dated buildings.': 'Het register heeft geen echt jaartal (de plaatshouder 1005, of een van de overtollige 1905’s in het oude centrum). Geschat uit de dichtstbijzijnde gedateerde gebouwen.',
  'Year from the register of national monuments, which dates the building earlier than BAG does.': 'Jaartal uit het rijksmonumentenregister, dat het gebouw eerder dateert dan de BAG.',
  'Dated by the register of national monuments to a century or part of one; the map spreads it across that span.': 'Door het rijksmonumentenregister gedateerd op een eeuw of een deel daarvan; de kaart spreidt het over die periode.',
  'Year from Wikidata, which dates the building earlier than BAG does; the register of national monuments gives no date.': 'Jaartal uit Wikidata, dat het gebouw eerder dateert dan de BAG; het rijksmonumentenregister geeft geen datering.',
  'Before 1600': 'Vóór 1600', '1600–1665 Canal ring': '1600–1665 Grachtengordel', '1870–1913 Nineteenth-century belt': '1870–1913 Negentiende-eeuwse gordel',
  '1914–1940 Amsterdam School': '1914–1940 Amsterdamse School', '1941–1964 Garden cities': '1941–1964 Tuinsteden', '1965–1984 Bijlmer era': '1965–1984 Bijlmertijd',
  '1985–1999 Eastern docks': '1985–1999 Oostelijk Havengebied', '2000– IJburg, Zuidas, Noord': '2000– IJburg, Zuidas, Noord',
  'Layers': 'Lagen',
  'All layers': 'Alle lagen',
  'A building already stood on this footprint in the 1832 land register. BAG’s year may record a rebuilding, or this house replaced the older one.': 'Op deze plek stond al een gebouw in het kadaster van 1832. Het jaartal van de BAG kan een verbouwing zijn, of dit huis verving het oudere.',
  'Walk': 'Wandeling',
  'Plan a walk': 'Plan een wandeling',
  'Your walk': 'Jouw wandeling',
  'Choose what interests you, where you start and how far you want to go. The walk links the buildings with stories on the way.': 'Kies wat je interesseert, waar je begint en hoe ver je wilt lopen. De wandeling verbindt de gebouwen met een verhaal onderweg.',
  'What interests you': 'Wat interesseert je',
  'Where you start': 'Waar je begint',
  'How far': 'Hoe ver',
  'Nothing chosen: the walk takes every story.': 'Niets gekozen: de wandeling neemt alle verhalen mee.',
  'My location': 'Mijn locatie',
  'Pick on the map': 'Kies op de kaart',
  'Your location': 'Jouw locatie',
  'Point on the map': 'Punt op de kaart',
  'Your point': 'Jouw punt',
  'Back to the start': 'Terug naar het begin',
  'One way': 'Enkele reis',
  'Make my walk': 'Maak mijn wandeling',
  'Cancel': 'Annuleren',
  'Click the map where the walk should start.': 'Klik op de kaart waar de wandeling moet beginnen.',
  'This browser does not share its location.': 'Deze browser deelt geen locatie.',
  'You seem to be outside the city, so the walk starts at {s}.': 'Je lijkt buiten de stad te zijn, dus de wandeling begint bij {s}.',
  'The location was not shared. Pick a start on the map instead.': 'De locatie werd niet gedeeld. Kies het begin op de kaart.',
  'No stories within reach. Try a longer walk or more interests.': 'Geen verhalen binnen bereik. Probeer een langere wandeling of meer interesses.',
  'about {m} min': 'ongeveer {m} min',
  'Download the walk with its stories (KML), for Google My Maps: Create a new map, then Import.': 'Download de wandeling met verhalen (KML), voor Google Mijn kaarten: maak een nieuwe kaart en kies Importeren.',
  'Google Maps takes nine stops; the paler ones lie on the way.': 'Google Maps neemt negen stops; de lichtere liggen onderweg.',
  'Share my location': 'Deel mijn locatie',
  'Asking for your location…': 'Je locatie wordt gevraagd…',
  'Start from where you are: share your location, or choose a start below.': 'Begin waar je bent: deel je locatie, of kies hieronder een begin.',
  'Shorter than asked: the stories you chose lie close together.': 'Korter dan gevraagd: de verhalen die je koos liggen dicht bij elkaar.',
  'Longer than asked: few of the stories you chose lie that close.': 'Langer dan gevraagd: weinig van de gekozen verhalen liggen zo dichtbij.',
  'How many stops': 'Hoeveel stops',
  'As many as fit': 'Zoveel als past',
  'Fewer stops than asked: that is all the stories you chose.': 'Minder stops dan gevraagd: meer verhalen van je keuze zijn er niet.',
  'Open in Google Maps': 'Open in Google Maps',
  'Change': 'Wijzigen',
  'Straight lines on the map; Google Maps shows the walking route.': 'Rechte lijnen op de kaart; Google Maps toont de looproute.',
  'Buildings today': 'De gebouwen nu',
  'Generate a walk': 'Maak een wandeling',
  'Riddles hidden in the city. Find each building on the map, using its colours and layers, and click it. Every riddle is worth three tiles; hints cost one.': 'Raadsels verstopt in de stad. Zoek elk gebouw op de kaart, met de kleuren en lagen, en klik erop. Elk raadsel is drie tegeltjes waard; een hint kost er een.',
  'Your tiles': 'Jouw tegeltjes',
  'Open the layer': 'Open de laag',
  'Colour the map for it': 'Kleur de kaart ervoor',
  'Next riddle': 'Volgend raadsel',
  'Colour by energy label': 'Kleur naar energielabel',
  'See all quests': 'Alle speurtochten',
  'Found!': 'Gevonden!',
  'Right': 'Goed',
  'Without a single hint.': 'Zonder één hint.',
  'Quest complete': 'Speurtocht voltooid',
  'Any of {n} buildings counts.': 'Elk van {n} gebouwen telt.',
  'One of the buildings that answer the riddle.': 'Een van de gebouwen die het raadsel beantwoorden.',
  'Not this one, but very close.': 'Dit is hem niet, maar je bent er heel dichtbij.',
  'Not this one. You are getting warm.': 'Dit is hem niet. Je wordt warm.',
  'Not this one. Still a few streets away.': 'Dit is hem niet. Nog een paar straten verder.',
  'A hint may help.': 'Een hint kan helpen.',
  'Today’s photo of the building to find': 'Foto van vandaag van het gebouw dat je zoekt',
  'From the graph': 'Uit de graaf',
  'Back to the graph': 'Terug naar de graaf',
  'Graph': 'Graaf',
  'Search a building, address or street': 'Zoek een gebouw, adres of straat', 'Search': 'Zoeken', 'Address': 'Adres', 'Open in Google Maps': 'Open in Google Maps',
  'Building': 'Gebouw', 'Lived here': 'Woonde hier', 'Street': 'Straat', 'Nothing found': 'Niets gevonden', 'Clear': 'Wissen',
  '{n} is not in the register; nearest on the same side': '{n} staat niet in het register; het dichtstbijzijnde nummer aan dezelfde kant',
  'Before 1536': 'Vóór 1536',
  '1536–1653 After the great fire': '1536–1653 Na de stadsbrand',
  '1654–1799 After the thunderclap': '1654–1799 Na de Delftse donderslag',
  '1864–1913 Polytechnic and factories': '1864–1913 Polytechnische School en fabrieken',
};
let LANG = (() => {
  const q = new URLSearchParams(location.search).get('lang');
  if (q === 'nl' || q === 'en') return q;
  try { const s = localStorage.getItem('lang'); if (s === 'nl' || s === 'en') return s; } catch {}
  return navigator.language?.startsWith('nl') ? 'nl' : 'en';
})();
const t = s => (LANG === 'nl' && NL_UI[s]) || s;
const tr = (o, k) => (LANG === 'nl' && o?.[k + '_nl']) || o?.[k];
const fmtLocale = () => LANG === 'nl' ? 'nl-NL' : 'en';
const periods = config.periods;

// ---------- Scene ----------
const canvas = document.getElementById('scene');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.outputColorSpace = THREE.LinearSRGBColorSpace;
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.setClearColor(SKY);
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, 1, 5, 60000);
const controls = new MapControls(camera, canvas);
controls.enableDamping = true;
// Left drag turns and tilts the city; right drag, or Shift with the left, moves it.
controls.mouseButtons = { LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };
controls.rotateSpeed = 0.6;
controls.maxPolarAngle = Math.PI * 0.47;
controls.minDistance = 60;
controls.maxDistance = 30000;

function goHome() {
  const h = config.home, az = THREE.MathUtils.degToRad(h.azimuth), el = THREE.MathUtils.degToRad(h.elevation);
  const d = h.span * 0.9;
  controls.target.set(h.x, 0, h.z);
  camera.position.set(h.x + d * Math.cos(el) * Math.sin(az), d * Math.sin(el), h.z + d * Math.cos(el) * Math.cos(az));
  controls.update();
}
goHome();

// Land and water: flat polygons in the local frame (see pipeline/s04_water.py).
async function loadPolygons(url) {
  const buf = await (await fetch(url)).arrayBuffer();
  const [nPoly, nRing, nVert] = new Uint32Array(buf, 0, 3);
  const ringStart = new Uint32Array(buf, 12, nPoly + 1);
  const vertStart = new Uint32Array(buf, 12 + 4 * (nPoly + 1), nRing + 1);
  const xz = new Float32Array(buf, 12 + 4 * (nPoly + 1) + 4 * (nRing + 1), 2 * nVert);
  const ring = r => {
    const pts = [];
    for (let v = vertStart[r]; v < vertStart[r + 1]; v++) pts.push(new THREE.Vector2(xz[2 * v], -xz[2 * v + 1]));
    return pts;
  };
  const shapes = [];
  for (let p = 0; p < nPoly; p++) {
    const shape = new THREE.Shape(ring(ringStart[p]));
    for (let r = ringStart[p] + 1; r < ringStart[p + 1]; r++) shape.holes.push(new THREE.Path(ring(r)));
    shapes.push(shape);
  }
  const g = new THREE.ShapeGeometry(shapes);
  g.rotateX(-Math.PI / 2);
  return g;
}
const flat = new THREE.Group();
scene.add(flat);
const [landGeo, waterGeo] = await Promise.all([loadPolygons('data/land.bin'), loadPolygons('data/water.bin')]);
const land = new THREE.Mesh(landGeo, new THREE.MeshBasicMaterial({ color: LAND }));
const water = new THREE.Mesh(waterGeo, new THREE.MeshBasicMaterial({ color: WATER }));
land.position.y = -0.05;
water.position.y = -0.4;
flat.add(land, water);

// ---------- Street and canal names ----------
// Flat on the ground, turned along the street (pipeline/s07_labels.py). Textures are drawn on first use.
const labelData = await fetch('data/labels.json').then(r => r.json());
const labelGroup = new THREE.Group();
scene.add(labelGroup);
const labelTex = new Map();
const LABEL_PX = 64;
function textureFor(L) {
  let t = labelTex.get(L.name + L.water);
  if (t) return t;
  const c = document.createElement('canvas'), ctx = c.getContext('2d');
  const font = `${L.water ? 'italic 500' : '500'} ${LABEL_PX * 0.62}px "Schibsted Grotesk", sans-serif`;
  ctx.font = font;
  c.width = Math.ceil(ctx.measureText(L.name).width + LABEL_PX * 0.4);
  c.height = LABEL_PX;
  ctx.font = font;
  ctx.textBaseline = 'middle';
  ctx.lineWidth = LABEL_PX * 0.12;
  ctx.strokeStyle = L.water ? 'rgba(181,199,198,0.85)' : 'rgba(244,243,239,0.85)';
  ctx.fillStyle = L.water ? '#3c6875' : '#50565b';
  ctx.strokeText(L.name, LABEL_PX * 0.2, LABEL_PX / 2);
  ctx.fillText(L.name, LABEL_PX * 0.2, LABEL_PX / 2);
  t = new THREE.CanvasTexture(c);
  t.anisotropy = 4;
  t.userData = { aspect: c.width / c.height };
  labelTex.set(L.name + L.water, t);
  return t;
}
const labelPlane = new THREE.PlaneGeometry(1, 1);
const labels = labelData.flatMap(L => L.pts.map(([x, z, ang, len, wid]) => ({ L, x, z, ang, len, wid: wid || 20, mesh: null })))
  .sort((a, b) => a.L.tier - b.L.tier || b.len - a.len);
function updateLabels(dist) {
  if (!document.fonts.check('500 16px "Schibsted Grotesk"')) return;
  // Label height in metres, roughly constant on screen; the canals and main streets read larger.
  const h1 = THREE.MathUtils.clamp(dist * 0.014, 4, 44), h2 = THREE.MathUtils.clamp(dist * 0.01, 3, 15);
  // Names appear only when the camera comes close: canals and main streets first, the rest closer still.
  const near = dist * 1.2, far = dist * 2;
  // Greedy collision: canals and main streets first, then the longest stretches; a label is dropped
  // when an accepted one already sits within a few label heights of it.
  const taken = new Map(), C = h1 * 5; // one grid, cells as wide as the largest separation
  const cellOf = (x, z) => `${Math.floor(x / C)},${Math.floor(z / C)}`;
  const clear = (l, sep) => {
    const cx = Math.floor(l.x / C), cz = Math.floor(l.z / C);
    for (let i = -1; i <= 1; i++) for (let j = -1; j <= 1; j++) {
      for (const q of taken.get(`${cx + i},${cz + j}`) || []) if ((q.x - l.x) ** 2 + (q.z - l.z) ** 2 < sep * sep) return false;
    }
    return true;
  };
  for (const l of labels) {
    const d = Math.hypot(l.x - camera.position.x, l.z - camera.position.z);
    let show = d < (l.L.tier === 1 ? far : near) && dist < (l.L.tier === 1 ? 3200 : 1300);
    const sep = (l.L.tier === 1 ? h1 : h2) * 5;
    if (show && !clear(l, sep)) show = false;
    if (show) {
      const key = cellOf(l.x, l.z);
      if (!taken.has(key)) taken.set(key, []);
      taken.get(key).push(l);
    }
    if (show && !l.mesh) {
      const tex = textureFor(l.L);
      l.mesh = new THREE.Mesh(labelPlane, new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }));
      // Turn about the vertical first, then lay the plane flat.
      l.mesh.rotation.set(-Math.PI / 2, THREE.MathUtils.degToRad(-l.ang), 0, "YXZ"); // ang is measured towards +z, Y turns towards -z
      l.mesh.position.set(l.x, l.L.water ? 0.4 : 0.6, l.z);
      l.mesh.renderOrder = 2;
      labelGroup.add(l.mesh);
    }
    if (l.mesh) {
      // Never taller than the street or canal is wide, so a name stays off the buildings.
      const h = Math.min(l.L.tier === 1 ? h1 : h2, l.wid * 0.55);
      const w = h * l.mesh.material.map.userData.aspect;
      // A name much longer than its stretch of street would spill over the buildings.
      if (show && (w > l.len * 1.1 || h < 2.5)) show = false;
      l.mesh.visible = show;
      if (show) l.mesh.scale.set(w, h, 1);
    }
  }
}

// ---------- Shared uniforms ----------
const col = c => new THREE.Color(c);
const FOCUS_MAX = 160;  // buildings a walk can light up at once
const uniforms = {
  uYear: { value: config.yearMax },
  uYearFrom: { value: config.yearMin - 1 },
  uMode: { value: MODE.period },
  uPalette: { value: periods.map(p => col(p.color)) },
  uMask: { value: periods.map(() => 1) },
  uNow: { value: 0 },                              // seconds, for tiles dropping in as they load
  uPlaying: { value: 0 },                          // while the film plays buildings fly in rather than grow
  uRise: { value: 0.01 },
  uLayerAt: { value: -10 },                        // seconds; when a context layer opened, its buildings rise                          // years a building's entrance spans; only the film widens it
  uGroupBit: { value: Array(MAX_GROUPS).fill(-1) },
  uGroupColor: { value: GROUP_COLORS.map(col) },
  uMaquette: { value: col(MAQUETTE) },
  uEnergy: { value: ENERGY_COLORS.map(col) },
  uHover: { value: -1 },
  uSelected: { value: -1 },
  uFocus: { value: Array(FOCUS_MAX).fill(-1) },
  uFocusGroup: { value: Array(FOCUS_MAX).fill(0) },
  uFocusN: { value: 0 },
  uBlind: { value: 0 },
  // Search: per building whether it is lit; while uPickOn is 1 the found buildings keep their colour and the rest dims.
  uPick: { value: null },
  uPickOn: { value: 0 },
  uFogColor: { value: col(SKY) },
  uFog: { value: new THREE.Vector2(9000, 26000) },
};

const PICK_ROWS = Math.ceil(config.stats.buildings / ATTR_W);
const pickData = new Uint8Array(ATTR_W * PICK_ROWS * 4);
const pickTex = new THREE.DataTexture(pickData, ATTR_W, PICK_ROWS, THREE.RGBAFormat, THREE.UnsignedByteType);
pickTex.needsUpdate = true;
uniforms.uPick.value = pickTex;

const VERT = /* glsl */`
  in float bld;
  uniform sampler2D uAttr;
  uniform float uYear, uYearFrom, uMode, uHover, uSelected, uBlind, uNow, uBorn, uPlaying, uRise, uLayerAt;
  uniform vec3 uPalette[${periods.length}];
  uniform float uMask[${periods.length}];
  uniform int uGroupBit[${MAX_GROUPS}];
  uniform vec3 uGroupColor[${MAX_GROUPS}];
  uniform vec3 uMaquette;
  uniform vec3 uEnergy[13];
  uniform float uFocus[${FOCUS_MAX}];
  uniform int uFocusGroup[${FOCUS_MAX}];
  uniform int uFocusN;
  uniform sampler2D uPick;
  uniform float uPickOn;
  out vec3 vColor;
  out vec3 vWorld;
  out float vGid;

  vec3 floorsRamp(float f) {
    float t = clamp(log(f) / log(40.0), 0.0, 1.0);
    vec3 a = vec3(0.86, 0.89, 0.90), b = vec3(0.49, 0.66, 0.75), c = vec3(0.17, 0.36, 0.55), d = vec3(0.05, 0.10, 0.25);
    return t < 0.33 ? mix(a, b, t / 0.33) : t < 0.66 ? mix(b, c, (t - 0.33) / 0.33) : mix(c, d, (t - 0.66) / 0.34);
  }

  bool hasBit(vec4 words, int bit) {
    int w = bit / 16;
    float v = w == 0 ? words.x : w == 1 ? words.y : w == 2 ? words.z : words.w;
    return ((int(v + 0.5) >> (bit - w * 16)) & 1) == 1;
  }

  void main() {
    int i = int(bld + 0.5);
    ivec2 tc = ivec2(2 * (i % ${ATTR_W}), i / ${ATTR_W});
    vec4 a = texelFetch(uAttr, tc, 0);
    vec4 lay = texelFetch(uAttr, tc + ivec2(1, 0), 0);
    float year = a.x;
    int pf = int(a.y + 0.5);
    int period = pf % 16;
    int flag = pf / 16;
    vGid = a.w;
    float vis = uMode < 1.5 ? uMask[period] : 1.0;
    float g = clamp((uYear - year + 1.0) / uRise, 0.0, 1.0);
    g = g * g * (3.0 - 2.0 * g);
    if (g <= 0.003 || vis <= 0.003) { gl_Position = vec4(2.0, 2.0, 2.0, 1.0); return; }

    // Entrances, only while the film plays and while tiles load: a building drops in from its own side of the
    // sky, the same side every time (seeded by its id). Filters and scrubbing change the city at once.
    vec3 p = position;
    float seed = fract(sin(a.w * 12.9898) * 43758.5453);
    float arrive = clamp((uNow - uBorn) / 0.9 - seed * 0.35, 0.0, 1.0);
    float fly = 1.0 - arrive;
    if (uPlaying > 0.5) fly = max(fly, 1.0 - g);
    if (fly > 0.0) {
      float e = fly * fly * fly;
      float ang = seed * 6.2831853;
      // positions are in decimetres: a few hundred metres sideways and up
      p += vec3(cos(ang), 0.0, sin(ang)) * (1800.0 + 1600.0 * fract(seed * 7.13)) * e;
      p.y += (2600.0 + 2400.0 * fract(seed * 3.71)) * e;
    }
    vec3 c;
    if (uMode < 0.5) {
      c = uPalette[period];
      if (flag == 1 || flag == 2 || flag == 4) c = mix(c, uMaquette, 0.45);
    } else if (uMode < 1.5) {
      c = floorsRamp(mod(a.z, 128.0));
    } else if (uMode < 2.5) {
      c = uEnergy[int(a.z / 128.0)];
    } else {
      c = uMaquette;
      for (int g = 0; g < ${MAX_GROUPS}; g++) {
        if (uGroupBit[g] >= 0 && hasBit(lay, uGroupBit[g])) {
          c = uGroupColor[g];
          // Opening a layer: its buildings rise out of the ground in a quick wave, overshoot a little, settle.
          float k = clamp((uNow - uLayerAt) / 0.55 - seed * 0.6, 0.0, 1.0);
          float q = k - 1.0;
          p.y *= 1.0 + 2.70158 * q * q * q + 1.70158 * q * q;
          break;
        }
      }
    }
    if (uFocusN > 0) {
      c = uMaquette;
      for (int k = 0; k < ${FOCUS_MAX}; k++) {
        if (k >= uFocusN) break;
        if (abs(vGid - uFocus[k]) < 0.5) { c = uGroupColor[uFocusGroup[k]]; break; }
      }
    }
    if (year <= uYearFrom) c = mix(c, uMaquette, 0.8);
    // A quest's question about one building turns it red; a year riddle also hides every other age.
    if (uBlind > 0.5 && vGid == uSelected) c = vec3(0.925, 0.0, 0.0);
    else if (uBlind > 0.5 && uBlind < 1.5) c = uMaquette;
    if (vGid == uHover || (vGid == uSelected && uBlind < 0.5)) c = mix(c, vec3(0.0), 0.35);
    if (uPickOn > 0.5) {
      int gi = int(vGid + 0.5);
      if (texelFetch(uPick, ivec2(gi % ${ATTR_W}, gi / ${ATTR_W}), 0).x < 0.5) c = mix(c, uMaquette, 0.78);
    }
    vColor = c;
    vec4 w = modelMatrix * vec4(p, 1.0);
    vWorld = w.xyz;
    gl_Position = projectionMatrix * viewMatrix * w;
  }
`;

const FRAG = /* glsl */`
  precision highp float;
  uniform vec3 uFogColor;
  uniform vec2 uFog;
  in vec3 vColor;
  in vec3 vWorld;
  in float vGid;
  out vec4 outColor;
  void main() {
    #ifdef PICK
      float id = vGid + 1.0;
      outColor = vec4(mod(id, 256.0), mod(floor(id / 256.0), 256.0), floor(id / 65536.0), 255.0) / 255.0;
    #else
      vec3 n = normalize(cross(dFdx(vWorld), dFdy(vWorld)));
      // Low afternoon sun from the south-west, a soft sky from above.
      float sun = max(dot(n, normalize(vec3(-0.55, 0.55, 0.62))), 0.0);
      float light = n.y > 0.9 ? 1.04 : 0.66 + 0.34 * sun;
      float foot = mix(0.82, 1.0, clamp(vWorld.y / 12.0, 0.0, 1.0));
      vec3 c = vColor * light * foot;
      float d = length(vWorld - cameraPosition);
      c = mix(c, uFogColor, smoothstep(uFog.x, uFog.y, d));
      outColor = vec4(c, 1.0);
    #endif
  }
`;

function makeMaterial(tex, pick, born) {
  return new THREE.ShaderMaterial({
    glslVersion: THREE.GLSL3,
    uniforms: { ...uniforms, uAttr: { value: tex }, uBorn: born },
    vertexShader: VERT,
    fragmentShader: FRAG,
    defines: pick ? { PICK: 1 } : {},
    side: THREE.DoubleSide,
  });
}

// ---------- Tiles ----------
const meshes = [];
let loaded = 0;
const queue = [...config.tiles];
const pool = Array.from({ length: WORKERS }, () => new Worker('worker.js', { type: 'module' }));

function addTile(m) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(m.pos, 3));
  g.setAttribute('bld', new THREE.BufferAttribute(m.bld, 1));
  g.setIndex(new THREE.BufferAttribute(m.idx, 1));
  const rows = Math.ceil(m.nB / ATTR_W);
  const data = new Float32Array(ATTR_W * 2 * rows * 4);
  data.set(m.attr);
  const tex = new THREE.DataTexture(data, ATTR_W * 2, rows, THREE.RGBAFormat, THREE.FloatType);
  tex.needsUpdate = true;
  const born = { value: performance.now() / 1000 };
  const mesh = new THREE.Mesh(g, makeMaterial(tex, false, born));
  mesh.userData = { draw: mesh.material, pick: makeMaterial(tex, true, born) };
  mesh.scale.setScalar(0.1);
  mesh.position.set(m.origin[0], 0, m.origin[1]);
  scene.add(mesh);
  meshes.push(mesh);
}

// Tiles come in packs (see pipeline/s03_tiles.py); a tile is ready once its pack has arrived.
const packs = Object.fromEntries(config.packs.map(name => [name, fetch(`data/${name}`).then(r => r.arrayBuffer())]));
for (const w of pool) {
  const next = async () => {
    const t = queue.shift();
    if (!t) return;
    const buf = (await packs[t.pack]).slice(t.offset, t.offset + t.length);
    w.postMessage({ buf, id: t.file }, [buf]);
  };
  w.onmessage = ({ data }) => {
    addTile(data);
    loaded++;
    document.getElementById('progress').textContent = Math.round(100 * loaded / config.tiles.length);
    if (loaded === config.tiles.length) { document.getElementById('loading').hidden = true; cityReady(); openDeepLink(); }
    next();
  };
  next();
}

// ---------- Picking ----------
const pickTarget = new THREE.WebGLRenderTarget(1, 1);
const pickPixel = new Uint8Array(4);
function pick(x, y) {
  const w = renderer.domElement.clientWidth, h = renderer.domElement.clientHeight;
  camera.setViewOffset(w, h, x, y, 1, 1);
  for (const m of meshes) m.material = m.userData.pick;
  flat.visible = false;
  labelGroup.visible = false;
  renderer.setRenderTarget(pickTarget);
  renderer.setClearColor(0x000000, 0);
  renderer.clear();
  renderer.render(scene, camera);
  renderer.readRenderTargetPixels(pickTarget, 0, 0, 1, 1, pickPixel);
  renderer.setRenderTarget(null);
  renderer.setClearColor(SKY, 1);
  flat.visible = true;
  labelGroup.visible = true;
  for (const m of meshes) m.material = m.userData.draw;
  camera.clearViewOffset();
  return pickPixel[0] + pickPixel[1] * 256 + pickPixel[2] * 65536 - 1;
}

// ---------- Building lookup ----------
const DATE_NOTE = [
  null,
  'The register gives a round year here, more often than neighbouring years predict. Read it as “around then”.',
  'The register has no real year (placeholder 1005, or one of the surplus 1905s of the old centre). Estimated from the nearest dated buildings.',
  'Year from the register of national monuments, which dates the building earlier than BAG does.',
  'Dated by the register of national monuments to a century or part of one; the map spreads it across that span.',
  'Year from Wikidata, which dates the building earlier than BAG does; the register of national monuments gives no date.',
];
const residentsLayer = layers.find(L => L.id === 'residents');
const contextLayers = layers;
// The card shows residents in their own section, so they are left out of its list of layers.
const groupsByBit = layers.filter(L => L !== residentsLayer).flatMap(L => L.groups.map(g => ({ ...g, layer: L })));

function building(gid) {
  const o = gid * config.attrStride;
  const lay0 = attrs.getUint32(o + 20, true), lay1 = attrs.getUint32(o + 24, true);
  return {
    gid,
    bag: String(attrs.getFloat64(o, true)).padStart(16, '0'),
    height: attrs.getUint16(o + 8, true) / 10,
    fsrc: attrs.getUint8(o + 10),
    flag: attrs.getUint8(o + 11),
    year: attrs.getInt16(o + 12, true),
    orig: attrs.getInt16(o + 14, true),
    mon: attrs.getUint32(o + 16, true),
    wk: attrs.getInt32(o + 28, true),
    energy: attrs.getUint8(o + 32),
    x: attrs.getFloat32(o + 36, true),
    z: attrs.getFloat32(o + 40, true),
    groups: groupsByBit.filter(g => g.bit < 32 ? (lay0 >>> g.bit) & 1 : (lay1 >>> (g.bit - 32)) & 1),
  };
}

const periodOf = y => periods.find(p => y >= p.from && y <= p.to) || periods[0];

// ---------- Building card ----------
// Hover shows a light card that follows the pointer; a click pins it, with the article extract and links.
let wiki = [], didYouKnow = {};
fetch('data/wiki.json').then(r => r.json()).then(w => { wiki = w; });
fetch('data/facts.json').then(r => r.json()).then(f => { didYouKnow = f; }); // 'Did you know', checked in s11_facts
const esc = s => String(s ?? '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const link = (href, text) => `<a href="${esc(href)}" target="_blank" rel="noopener">${esc(text)}</a>`;

// Local metres → RD New → WGS84 (Schreutelkamp and Strang van Hees approximation, ~1 m).
function toLatLon(x, z) {
  const dX = (x + config.origin[0] - 155000) * 1e-5, dY = (config.origin[1] - z - 463000) * 1e-5;
  const lat = 52.15517440 + (3235.65389 * dY - 32.58297 * dX ** 2 - 0.2475 * dY ** 2 - 0.84978 * dX ** 2 * dY
    - 0.0655 * dY ** 3 - 0.01709 * dX ** 2 * dY ** 2 - 0.00738 * dX + 0.0053 * dX ** 4 - 0.00039 * dX ** 2 * dY ** 3
    + 0.00033 * dX ** 4 * dY - 0.00012 * dX * dY) / 3600;
  const lon = 5.38720621 + (5260.52916 * dX + 105.94684 * dX * dY + 2.45656 * dX * dY ** 2 - 0.81885 * dX ** 3
    + 0.05594 * dX * dY ** 3 - 0.05607 * dX ** 3 * dY + 0.01199 * dY - 0.00256 * dX ** 3 * dY ** 2
    + 0.00128 * dX * dY ** 4 + 0.00022 * dY ** 2 - 0.00022 * dX ** 2 + 0.00026 * dX ** 5) / 3600;
  return [lat, lon];
}
// The city's street panoramas (CC BY 4.0), turned towards the building from the nearest point on the street.
function streetView(b) {
  const [lat, lon] = toLatLon(b.x, b.z);
  return `https://api.data.amsterdam.nl/panorama/thumbnail/?lat=${lat.toFixed(6)}&lon=${lon.toFixed(6)}&width=640&radius=80`;
}
const svCredit = () => `${t('Street view')}: <a href="https://data.amsterdam.nl" target="_blank" rel="noopener">Gemeente Amsterdam</a>, CC BY 4.0`;

// The article in the reader's language when there is one.
const wikiOf = w => (LANG === 'nl' && w?.wiki_nl?.extract ? w.wiki_nl : w?.wiki) || w?.wiki_nl;

function groupColor(g) {
  return GROUP_COLORS[g.layer.groups.findIndex(x => x.bit === g.bit)] || GROUP_COLORS[0];
}

function residentsHtml(b, pinned) {
  const n = residentsLayer?.notes?.[b.bag];
  if (!n) return '';
  const people = pinned ? n.people : n.people.slice(0, 3);
  return `<section><h4>${t('Lived or worked here')}</h4><ul class="residents">${people.map(p => `<li>
    <b>${pinned ? link(p.url, p.person) : esc(p.person)}</b>${p.born ? ` <span>${esc(p.born)}${p.died ? '–' + esc(p.died) : ''}</span>` : ''}
    ${p.desc ? `<div class="desc">${esc(p.desc)}</div>` : ''}
    ${pinned ? (p.quote.startsWith('Wikidata') ? `<p class="why">${esc(t(p.quote))}</p>` : `<blockquote lang="nl">${esc(p.quote)}</blockquote>`) : ''}
    ${p.died && b.year > +p.died + 5 ? `<p class="why">${LANG === 'nl' ? `Dit gebouw dateert uit ${b.year}, na de dood van ${esc(p.person.split(' ').slice(-1)[0])}; het staat op de plek van het huis.` : `This building dates from ${b.year}, after ${esc(p.person.split(' ').slice(-1)[0])} died; it stands where their house stood.`}</p>` : ''}</li>`).join('')}</ul>
    ${!pinned && n.people.length > 3 ? `<p class="why">${LANG === 'nl' ? 'en' : 'and'} ${n.people.length - 3} ${LANG === 'nl' ? 'meer' : 'more'}</p>` : ''}</section>`;
}

// ---------- Photos through the years ----------
// Archive pictures from the Stadsarchief beeldbank (s12_archive), in 64 shards keyed by a CRC-32 of the BAG id.
const CRC = Array.from({ length: 256 }, (_, n) => { for (let k = 0; k < 8; k++) n = n & 1 ? 0xEDB88320 ^ (n >>> 1) : n >>> 1; return n >>> 0; });
const crc32 = s => { let c = ~0; for (const ch of s) c = CRC[(c ^ ch.charCodeAt(0)) & 255] ^ (c >>> 8); return (~c) >>> 0; };
// ---------- The card's head ----------
// The head is painted in the building's period colour, so the card says its age before it is read: name, address,
// year. Text goes dark on the light colours of the palette and white on the dark ones.
const addrShards = {};
function addressOf(gid, then) {
  const k = Math.floor(gid / 4096);
  if (addrShards[k] === undefined) {
    addrShards[k] = null;
    fetch(`data/addr/${k}.json`).then(r => r.json()).then(d => { addrShards[k] = d; then(); }).catch(() => {});
  }
  return addrShards[k]?.[gid % 4096] || null;
}
function inkOn(hex) {
  const c = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255).map(v => v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2] > 0.3 ? '#000' : '#fff';
}
// Google Maps by address, so Google opens its own card for the place; by coordinates when there is no address.
function googleMapsUrl(b, a) {
  const [lat, lon] = toLatLon(b.x, b.z);
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(a ? `${a[0]}, ${config.label}` : `${lat.toFixed(6)},${lon.toFixed(6)}`)}`;
}
function cardHeadHtml(b, w, period) {
  const a = addressOf(b.gid, () => refreshCard(b.gid));
  const address = a && `${esc(a[0])}${a[1] ? ` <span class="more">${LANG === 'nl' ? `(en ${a[1]} meer)` : `(and ${a[1]} more)`}</span>` : ''}`;
  const name = w?.label && tr(w, 'label');
  // a Wikidata label that is only the address (many listed houses) is said once
  const sameAsAddress = name && a && name.replace(/,.*$/, '') === a[0];
  return `<header class="card-head" style="background:${period.color};color:${inkOn(period.color)}">
      ${name && !sameAsAddress ? `<h3>${esc(name)}</h3>` : ''}
      <p class="addr">${address ? `<span>${address}</span>` : ''}<a class="gmaps" href="${esc(googleMapsUrl(b, a))}" target="_blank" rel="noopener" title="${t('Open in Google Maps')}" aria-label="${t('Open in Google Maps')}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 15s5-4.6 5-8.6A5 5 0 0 0 3 6.4C3 10.4 8 15 8 15z"/><circle cx="8" cy="6.4" r="1.8"/></svg></a></p>
      <div class="when"><span class="y">${[1, 2, 4].includes(b.flag) ? 'c. ' : ''}${b.year}</span>
        <span class="period">${esc(t(period.label))}</span></div>
    </header>`;
}

const archiveShards = {};
function archiveOf(bag, then) {
  const n = String(crc32(bag) % 64).padStart(2, '0');
  if (archiveShards[n] === undefined) {
    archiveShards[n] = null;
    fetch(`data/archive/${n}.json`).then(r => r.json()).then(d => { archiveShards[n] = d; then(); }).catch(() => {});
  }
  return archiveShards[n]?.[bag] || [];
}
// The archive's thumbnails load straight from its image host. A proxy through the site's Worker does not work:
// the host answers data-centre requests with a bot challenge.
const SAA_IMG = 'https://images.memorix.nl/ams/thumb/';
const KIND_EN = { bouwtekening: 'building drawing', tekening: 'drawing', prent: 'print', prentbriefkaart: 'picture postcard' };
let slides = [], slide = 0;
// Oldest archive picture first, today's photo (Wikimedia, or the street panorama) last; the card opens on today.
function photosHtml(b, im, credit, pinned) {
  const archive = archiveOf(b.bag, () => refreshCard(b.gid));
  slides = [...archive.map(a => ({
    src: `${SAA_IMG}640x480/${a.t}.jpg`, label: String(a.y), page: `https://archief.amsterdam/beeldbank/detail/${a.r}`,
    credit: `${a.k ? esc(LANG === 'nl' ? a.k : KIND_EN[a.k] || a.k) + ', ' : ''}${a.y}${a.m ? ', ' + esc(a.m) : ''}, ${pinned
      ? link(`https://archief.amsterdam/beeldbank/detail/${a.r}`, 'Stadsarchief Amsterdam') : 'Stadsarchief Amsterdam'}`,
  })), im ? { src: im.thumb, label: t('Today'), credit: `${t('Photo')}: ${credit}` }
    : { sv: streetView(b), label: t('Today'), credit: pinned ? svCredit() : `${t('Street view')}: Gemeente Amsterdam, CC BY 4.0` }];
  slide = slides.length - 1;
  const s = slides[slide];
  const span = archive.length && `${archive[0].y}${archive.length > 1 ? '–' + archive.at(-1).y : ''}`;
  const more = !archive.length || pinned ? '' : `<p class="more-photos">${LANG === 'nl'
    ? `+ ${archive.length} archieffoto${archive.length > 1 ? "'s" : ''}, ${span}. Klik om te bladeren`
    : `+ ${archive.length} archive photo${archive.length > 1 ? 's' : ''}, ${span}. Click to browse`}</p>`;
  return `<figure class="photo${s.sv ? ' sv' : ''}"><div class="frame">${s.sv ? `<img data-sv="${esc(s.sv)}" alt="">` : `<img src="${esc(s.src)}" alt="">`}
    ${pinned && slides.length > 1 ? `<button class="prev" aria-label="${t('Earlier')}">‹</button><button class="next" aria-label="${t('Later')}">›</button>` : ''}
    ${slides.length > 1 ? `<span class="year">${s.label}</span>` : ''}</div>
    <figcaption>${s.credit}</figcaption>${pinned && slides.length > 1 ? '<nav class="years"></nav>' : ''}${more}</figure>`;
}
function showSlide(i) {
  const fig = card.querySelector('.photo');
  if (!fig || !slides.length) return;
  slide = Math.max(0, Math.min(i, slides.length - 1));
  const s = slides[slide], img = fig.querySelector('img');
  img.removeAttribute('data-sv');
  img.src = s.sv || s.src;
  fig.classList.toggle('sv', !!s.sv);
  const year = fig.querySelector('.year');
  if (year) year.textContent = s.label;
  fig.querySelector('figcaption').innerHTML = s.credit;
  const nav = fig.querySelector('.years');
  if (nav) {
    nav.innerHTML = slides.map((x, k) => `<button data-slide="${k}"${k === slide ? ' aria-current="true"' : ''}>${x.label}</button>`).join('');
    nav.querySelectorAll('button').forEach(b => b.addEventListener('click', () => showSlide(+b.dataset.slide)));
  }
  fig.querySelector('.prev')?.toggleAttribute('disabled', slide === 0);
  fig.querySelector('.next')?.toggleAttribute('disabled', slide === slides.length - 1);
}
function wireSlides() {
  const fig = card.querySelector('.photo');
  if (!fig) return;
  // A picture that fails to load says so and links to the archive; with nothing else to show the frame goes.
  fig.querySelector('img').addEventListener('error', () => {
    if (slides.length < 2) { fig.remove(); return; }
    fig.classList.add('failed');
    fig.querySelector('.frame .gone')?.remove();
    fig.querySelector('.frame').insertAdjacentHTML('afterbegin', `<p class="gone">${t('This photo did not load.')}${
      slides[slide].page ? ` ${link(slides[slide].page, t('Open it in the archive'))}` : ''}</p>`);
  });
  fig.querySelector('img').addEventListener('load', () => { fig.classList.remove('failed'); fig.querySelector('.frame .gone')?.remove(); });
  fig.querySelector('.prev')?.addEventListener('click', () => showSlide(slide - 1));
  fig.querySelector('.next')?.addEventListener('click', () => showSlide(slide + 1));
  let x0 = null; // swipe on phones
  fig.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; }, { passive: true });
  fig.addEventListener('touchend', e => { const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 40) showSlide(slide + (dx < 0 ? 1 : -1)); });
  if (fig.querySelector('.years')) showSlide(slide);
}
// A shard that arrives after the card is drawn redraws the card, if it still shows that building.
function refreshCard(gid) {
  if (card.hidden) return;
  if (pinnedGid === gid) pinCard(gid, ...lastPin);
  else if (hoverGid === gid) { hoverGid = -1; showCard(gid, ...(pointer || lastPin)); }
}

// The card reads top to bottom: photo, name and year; what the building is; the layers it belongs to and why;
// the facts; how its date was found; where to read more.
function cardHtml(gid, pinned) {
  const b = building(gid);
  const w = b.wk >= 0 ? wiki[b.wk] : null;
  const im = w?.image?.thumb ? w.image : null;
  const period = periodOf(b.year);
  const facts = [
    [t('Height'), `${b.height.toFixed(1)} m`],
    [t('Storeys'), b.fsrc === 0 ? t('from the 3D BAG model') : t('height ÷ 3.2 m')],
    w?.architects?.length && [t(w.architects.length > 1 ? 'Architects' : 'Architect'), w.architects.map(esc).join(', ')],
    w?.styles?.length && [t('Style'), w.styles.map(esc).join(', ')],
    b.mon && [t('National monument'), `${LANG === 'nl' ? 'nr.' : 'no.'} ${b.mon}`],
    b.energy && [t('Energy label'), `<span class="elabel" style="background:${ENERGY_COLORS[b.energy]}">${config.energy.labels[b.energy - 1]}</span>`],
  ].filter(Boolean);
  const credit = im && (pinned
    ? `${link(im.page || im.thumb, im.artist || 'Wikimedia Commons')}${im.license ? `, ${im.licenseUrl ? link(im.licenseUrl, im.license) : esc(im.license)}` : ''}`
    : `${esc(im.artist || 'Wikimedia Commons')}${im.license ? `, ${esc(im.license)}` : ''}`);
  const sources = [
    wikiOf(w)?.url && link(wikiOf(w).url, t(wikiOf(w).lang === 'nl' ? 'Dutch Wikipedia' : 'Wikipedia')),
    b.mon && link(`https://monumentenregister.cultureelerfgoed.nl/monumenten/${b.mon}`, t('Monument register')),
    link(`https://bagviewer.kadaster.nl/lvbag/bag-viewer/?objectId=${b.bag}`, t('BAG register')),
    link(googleMapsUrl(b, addressOf(b.gid, () => {})), 'Google Maps'),
  ].filter(Boolean);
  const inLayers = b.groups.map(g => {
    const note = g.layer.notes?.[b.bag];
    return `<li><i style="background:${groupColor(g)}"></i><div><b>${esc(tr(g.layer, 'title'))}</b> <span>${esc(tr(g, 'label'))}</span>
      ${pinned && note ? `<p>${esc(tr(note, 'story'))}${note.source ? ` ${link(note.source, t('Source'))}` : ''}</p>` : ''}</div></li>`;
  }).join('');
  const dating = b.orig !== b.year ? `${t(DATE_NOTE[b.flag] || '')} ${t('BAG gives')} ${b.orig}.` : (DATE_NOTE[b.flag] && t(DATE_NOTE[b.flag]));
  return `
    ${pinned ? '<button class="card-close" aria-label="Close">×</button>' : ''}
    ${photosHtml(b, im, credit, pinned)}
    ${cardHeadHtml(b, w, period)}
    ${pinned && wikiOf(w)?.extract ? `<section><p class="extract">${esc(wikiOf(w).extract)}</p></section>` : ''}
    ${didYouKnow[b.bag] ? `<section class="fact"><h4>${t('Did you know')}</h4><p>${esc(LANG === 'nl' ? didYouKnow[b.bag].nl : didYouKnow[b.bag].en)}${pinned ? ` ${link(didYouKnow[b.bag].source, t('Source'))}` : ''}</p></section>` : ''}
    ${residentsHtml(b, pinned)}
    ${inLayers ? `<section><h4>${t('In layers')}</h4><ul class="chips">${inLayers}</ul></section>` : ''}
    <section><dl>${facts.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('')}</dl></section>
    ${dating ? `<section><h4>${t('Dating')}</h4><p class="why">${dating}</p></section>` : ''}
    ${pinned ? `<section class="sources"><h4>${t('Read more')}</h4><p>${sources.join(', ')}</p></section>`
      : `<p class="hint">${w?.wiki || b.groups.some(g => g.layer.notes?.[b.bag]) ? t('Click for the story and sources') : t('Click to keep this card open')}</p>`}`;
}

const card = document.getElementById('card');
let pinnedGid = -1;
let svTimer = null;
function loadStreetViews(delay) {
  clearTimeout(svTimer);
  svTimer = setTimeout(() => card.querySelectorAll('img[data-sv]').forEach(img => {
    img.addEventListener('load', () => placeCard(...(pointer || lastPin)), { once: true });
    img.src = img.dataset.sv;
  }), delay);
}
let lastPin = [0, 0];
function placeCard(x, y) {
  const r = card.getBoundingClientRect();
  card.style.left = Math.max(12, Math.min(x + 18, innerWidth - r.width - 12)) + 'px';
  card.style.top = Math.max(12, Math.min(y + 18, innerHeight - r.height - 12)) + 'px';
}
let hoverGid = -1;
function showCard(gid, x, y) {
  if (pinnedGid >= 0 || phone.matches) return;
  if (cardsLocked()) { card.hidden = true; return; }
  if (gid < 0) { card.hidden = true; hoverGid = -1; return; }
  if (gid !== hoverGid || card.hidden) {
    // Re-render only when the building changes, so the photo is not reloaded every frame.
    hoverGid = gid;
    card.innerHTML = cardHtml(gid, false);
    wireSlides();
    card.classList.remove('pinned');
    card.hidden = false;
    loadStreetViews(350);
    card.querySelector('img')?.addEventListener('load', () => placeCard(...(pointer || [x, y])));
  }
  placeCard(x, y);
}
function pinCard(gid, x, y) {
  pinnedGid = gid;
  hoverGid = -1;
  uniforms.uSelected.value = gid;
  if (gid < 0) { card.hidden = true; card.classList.remove('pinned'); return; }
  card.innerHTML = cardHtml(gid, true);
  wireSlides();
  card.classList.add('pinned');
  lastPin = [x, y];
  collapsePanelOnPhone();
  loadStreetViews(0);
  card.hidden = false;
  card.querySelector('.card-close').onclick = () => pinCard(-1);
  card.querySelector('img')?.addEventListener('load', () => placeCard(x, y));
  placeCard(x, y);
}
addEventListener('keydown', e => { if (e.key === 'Escape') pinCard(-1); });

// A click (not a drag) pins the building under the pointer, or clears the pin on empty ground.
let pointer = null, dragging = false, downAt = null;
canvas.addEventListener('pointermove', e => { pointer = [e.clientX, e.clientY]; });
canvas.addEventListener('pointerdown', e => {
  dragging = true; downAt = [e.clientX, e.clientY];
  if (pinnedGid < 0) card.hidden = true;
});
canvas.addEventListener('pointerup', e => {
  dragging = false;
  if (!downAt || Math.hypot(e.clientX - downAt[0], e.clientY - downAt[1]) > 5) return;
  if (pickingStart) {
    const at = groundAt(e.clientX, e.clientY);
    if (at) { pickingStart = false; walkPrefs.at = at; walkPrefs.atLabel = t('Point on the map'); walkEl.hidden = true; openWalks(); }
    return;
  }
  const gid = pick(e.clientX, e.clientY);
  if (quest && !solved && qStep().kind === 'where') { whereClick(e.clientX, e.clientY); return; }
  if (quest && !solved && qStep().kind === 'find') { questClick(gid); return; }
  if (cardsLocked()) return;
  pinCard(gid === pinnedGid ? -1 : gid, e.clientX, e.clientY);
});
canvas.addEventListener('pointerleave', () => { pointer = null; if (pinnedGid < 0) card.hidden = true; uniforms.uHover.value = -1; });

// ---------- Flying to a building ----------
let bagIndex = null;
function gidOf(bag) {
  if (!bagIndex) {
    bagIndex = new Map();
    for (let g = 0; g < config.stats.buildings; g++) {
      bagIndex.set(String(attrs.getFloat64(g * config.attrStride, true)).padStart(16, '0'), g);
    }
  }
  return bagIndex.get(bag) ?? -1;
}
let flight = null;
function flyTo(x, z, done, distance = 520) {
  const dir = camera.position.clone().sub(controls.target).normalize();
  if (dir.y < 0.45) { dir.y = 0.45; dir.normalize(); }
  const target = new THREE.Vector3(x, 0, z);
  flight = { t0: performance.now(), dur: 1400, fromT: controls.target.clone(), toT: target,
    fromP: camera.position.clone(), toP: target.clone().add(dir.multiplyScalar(distance)), done };
}
function stepFlight(now) {
  if (!flight) return;
  const k = Math.min(1, (now - flight.t0) / flight.dur), e = k < 0.5 ? 2 * k * k : 1 - (-2 * k + 2) ** 2 / 2;
  controls.target.lerpVectors(flight.fromT, flight.toT, e);
  camera.position.lerpVectors(flight.fromP, flight.toP, e);
  if (k >= 1) { const d = flight.done; flight = null; d?.(); }
}

// ---------- Quests ----------
// Short walks through the city as riddles (pipeline/quests.py, checked by s13_quests): find a building on the map,
// point to where a building stands, guess its year with the colours hidden, or pick one of three answers.
// Every answer is worth up to 100 points; hints and wrong answers cost points. A finished quest can be sent to a
// friend as a challenge: the link opens the same quest with the score to beat. Progress stays in this browser.
let quests = [];
fetch('data/quests.json').then(r => r.ok ? r.json() : []).then(q => { quests = q; challengeFromUrl(); }).catch(() => {});
const questEl = document.getElementById('quest');
const questsDlg = document.getElementById('quests');
const L10 = o => o?.[LANG] || o?.en || '';
const LEVEL = ['', 'Easy', 'Medium', 'Hard'];
const qStore = () => { try { return JSON.parse(localStorage.getItem('ams-quests2') || '{}'); } catch { return {}; } };
function qSave(id, patch) {
  try { const p = qStore(); p[id] = { ...(p[id] || {}), ...patch }; localStorage.setItem('ams-quests2', JSON.stringify(p)); } catch {}
}
const crosses = (n, of = 3) => `<span class="q-x" aria-hidden="true">${Array.from({ length: of }, (_, i) =>
  `<i class="${i < n ? 'on' : ''}">×</i>`).join('')}</span>`;
const levelMark = lv => `<span class="q-level">${crosses(lv)}${t(LEVEL[lv])}</span>`;
const fmtN = n => n.toLocaleString(fmtLocale());
const maxOf = q => q.steps.length * 100;
// A small seeded generator: the same circle offset and answer order every time a step is played.
function rng(seed) { let h = 2166136261; for (const c of seed) h = Math.imul(h ^ c.charCodeAt(0), 16777619); return () => ((h = Math.imul(h ^ (h >>> 15), 2246822507) ^ Math.imul(h ^ (h >>> 13), 3266489909)) >>> 0) / 4294967296; }

function renderQuestList() {
  const p = qStore();
  const total = quests.reduce((n, q) => n + (p[q.id]?.best || 0), 0), max = quests.reduce((n, q) => n + maxOf(q), 0);
  const tile = (q, st) => {
    const n = q.steps.length, done = Math.min(st.step || 0, n), complete = st.best !== undefined && !(st.step > 0 && st.step < n);
    return `<li class="q-tile l${q.level}${complete ? ' complete' : ''}">
      ${levelMark(q.level)}
      <h3>${esc(L10(q.title))}</h3><p>${esc(L10(q.intro))}</p>
      <footer><span class="q-progress">${complete ? `${t('Best')}: ${fmtN(st.best)}` : done ? `${done} / ${n}` : `${n} ${t('steps')}`}</span>
        <button class="q-start" data-q="${q.id}">${complete ? t('Play again') : done ? t('Continue') : t('Start')}</button></footer></li>`;
  };
  document.getElementById('quests-body').innerHTML = `
    <h2 id="quests-title">${t('Quests')}</h2>
    <p class="q-lede">${t('Find buildings from riddles and old photos, point to them on the map, guess their age with the colours switched off. Up to 100 points an answer; hints cost points.')}</p>
    <p class="q-score">${t('Your points')}: <b>${fmtN(total)}</b> / ${fmtN(max)}</p>
    <ul class="q-grid">${quests.map(q => tile(q, p[q.id] || {})).join('')}</ul>`;
  questsDlg.querySelectorAll('.q-start').forEach(b => b.onclick = () => {
    const q = quests.find(q => q.id === b.dataset.q), st = qStore()[q.id] || {};
    questsDlg.close();
    const resume = st.step > 0 && st.step < q.steps.length;
    rival = null;
    startQuest(q, resume ? st.step : 0, resume ? st.score || 0 : 0, resume ? st.marks || [] : []);
  });
}
function openQuests() { renderQuestList(); questsDlg.showModal(); }
document.querySelector('.quests-open').onclick = openQuests;
questsDlg.querySelector('.about-close').onclick = () => questsDlg.close();
questsDlg.addEventListener('click', e => { if (e.target === questsDlg) questsDlg.close(); });

// A friend's challenge: ?quest=<id>&beat=<points> opens that quest once the city has loaded.
let rival = null, cityLoaded = false, pendingQuest = null;
function challengeFromUrl() {
  const u = new URLSearchParams(location.search), q = quests.find(q => q.id === u.get('quest'));
  if (!q) return;
  rival = Number.isFinite(+u.get('beat')) && u.get('beat') !== null ? Math.max(0, Math.min(maxOf(q), +u.get('beat'))) : null;
  pendingQuest = q;
  if (cityLoaded) cityReady();
}
function cityReady() {
  cityLoaded = true;
  if (pendingQuest) { const q = pendingQuest; pendingQuest = null; startQuest(q, 0, 0, []); }
}

// On the ground: the search circle (red ring around, not centred on, the answer), and for "where" steps the
// player's guess (a black dot), the answer (a red dot) and the line between them.
const groundMat = (color, opacity = 1) => new THREE.MeshBasicMaterial({ color, depthTest: false, transparent: true, opacity });
const onGround = m => { m.rotation.x = -Math.PI / 2; m.renderOrder = 20; return m; };
const ring = new THREE.Group();
ring.add(onGround(new THREE.Mesh(new THREE.RingGeometry(0.97, 1, 128), groundMat(0xec0000, 0.95))));
ring.add(onGround(new THREE.Mesh(new THREE.CircleGeometry(0.97, 128), groundMat(0xec0000, 0.06))));
ring.visible = false;
scene.add(ring);
const pins = new THREE.Group();
const guessDot = onGround(new THREE.Mesh(new THREE.CircleGeometry(1, 32), groundMat(0x000000)));
const answerDot = onGround(new THREE.Mesh(new THREE.RingGeometry(0.55, 1, 32), groundMat(0xec0000)));
const pinLine = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), groundMat(0x000000, 0.8));
onGround(pinLine);
pins.add(pinLine, guessDot, answerDot);
pins.visible = false;
scene.add(pins);
function showPins(gx, gz, ax, az, d) {
  const s = Math.max(10, d / 30);
  guessDot.position.set(gx, 3, gz); guessDot.scale.setScalar(s * 0.8);
  answerDot.position.set(ax, 3, az); answerDot.scale.setScalar(s * 1.2);
  pinLine.position.set((gx + ax) / 2, 2.5, (gz + az) / 2);
  pinLine.scale.set(Math.max(1, d), s * 0.25, 1);
  pinLine.rotation.z = -Math.atan2(az - gz, ax - gx);
  pins.visible = true;
}

// "Show me": a red pin standing on the building, seen from anywhere above the city.
const marker = new THREE.Group();
const pinMat = new THREE.MeshBasicMaterial({ color: 0xec0000, depthTest: false, transparent: true });
const stem = new THREE.Mesh(new THREE.CylinderGeometry(1, 1, 1, 8), pinMat), head = new THREE.Mesh(new THREE.SphereGeometry(1, 20, 14), pinMat);
stem.renderOrder = head.renderOrder = 21;
marker.add(stem, head);
marker.visible = false;
scene.add(marker);
function showMarker(b) {
  const top = b.height, len = 70;
  stem.scale.set(1.6, len, 1.6); stem.position.set(0, top + len / 2, 0);
  head.scale.setScalar(9); head.position.set(0, top + len, 0);
  marker.position.set(b.x, 0, b.z); marker.visible = true;
}

let quest = null, step = 0, score = 0, marks = [], hintsShown = 0, tries = 0, solved = false, revealed = false, lastDist = null;
let folded = false, guess = 1800, missed = null;
const qStep = () => quest.steps[step];
const stepGids = s => s.bags.map(gidOf).filter(g => g >= 0);
function centre(gids) {
  const bs = gids.map(building);
  return [bs.reduce((a, b) => a + b.x, 0) / bs.length, bs.reduce((a, b) => a + b.z, 0) / bs.length];
}
// The map's state while a step asks about one building: its card locked, its colours hidden for a year riddle.
let quizGid = -1;
function setQuiz(gid, blind) {
  quizGid = gid;
  uniforms.uSelected.value = gid;
  uniforms.uBlind.value = gid < 0 ? 0 : blind ? 1 : 2;
  if (gid >= 0) { pinCard(-1); uniforms.uSelected.value = gid; }
}
// Cards stay closed while they would give the answer away: a building asked about, or any name in a "where" step.
const cardsLocked = () => quest && !solved && (quizGid >= 0 || qStep().kind === 'where');

function startQuest(q, n, sc = 0, mk = []) {
  quest = q; step = n; score = sc; marks = mk;
  document.body.classList.add('questing');
  pinCard(-1);
  enterStep(true);
}
// The camera over the box around every building the quest visits.
function overview() {
  const bs = quest.steps.flatMap(stepGids).map(building);
  const x0 = Math.min(...bs.map(b => b.x)), x1 = Math.max(...bs.map(b => b.x)), z0 = Math.min(...bs.map(b => b.z)), z1 = Math.max(...bs.map(b => b.z));
  questFly((x0 + x1) / 2, (z0 + z1) / 2, Math.min(7000, Math.max(900, Math.hypot(x1 - x0, z1 - z0) * 1.5)));
}
function enterStep(first) {
  hintsShown = 0; tries = 0; solved = false; revealed = false; lastDist = null; folded = false; guess = 1800; missed = null;
  ring.visible = false; pins.visible = false; marker.visible = false;
  const s = qStep(), gids = stepGids(s);
  if (s.kind === 'find' || s.kind === 'where') {
    setQuiz(-1, false);
    // A find quest opens on all of its buildings; every "where" step goes back to the whole city.
    if (first || s.kind === 'where') overview();
  } else if (gids.length) {
    const b = building(gids[0]);
    setQuiz(gids[0], s.kind === 'year');
    questFly(b.x, b.z, s.kind === 'year' ? 300 : 380);
  }
  renderQuest();
}
// On a phone the quest sits over the top half of the map: aim past the building so it lands in the lower half.
function questFly(x, z, dist, done = null) {
  if (phone.matches) {
    const f = controls.target.clone().sub(camera.position).setY(0).normalize();
    x += f.x * dist * 0.2; z += f.z * dist * 0.2;
  }
  flyTo(x, z, done, dist);
}
function closeQuest() {
  document.body.classList.remove('questing');
  quest = null; questEl.hidden = true; ring.visible = false; pins.visible = false; marker.visible = false; setQuiz(-1, false);
}
function setModeNamed(name) {
  if (name === 'floors' || name === 'energy') { setBuildingView(MODE[name]); return; }
  document.querySelector(`.modes button[data-mode="${MODE[name]}"]`)?.click();
}
// Storeys and energy labels are views of the buildings themselves; they live in the layers list.
function setBuildingView(m) {
  document.querySelectorAll('.modes button[data-mode]').forEach(x => x.setAttribute('aria-pressed', x.dataset.mode === String(MODE.layers)));
  activeLayer = null;
  uniforms.uGroupBit.value = Array(MAX_GROUPS).fill(-1);
  uniforms.uMode.value = m;
  if (!phone.matches) setCollapsed(false);
  renderPanel(); drawHist();
}
function showRing() {
  const s = qStep(), [x, z] = centre(stepGids(s));
  const r = { 1: 220, 2: 300, 3: 380 }[quest.level] || 300;
  const k = rng(quest.id + step), a = k() * Math.PI * 2, d = r * 0.55 * Math.sqrt(k());
  const cx = x + Math.cos(a) * d, cz = z + Math.sin(a) * d;
  ring.position.set(cx, 2, cz); ring.scale.setScalar(r); ring.visible = true;
  questFly(cx, cz, r * 5);
}

function photoOf(s) {
  if (s.clue?.id) return { src: `${SAA_IMG}640x480/${s.clue.thumb}.jpg`, credit: `${link(`https://archief.amsterdam/beeldbank/detail/${s.clue.id}`, 'Stadsarchief Amsterdam')}, ${s.clue.year}`, year: s.clue.year };
  if (s.clue?.thumb) return { src: s.clue.thumb, credit: link(s.clue.page || s.clue.thumb, [s.clue.artist, s.clue.license].filter(Boolean).join(', ') || 'Wikimedia Commons') };
  return null;
}
const progress = () => `<div class="q-steps">${quest.steps.map((_, i) => `<i class="${i < step || (i === step && solved) ? 'done' : i === step ? 'now' : ''}"></i>`).join('')}
  <span>${fmtN(score)} ${t('pts')}</span></div>`;
// Points: a find loses 25 a hint (never below 25); a choice gives 100, 40, then nothing; a year guess and a
// "where" tap lose points smoothly with the distance.
const HINT_COST = 25;
const worth = () => {
  const s = qStep();
  if (s.kind === 'find') return revealed ? 0 : Math.max(25, 100 - HINT_COST * hintsShown);
  if (s.kind === 'choice') return [100, 40, 0][Math.min(tries, 2)];
  return 100;
};
const yearPoints = d => Math.round(100 * Math.exp(-d / 30));
const wherePoints = m => Math.round(100 * Math.exp(-m / 450));
const fmtDist = m => m < 1000 ? `${Math.round(m / 10) * 10} m` : `${(m / 1000).toLocaleString(fmtLocale(), { maximumFractionDigits: 1 })} km`;

function renderQuest() {
  if (!quest) return;
  const s = qStep(), ph = photoOf(s);
  questEl.className = `quest k-${s.kind}${solved ? ' solved' : ''}${folded ? ' folded' : ''}`;
  // Once answered, a "where" step drops its photo so the map shows the guess and the answer.
  const photo = ph && !(solved && (s.clue?.id || s.kind === 'where')) ? `<figure class="q-photo"><img src="${esc(ph.src)}" alt="${t('A photo of the building')}">${ph.year ? `<span class="year">${ph.year}</span>` : ''}</figure><p class="q-credit">${ph.credit}</p>` : '';
  let body = '';
  if (s.kind === 'find') {
    const hints = Array.from({ length: hintsShown }, (_, i) => i === 0 ? t('Look inside the red circle.') : L10(s.hints[i - 1]));
    const more = hintsShown < s.hints.length + 1;
    body = `${photo}
      <p class="q-riddle">${esc(L10(s.riddle))}</p>
      ${hints.length ? `<ul class="q-hints">${hints.map(h => `<li>${esc(h)}</li>`).join('')}</ul>` : ''}
      ${solved ? '' : `<p class="q-feedback">${t('Find it on the map and click it.')}</p>
      <div class="q-actions">
        ${s.mode ? `<button class="q-mode">${t(s.mode === 'floors' ? 'Colour by floors' : 'Colour by period')}</button>` : ''}
        <span class="q-quiet">${more ? `<button class="q-hint">${t('Hint')} −${HINT_COST}</button>` : ''}<button class="q-reveal">${t('Show me')}</button></span></div>`}`;
  } else if (s.kind === 'where') {
    body = `${photo}<p class="q-riddle">${esc(L10(s.riddle))}</p>
      ${solved ? '' : `<p class="q-feedback">${t('Tap the map where you think it stands.')}</p>`}`;
  } else if (s.kind === 'year') {
    body = `${photo}
      <p class="q-riddle">${esc(L10(s.ask))}</p>
      ${solved ? '' : `<div class="q-year"><output>${guess}</output>
        <input type="range" min="1250" max="2025" step="1" value="${guess}" aria-label="${t('Your guess')}">
        <div class="q-scale"><span>1250</span><span>1500</span><span>1750</span><span>2000</span></div></div>
        <div class="q-actions"><button class="primary q-guess">${t('Guess')}</button></div>`}`;
  } else {
    const order = s.options.map((o, i) => i).sort((a, b) => rng(quest.id + step + a)() - rng(quest.id + step + b)());
    body = `
      <p class="q-riddle">${esc(L10(s.ask))}</p>
      <div class="q-options">${order.map(i => `<button data-i="${i}" ${solved ? 'disabled' : ''} class="${solved && i === 0 ? 'right' : ''}">${esc(L10(s.options[i]))}</button>`).join('')}</div>
      ${solved ? '' : `<p class="q-feedback"></p>`}`;
  }
  questEl.innerHTML = `
    <button class="q-close" aria-label="${t('Close')}">×</button>
    <header><b>${esc(L10(quest.title))}</b>${levelMark(quest.level)}</header>
    ${progress()}${rival !== null && step === 0 && !solved ? `<p class="q-rival">${t('Score to beat')}: <b>${fmtN(rival)}</b></p>` : ''}${body}${solved ? revealHtml(s) : ''}`;
  questEl.hidden = false;
  wireQuest(s);
}
function revealHtml(s) {
  const got = marks[step] ?? 0, last = step === quest.steps.length - 1;
  const g = stepGids(s)[0], b = g >= 0 ? building(g) : null;
  const d = Math.abs(guess - (s.year || 0));
  const extra = s.kind === 'year' ? `<p class="q-yeardiff">${t('Your guess')}: <b>${guess}</b>. ${t('Built')}: <b>${s.year}</b>. ${d === 0 ? t('Exactly right.') : `${d} ${t(d === 1 ? 'year off' : 'years off')}.`}</p>`
    : s.kind === 'where' && missed !== null ? `<p class="q-yeardiff">${missed < 30 ? t('Spot on.') : `${fmtDist(missed)} ${t('off')}.`}</p>` : '';
  const then = s.clue?.id && b ? `<div class="q-then"><figure><img src="${esc(photoOf(s).src)}" alt=""><figcaption>${s.clue.year}</figcaption></figure>${
    b.wk >= 0 && wiki[b.wk]?.image?.thumb ? `<figure><img src="${esc(wiki[b.wk].image.thumb)}" alt=""><figcaption>${t('Today')}</figcaption></figure>` : ''}</div>` : '';
  return `<div class="q-found">
    <div class="q-stamp${got === 100 ? ' full' : ''}" aria-label="${got} ${t('pts')}">+${got}</div>
    ${then}${extra}
    <p>${esc(L10(s.reveal))}${s.sources?.length ? ' ' + s.sources.map((u, i) => link(u, s.sources.length > 1 ? `${t('Source')} ${i + 1}` : t('Source'))).join(', ') : ''}</p>
    ${revealed ? `<p class="q-earned">${t('Shown, not found: no points.')}</p>` : ''}</div>
    <div class="q-actions">${last ? `<button class="primary q-finish">${t('See the result')}</button>`
      : `<button class="primary q-next">${t('Next')}</button>`}<button class="q-card">${t('Open its card')}</button></div>`;
}
function wireQuest(s) {
  questEl.querySelector('header').onclick = () => { folded = !folded; questEl.classList.toggle('folded', folded); };
  questEl.querySelector('.q-close').onclick = closeQuest;
  const foldOnPhone = () => { if (phone.matches) { folded = true; questEl.classList.add('folded'); } };
  questEl.querySelector('.q-hint')?.addEventListener('click', () => { hintsShown++; if (hintsShown === 1) showRing(); renderQuest(); if (hintsShown === 1) foldOnPhone(); });
  questEl.querySelector('.q-mode')?.addEventListener('click', () => { setModeNamed(s.mode); foldOnPhone(); });
  questEl.querySelector('.q-reveal')?.addEventListener('click', () => {
    const g = stepGids(s)[0]; if (g === undefined) return;
    revealed = true; const b = building(g);
    questFly(b.x, b.z, 420, () => solve(g));
  });
  const range = questEl.querySelector('.q-year input');
  if (range) range.oninput = () => { guess = +range.value; questEl.querySelector('.q-year output').textContent = guess; };
  questEl.querySelector('.q-guess')?.addEventListener('click', () => solve(stepGids(s)[0], yearPoints(Math.abs(guess - s.year))));
  questEl.querySelectorAll('.q-options button').forEach(b => b.onclick = () => {
    if (+b.dataset.i === 0) { b.classList.add('right'); solve(stepGids(s)[0]); return; }
    tries++; b.classList.add('wrong'); b.disabled = true;
    const fb = questEl.querySelector('.q-feedback'); fb.textContent = `${t('Not that one.')} −${100 - worth()}`; fb.classList.remove('miss'); void fb.offsetWidth; fb.classList.add('miss');
  });
  questEl.querySelector('.q-next')?.addEventListener('click', () => { step++; qSave(quest.id, { step, score, marks }); enterStep(false); });
  questEl.querySelector('.q-finish')?.addEventListener('click', finished);
  questEl.querySelector('.q-card')?.addEventListener('click', () => { const g = stepGids(s)[0]; const b = building(g); quizGid = -1; uniforms.uBlind.value = 0; pins.visible = false; flyTo(b.x, b.z, () => pinCard(g, innerWidth * 0.3, 120), 380); });
}
function solve(gid, points) {
  solved = true; folded = false; ring.visible = false;
  const got = points ?? worth();
  marks[step] = got; score += got;
  quizGid = -1;
  // The answer stays marked: the building turns red in its own colours' city, and "Show me" also rings it.
  // Shown rather than found: the rest of the city goes grey, the building turns red, a pin and a ring mark it.
  uniforms.uBlind.value = gid < 0 ? 0 : revealed ? 1 : 2;
  if (gid >= 0) {
    pinCard(-1); uniforms.uSelected.value = gid;
    if (revealed) { const b = building(gid); ring.position.set(b.x, 2, b.z); ring.scale.setScalar(45); ring.visible = true; showMarker(b); }
  }
  const st = qStore()[quest.id] || {};
  const patch = { step: step + 1, score, marks };
  if (step === quest.steps.length - 1) patch.best = Math.max(st.best || 0, score);
  qSave(quest.id, patch);
  renderQuest();
}
// The result: the score, a bar per answer, and a challenge to send: a link that opens this quest with the score to beat.
function finished() {
  const max = maxOf(quest), share = Math.round(100 * score / max);
  const verdict = share >= 90 ? 'A true Amsterdammer.' : share >= 70 ? 'You know your way around.' : share >= 45 ? 'A good walk.' : 'Time for a walk through town.';
  const url = `https://stop-token.com/lab/amsterdam/?quest=${quest.id}&beat=${score}${LANG === 'nl' ? '&lang=nl' : ''}`;
  const text = LANG === 'nl'
    ? `Ik haalde ${fmtN(score)} van de ${fmtN(max)} punten in '${L10(quest.title)}' op LAYRS: Amsterdam. Doe je beter?`
    : `I scored ${fmtN(score)} of ${fmtN(max)} in '${L10(quest.title)}' on LAYRS: Amsterdam. Can you beat it?`;
  const vs = rival === null ? '' : `<p class="q-vs">${score > rival ? t('You beat your friend') : score === rival ? t('A draw with your friend') : t('Your friend wins this time')}: ${fmtN(score)} – ${fmtN(rival)}</p>`;
  questEl.className = 'quest done';
  questEl.innerHTML = `
    <button class="q-close" aria-label="${t('Close')}">×</button>
    <header><b>${esc(L10(quest.title))}</b>${levelMark(quest.level)}</header>
    <div class="q-result"><p class="q-total"><b>${fmtN(score)}</b> / ${fmtN(max)}</p><p class="q-verdict">${t(verdict)}</p>${vs}
      <div class="q-bars" aria-hidden="true">${marks.map(m => `<i style="height:${Math.max(4, m)}%" class="${m === 100 ? 'full' : ''}"></i>`).join('')}</div></div>
    <div class="q-actions"><button class="primary q-share">${t('Challenge a friend')}</button><button class="q-list">${t('More quests')}</button></div>
    <p class="q-shared" hidden></p>`;
  questEl.hidden = false;
  ring.visible = false; pins.visible = false; marker.visible = false; setQuiz(-1, false);
  rival = null;
  questEl.querySelector('.q-close').onclick = closeQuest;
  questEl.querySelector('.q-list').onclick = () => { closeQuest(); openQuests(); };
  questEl.querySelector('.q-share').onclick = async e => {
    const note = questEl.querySelector('.q-shared');
    if (navigator.share && phone.matches) { try { await navigator.share({ title: 'LAYRS: Amsterdam', text, url }); return; } catch {} }
    try { await navigator.clipboard.writeText(`${text}\n${url}`); e.target.textContent = t('Link copied'); }
    catch { note.hidden = false; note.textContent = `${text} ${url}`; }
  };
}
// Every click on the map while a find step is open.
function questClick(gid) {
  if (!quest || solved || gid < 0 || qStep().kind !== 'find') return;
  const s = qStep(), targets = stepGids(s);
  if (targets.includes(gid)) { solve(gid); return; }
  const fb = questEl.querySelector('.q-feedback');
  if (!fb) return;
  const b = building(gid);
  const d = Math.min(...targets.map(g => { const a = building(g); return Math.hypot(a.x - b.x, a.z - b.z); }));
  let msg = d < 40 ? t('Not this one, but right next to it.') : d < 200 ? t('Not this one. Very warm.')
    : d < 700 ? t('Not this one. A few streets away.') : t('Not this one. Far off.');
  if (lastDist !== null && d >= 40) msg += ' ' + t(d < lastDist - 20 ? 'Warmer than before.' : d > lastDist + 20 ? 'Colder than before.' : '');
  lastDist = d;
  fb.textContent = msg.trim();
  fb.className = `q-feedback ${d < 40 ? 'hot' : d < 200 ? 'warm' : 'cold'}`;
  void fb.offsetWidth; fb.classList.add('miss');
}
// A tap anywhere on the ground in a "where" step: the guess, scored by its distance from the building.
const groundPlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), caster = new THREE.Raycaster();
function whereClick(cx, cy) {
  const r = canvas.getBoundingClientRect(), hit = new THREE.Vector3();
  caster.setFromCamera(new THREE.Vector2(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1), camera);
  if (!caster.ray.intersectPlane(groundPlane, hit)) return;
  const s = qStep(), gids = stepGids(s);
  const near = gids.map(g => building(g)).sort((a, b) => Math.hypot(a.x - hit.x, a.z - hit.z) - Math.hypot(b.x - hit.x, b.z - hit.z))[0];
  missed = Math.hypot(near.x - hit.x, near.z - hit.z);
  showPins(hit.x, hit.z, near.x, near.z, missed);
  questFly((hit.x + near.x) / 2, (hit.z + near.z) / 2, Math.min(7000, Math.max(500, missed * (phone.matches ? 4 : 2))));
  solve(gids[0], wherePoints(missed));
}
addEventListener('keydown', e => { if (e.key === 'Escape' && questsDlg.open) questsDlg.close(); });

// Walk shows as on while a walk is open; on a phone the timeline steps aside.
function markWalk() {
  document.querySelector('.walks-open').setAttribute('aria-pressed', String(!!walkRoute));
  document.body.classList.toggle('walking', !!walkRoute);
}
// ---------- Walks ----------
// Where a walk can start besides the walker's location: the city config's list, else the map's centre.
const STARTS = config.starts || [{ en: 'Centre', nl: 'Centrum', x: 0, z: 0 }];
// A walk through the stories the walker cares about: pick interests, a start and a distance; the stops are the
// buildings with a story in those layers, chosen greedily by story per metre and ordered by 2-opt. Distances are
// straight lines times a detour factor; Google Maps gives the real walking route.
const DETOUR = 1.3, WALK_KMH = 4.5, STOP_MIN = 3, MAX_STOPS = 20;
const GOOGLE_LEG = 9;  // a Google Maps link takes at most 9 waypoints
const walkEl = document.getElementById('walk');
const walksDlg = document.getElementById('walks');
const walkGroup = new THREE.Group();
walkGroup.renderOrder = 5;
scene.add(walkGroup);
let walkPrefs = { layers: [], start: 0, km: 3, loop: true, at: null, stops: 0 }, walkRoute = null, pickingStart = false;

// WGS84 → local metres (inverse of toLatLon, Schreutelkamp and Strang van Hees, ~1 m).
function fromLatLon(lat, lon) {
  const p = 0.36 * (lat - 52.15517440), l = 0.36 * (lon - 5.38720621);
  const X = 155000 + 190094.945 * l - 11832.228 * p * l - 114.221 * p * p * l - 32.391 * l ** 3 - 0.705 * p
    - 2.34 * p ** 3 * l - 0.608 * p * l ** 3 - 0.008 * l * l + 0.148 * p * p * l ** 3;
  const Y = 463000 + 309056.544 * p + 3638.893 * l * l + 73.077 * p * p - 157.984 * p * l * l + 59.788 * p ** 3
    + 0.433 * l - 6.439 * p * p * l * l - 0.032 * p * l + 0.092 * l ** 4 - 0.054 * p * l ** 4;
  return [X - config.origin[0], -(Y - config.origin[1])];
}
// Every building with a story, merged across layers: one stop can carry several stories.
let poiCache = null;
function pois() {
  if (poiCache) return poiCache;
  const by = new Map();
  for (const L of layers) for (const [bag, n] of Object.entries(L.notes || {})) {
    if (!n.at) continue;
    const p = by.get(bag) || { bag, bags: [bag], x: n.at[0], z: n.at[1], notes: [] };
    p.notes.push({ L, n });
    by.set(bag, p);
  }
  // One stop per named place: a complex of several buildings (a laboratory, a hofje) carries the same story on
  // each of them; keep the building nearest their middle.
  const byName = new Map();
  for (const p of by.values()) {
    const key = p.notes.map(x => x.n.name).find(Boolean) || p.bag;
    (byName.get(key) || byName.set(key, []).get(key)).push(p);
  }
  poiCache = [];
  for (const ps of byName.values()) {
    const mx = ps.reduce((a, p) => a + p.x, 0) / ps.length, mz = ps.reduce((a, p) => a + p.z, 0) / ps.length;
    const keep = ps.reduce((a, p) => Math.hypot(p.x - mx, p.z - mz) < Math.hypot(a.x - mx, a.z - mz) ? p : a);
    const seen = new Set(keep.notes.map(x => x.L.id));
    keep.bags = [...new Set(ps.flatMap(p => p.bags))];
    for (const p of ps) for (const x of p.notes) if (!seen.has(x.L.id)) { keep.notes.push(x); seen.add(x.L.id); }
    poiCache.push(keep);
  }
  return poiCache;
}
const walkLayers = () => layers.filter(L => Object.values(L.notes || {}).filter(n => n.at).length >= 3);
const poiName = p => { if (p.name) return p.name; const n = p.notes.find(x => x.n.name && !x.n.people) || p.notes[0]; return tr(n.n, 'name') || n.n.name; };
function poiScore(p, chosen) {
  const hit = p.notes.filter(x => !chosen.length || chosen.includes(x.L.id)).length;
  if (!hit) return 0;
  const g = gidOf(p.bag), w = g >= 0 ? wiki[building(g).wk] : null;
  return 1 + 0.5 * (hit - 1) + (w?.image ? 0.4 : 0) + (didYouKnow[p.bag] ? 0.3 : 0);
}
const dist = (a, b) => Math.hypot(a.x - b.x, a.z - b.z);
function pathLen(pts) { let d = 0; for (let i = 1; i < pts.length; i++) d += dist(pts[i - 1], pts[i]); return d; }
function planWalkWithGap({ layers: chosen, km, loop, stops: asked, custom }, start, gap) {
  const budget = km * 1000 / DETOUR;
  const S = { x: start[0], z: start[1], start: true };
  let cand = (custom || pois().map(p => ({ ...p, score: poiScore(p, chosen) })))
    .filter(p => p.score > 0 && dist(p, S) <= (loop ? budget / 2 : budget));
  // Stops keep a spacing that grows with the walk, so a long walk goes somewhere instead of circling the Markt;
  // a closer one merges into the higher scored stop (a church with three entries is one stop).
  cand.sort((a, b) => b.score - a.score);
  cand = cand.filter((p, i) => !cand.slice(0, i).some(q => dist(p, q) < 25));
  const route = loop ? [S, S] : [S];
  const cap = asked || MAX_STOPS;
  const max = loop ? cap : cap + 1;
  while (route.length - (loop ? 2 : 1) < max) {
    let best = null;
    for (const c of cand) {
      if (route.includes(c) || route.some(r => !r.start && dist(r, c) < gap)) continue;
      for (let i = 0; i < route.length; i++) {
        const next = route[i + 1];
        const add = next ? dist(route[i], c) + dist(c, next) - dist(route[i], next) : dist(route[i], c);
        if (!next && loop) continue;
        if (pathLen(route) + add > budget) continue;
        const ratio = c.score / (add + gap);
        if (!best || ratio > best.ratio) best = { c, i, ratio };
      }
    }
    if (!best) break;
    route.splice(best.i + 1, 0, best.c);
  }
  // 2-opt over the stops between the fixed ends
  for (let improved = true; improved;) {
    improved = false;
    const last = loop ? route.length - 2 : route.length - 1;
    for (let i = 1; i < last; i++) for (let j = i + 1; j <= last; j++) {
      const a = route[i - 1], b = route[i], c = route[j], d = route[j + 1];
      const before = dist(a, b) + (d ? dist(c, d) : 0), after = dist(a, c) + (d ? dist(b, d) : 0);
      if (after < before - 1) { route.splice(i, j - i + 1, ...route.slice(i, j + 1).reverse()); improved = true; }
    }
  }
  return { start: S, stops: route.filter(p => !p.start), loop, length: pathLen(route) * DETOUR, route,
    score: route.reduce((n, p) => n + (p.score || 0), 0) };
}
// A wide spacing first; when the chosen stories are few and close together, tighter spacings keep them all.
function planAtLength(prefs, start) {
  const wide = Math.min(400, Math.max(30, prefs.km * 1000 / DETOUR / ((prefs.stops || MAX_STOPS) * 2.2)));
  const plans = [wide, wide / 2, wide / 4, 25].map(g => planWalkWithGap(prefs, start, g));
  const most = Math.max(...plans.map(p => p.stops.length));
  return plans.find(p => p.stops.length >= most);  // the widest spacing that loses no stop
}
// A walk with one or two stops is not a walk: when the chosen stories lie further away than the distance allows,
// the distance grows (up to three times) until there are a few of them, and the card says so.
const MIN_STOPS = 4;
function planWalk(prefs, start) {
  const available = prefs.custom ? prefs.custom.length : pois().filter(p => poiScore(p, prefs.layers) > 0).length;
  const want = Math.min(prefs.stops || MIN_STOPS, available);
  let w = planAtLength(prefs, start);
  for (let k = 1.25; w.stops.length < want && k <= 4.01; k += 0.25) {
    w = planAtLength({ ...prefs, km: prefs.km * k }, start);
    w.stretched = true;
  }
  return w;
}
// A stop goes to Google Maps by name and address, so Google opens its own card for the place (often with the
// Wikipedia summary); a stop without an address, and the start, go by coordinates.
const poiAddress = p => p.notes.map(x => x.n.address || x.n.people?.find(q => q.address)?.address).find(Boolean);
function poiQuery(p) {
  const addr = poiAddress(p), name = poiName(p);
  if (!addr) return null;
  return [name && name !== addr ? name : null, addr, config.label].filter(Boolean).join(', ');
}
// One Google Maps link: it takes at most 9 waypoints, so a longer walk sends the 9 best stops in walking order;
// the others lie on the way between them.
function googleStops(w) {
  const max = w.loop ? GOOGLE_LEG : GOOGLE_LEG + 1;
  if (w.stops.length <= max) return w.stops;
  const keep = new Set([...w.stops].sort((a, b) => b.score - a.score).slice(0, max));
  return w.stops.filter(p => keep.has(p));
}
function googleUrl(w) {
  const ll = p => (!p.start && poiQuery(p)) || toLatLon(p.x, p.z).map(v => v.toFixed(6)).join(',');
  const stops = googleStops(w).map(ll);
  const dest = w.loop ? ll(w.start) : stops.pop();
  const u = new URL('https://www.google.com/maps/dir/');
  u.searchParams.set('api', '1');
  u.searchParams.set('origin', ll(w.start));
  u.searchParams.set('destination', dest);
  if (stops.length) u.searchParams.set('waypoints', stops.join('|'));
  u.searchParams.set('travelmode', 'walking');
  return u.toString();
}
// The walk as KML, for Google My Maps or any map app: every stop with its story, its sources and a photo.
function walkKml(w) {
  const x = v => String(v ?? '').replace(/[<>&]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]));
  const pt = p => toLatLon(p.x, p.z).reverse().join(',') + ',0';
  const marks = w.stops.map((p, i) => {
    const g = gidOf(p.bag), wk = g >= 0 ? wiki[building(g).wk] : null, img = wk?.image?.thumb;
    const art = wk && (LANG === 'nl' ? wk.wiki_nl || wk.wiki : wk.wiki || wk.wiki_nl);
    const stories = p.notes.map(n => n.n.people
      ? `<p>${n.n.people.map(q => `${x(q.person)} (<a href="${x(q.url)}">Wikipedia</a>)`).join(', ')}</p>`
      : `<p>${x(tr(n.n, 'story'))}${n.n.source ? ` <a href="${x(n.n.source)}">${x(t('Source'))}</a>` : ''}</p>`).join('');
    const desc = `${img ? `<img src="${x(img)}" width="300"/>` : ''}${stories}${art?.url ? `<p><a href="${x(art.url)}">Wikipedia</a></p>` : ''}`;
    return `<Placemark><name>${i + 1}. ${x(poiName(p))}</name><description><![CDATA[${desc}]]></description>
<Point><coordinates>${pt(p)}</coordinates></Point></Placemark>`;
  }).join('\n');
  const line = [w.start, ...w.stops, ...(w.loop ? [w.start] : [])].map(pt).join(' ');
  return `<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>LAYRS ${x(config.label)}: ${x(t('Your walk'))}</name>
<Placemark><name>${x(t('Start'))}</name><Point><coordinates>${pt(w.start)}</coordinates></Point></Placemark>
${marks}
<Placemark><name>${x(t('Your walk'))}</name><LineString><tessellate>1</tessellate><coordinates>${line}</coordinates></LineString></Placemark>
</Document></kml>`;
}
function downloadKml(w) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([walkKml(w)], { type: 'application/vnd.google-earth.kml+xml' }));
  a.download = `layrs-${config.city}-walk.kml`;
  document.body.append(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(a.href), 2000);
}
// ---- on the map: a ribbon along the walk and a numbered disc over every stop
function discTexture(text, fill, ink) {
  const c = document.createElement('canvas'); c.width = c.height = 96;
  const g = c.getContext('2d');
  g.beginPath(); g.arc(48, 48, 40, 0, Math.PI * 2); g.fillStyle = fill; g.fill();
  g.lineWidth = 7; g.strokeStyle = '#ffffff'; g.stroke();
  g.fillStyle = ink; g.font = '800 44px "Schibsted Grotesk", Arial, sans-serif'; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillText(text, 48, 51);
  const t = new THREE.CanvasTexture(c); t.anisotropy = 4;
  return t;
}
// While a walk is shown the city is a plain model and only the walk's buildings carry colour (the graph's focus).
function lightWalk(w) {
  if (!w) { uniforms.uFocusN.value = 0; return; }
  const gids = [...new Set(w.stops.flatMap(p => p.bags.map(gidOf)))].filter(g => g >= 0).slice(0, FOCUS_MAX);
  uniforms.uFocus.value = [...gids, ...Array(FOCUS_MAX - gids.length).fill(-1)];
  uniforms.uFocusGroup.value = Array(FOCUS_MAX).fill(0);
  uniforms.uFocusN.value = gids.length;
}
function drawWalk(w) {
  walkGroup.clear();
  lightWalk(w);
  if (!w) return;
  const css = getComputedStyle(document.documentElement);
  const accent = css.getPropertyValue('--accent').trim() || css.getPropertyValue('--red').trim() || '#1f3f9a';
  const pts = w.route, pos = [];
  for (let i = 1; i < pts.length; i++) {
    const a = pts[i - 1], b = pts[i], len = dist(a, b) || 1, nx = -(b.z - a.z) / len * 3.5, nz = (b.x - a.x) / len * 3.5;
    pos.push(a.x + nx, 1, a.z + nz, a.x - nx, 1, a.z - nz, b.x + nx, 1, b.z + nz,
      a.x - nx, 1, a.z - nz, b.x - nx, 1, b.z - nz, b.x + nx, 1, b.z + nz);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
  const ribbon = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: accent, transparent: true, opacity: 0.85,
    side: THREE.DoubleSide, depthWrite: false, polygonOffset: true, polygonOffsetFactor: -4 }));
  walkGroup.add(ribbon);
  const marker = (p, text, fill, ink) => {
    const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: discTexture(text, fill, ink), depthTest: false, sizeAttenuation: false }));
    s.scale.set(0.034, 0.034, 1);
    s.position.set(p.x, 30, p.z);
    s.renderOrder = 20;
    walkGroup.add(s);
  };
  marker(w.start, '★', '#ffffff', accent);
  w.stops.forEach((p, i) => marker(p, String(i + 1), accent, '#ffffff'));
}
// ---- the planner
function startPoint() {
  if (walkPrefs.at) return walkPrefs.at;
  const s = STARTS[walkPrefs.start] || STARTS[0];
  return [s.x, s.z];
}
function renderWalkPlanner(msg = '') {
  const L = walkLayers(), sel = walkPrefs.layers;
  const startName = walkPrefs.at ? (walkPrefs.atLabel || t('Your point')) : L10(STARTS[walkPrefs.start]);
  document.getElementById('walks-body').innerHTML = `
    <h2 id="walks-title">${t('Plan a walk')}</h2>
    <p class="w-lede">${t('Choose what interests you, where you start and how far you want to go. The walk links the buildings with stories on the way.')}</p>
    <h3>${t('Where you start')}</h3>
    <div class="w-locate">${walkPrefs.atLabel === t('Your location')
      ? `<p class="w-note">${t('Start')}: ${esc(startName)}</p>`
      : `<button class="w-share" data-geo>${t(locating ? 'Asking for your location…' : 'Share my location')}</button>
         <p class="w-note">${t('Start from where you are: share your location, or choose a start below.')}</p>`}</div>
    <div class="w-chips">${STARTS.map((s, i) => `<button class="w-chip" data-start="${i}" aria-pressed="${!walkPrefs.at && walkPrefs.start === i}">${esc(L10(s))}</button>`).join('')}
      <button class="w-chip" data-pick aria-pressed="${walkPrefs.atLabel === t('Point on the map')}">${t('Pick on the map')}</button></div>
    ${walkPrefs.atLabel === t('Your location') ? '' : `<p class="w-note">${t('Start')}: ${esc(startName)}</p>`}
    <h3>${t('What interests you')}</h3>
    <div class="w-chips">${L.map(l => `<button class="w-chip" data-l="${l.id}" aria-pressed="${sel.includes(l.id)}">${sectionIcon(l.section)}${esc(tr(l, 'title'))}</button>`).join('')}</div>
    <p class="w-note">${sel.length ? '' : t('Nothing chosen: the walk takes every story.')}</p>
    <h3>${t('How far')}</h3>
    <div class="w-chips">${[1, 2, 3, 5, 8].map(k => `<button class="w-chip" data-km="${k}" aria-pressed="${walkPrefs.km === k}">${k} km</button>`).join('')}
      <span class="w-sep"></span>
      <button class="w-chip" data-loop="1" aria-pressed="${walkPrefs.loop}">${t('Back to the start')}</button>
      <button class="w-chip" data-loop="0" aria-pressed="${!walkPrefs.loop}">${t('One way')}</button></div>
    <h3>${t('How many stops')}</h3>
    <div class="w-chips">${[0, 5, 10, 15, 20].map(n => `<button class="w-chip" data-stops="${n}" aria-pressed="${walkPrefs.stops === n}">${n ? n : t('As many as fit')}</button>`).join('')}</div>
    ${msg ? `<p class="w-msg">${esc(msg)}</p>` : ''}
    <div class="w-go"><button class="w-make">${t('Make my walk')}</button></div>`;
  const body = document.getElementById('walks-body');
  body.querySelectorAll('[data-l]').forEach(b => b.onclick = () => {
    const id = b.dataset.l;
    walkPrefs.layers = sel.includes(id) ? sel.filter(x => x !== id) : [...sel, id];
    renderWalkPlanner();
  });
  body.querySelectorAll('[data-start]').forEach(b => b.onclick = () => { walkPrefs.start = +b.dataset.start; walkPrefs.at = null; walkPrefs.atLabel = null; renderWalkPlanner(); });
  body.querySelectorAll('[data-km]').forEach(b => b.onclick = () => { walkPrefs.km = +b.dataset.km; renderWalkPlanner(); });
  body.querySelectorAll('[data-stops]').forEach(b => b.onclick = () => { walkPrefs.stops = +b.dataset.stops; renderWalkPlanner(); });
  body.querySelectorAll('[data-loop]').forEach(b => b.onclick = () => { walkPrefs.loop = b.dataset.loop === '1'; renderWalkPlanner(); });
  body.querySelector('[data-geo]')?.addEventListener('click', requestLocation);
  body.querySelector('[data-pick]').onclick = () => { pickingStart = true; walksDlg.close(); showWalkHint(); };
  body.querySelector('.w-make').onclick = makeWalk;
}
let locating = false, locationAsked = false;
function requestLocation() {
  locationAsked = true;
  if (!navigator.geolocation) { renderWalkPlanner(t('This browser does not share its location.')); return; }
  locating = true; renderWalkPlanner();
  navigator.geolocation.getCurrentPosition(pos => {
    locating = false;
    const [x, z] = fromLatLon(pos.coords.latitude, pos.coords.longitude);
    if (Math.hypot(x, z) > 6000) { renderWalkPlanner(t('You seem to be outside the city, so the walk starts at {s}.').replace('{s}', L10(STARTS[0]))); return; }
    walkPrefs.at = [x, z]; walkPrefs.atLabel = t('Your location'); renderWalkPlanner();
  }, () => { locating = false; renderWalkPlanner(t('The location was not shared. Pick a start on the map instead.')); },
  { enableHighAccuracy: true, timeout: 10000 });
}
function showWalkHint() {
  walkEl.hidden = false;
  walkEl.className = 'walkcard';
  walkEl.innerHTML = `<header><b>${t('Plan a walk')}</b></header><p class="q-riddle">${t('Click the map where the walk should start.')}</p>
    <div class="q-actions"><button class="w-cancel">${t('Cancel')}</button></div>`;
  walkEl.querySelector('.w-cancel').onclick = () => { pickingStart = false; walkEl.hidden = true; openWalks(); };
}
// A click on the ground while picking: where the pointer ray meets the ground plane.
function groundAt(cx, cy) {
  const r = canvas.getBoundingClientRect();
  camera.updateMatrixWorld();
  const ray = new THREE.Raycaster();
  ray.setFromCamera(new THREE.Vector2((cx - r.left) / r.width * 2 - 1, -((cy - r.top) / r.height) * 2 + 1), camera);
  const hit = new THREE.Vector3();
  return ray.ray.intersectPlane(new THREE.Plane(new THREE.Vector3(0, 1, 0), 0), hit) ? [hit.x, hit.z] : null;
}
function makeWalk() {
  const w = planWalk(walkPrefs, startPoint());
  if (!w.stops.length) { renderWalkPlanner(t('No stories within reach. Try a longer walk or more interests.')); return; }
  walkRoute = w;
  walksDlg.close();
  drawWalk(w);
  walkEl.hidden = true;
  renderWalk();
  // on a phone a new walk opens folded to its bar, so the route on the map is what one sees first
  if (phone.matches) walkEl.classList.add('folded');
  const xs = w.route.map(p => p.x), zs = w.route.map(p => p.z);
  const span = Math.max(Math.max(...xs) - Math.min(...xs), Math.max(...zs) - Math.min(...zs));
  flyTo((Math.max(...xs) + Math.min(...xs)) / 2, (Math.max(...zs) + Math.min(...zs)) / 2, null, Math.max(600, span * 2.2));
  const u = new URL(location.href);
  if (walkPrefs.custom) u.searchParams.delete('walk'); else u.searchParams.set('walk', [walkPrefs.km, walkPrefs.loop ? 1 : 0, startPoint().map(Math.round).join('_'), walkPrefs.layers.join('.'), walkPrefs.stops].join('~'));
  history.replaceState(null, '', u);
}
function renderWalk() {
  const w = walkRoute;
  if (!w) return;
  const mins = Math.round(w.length / 1000 / WALK_KMH * 60 + w.stops.length * STOP_MIN);
  const inGoogle = new Set(googleStops(w));
  const folded = !walkEl.hidden && walkEl.classList.contains('folded');
  walkEl.hidden = false;
  walkEl.className = 'walkcard' + (folded ? ' folded' : '');
  walkEl.innerHTML = `
    <button class="q-close" aria-label="${t('Close')}">×</button>
    <header><b>${t('Your walk')}</b><span class="w-meta">${(w.length / 1000).toFixed(1).replace('.', LANG === 'nl' ? ',' : '.')} km · ${t('about {m} min').replace('{m}', mins)}</span></header>
    <div class="q-actions"><a class="w-google" href="${esc(googleUrl(w))}" target="_blank" rel="noopener">${t('Open in Google Maps')}</a>
      <button class="w-change">${t('Change')}</button>
      <button class="w-kml" title="${t('Download the walk with its stories (KML), for Google My Maps: Create a new map, then Import.')}" aria-label="${t('Download the walk with its stories (KML), for Google My Maps: Create a new map, then Import.')}"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 2v8m0 0-3-3m3 3 3-3M3 12.5v1.5h10v-1.5"/></svg></button></div>
    <ol class="w-stops">${w.stops.map((p, i) => {
      const pref = [...p.notes].sort((a, b) => (walkPrefs.layers.includes(b.L.id) ? 1 : 0) - (walkPrefs.layers.includes(a.L.id) ? 1 : 0));
      const story = pref.map(x => x.n.people ? `${t('Lived or worked here')}: ${x.n.people.map(q => q.person).join(', ')}` : tr(x.n, 'story')).find(Boolean) || '';
      const off = !inGoogle.has(p);
      return `<li${off ? ' class="w-off"' : ''}><button data-i="${i}"><span class="w-num">${i + 1}</span><span><b>${esc(poiName(p))}</b><em>${esc(story)}</em></span></button></li>`;
    }).join('')}</ol>
    <p class="q-credit">${walkPrefs.stops && w.stops.length < walkPrefs.stops ? t('Fewer stops than asked: that is all the stories you chose.') + ' ' : ''}${w.stretched ? t('Longer than asked: few of the stories you chose lie that close.') + ' '
      : w.length < walkPrefs.km * 600 ? t('Shorter than asked: the stories you chose lie close together.') + ' ' : ''}${t('Straight lines on the map; Google Maps shows the walking route.')}${inGoogle.size < w.stops.length
      ? ' ' + t('Google Maps takes nine stops; the paler ones lie on the way.') : ''}</p>`;
  markWalk();
  walkEl.querySelector('.q-close').onclick = () => { walkEl.hidden = true; walkRoute = null; drawWalk(null); markWalk();
    const u = new URL(location.href); u.searchParams.delete('walk'); history.replaceState(null, '', u); };
  walkEl.querySelector('.w-change').onclick = openWalks;
  walkEl.querySelector('.w-kml').onclick = () => downloadKml(w);
  // On a phone the list folds to its title bar and the Google Maps button; a tap on the bar opens it again.
  walkEl.querySelector('header').onclick = () => walkEl.classList.toggle('folded');
  walkEl.querySelectorAll('[data-i]').forEach(b => b.onclick = () => {
    const p = w.stops[+b.dataset.i], g = gidOf(p.bag);
    if (phone.matches) walkEl.classList.add('folded');
    flyTo(p.x, p.z, () => { if (g >= 0) pinCard(g, innerWidth / 3, innerHeight / 2); }, 330);
  });
}
// A walk straight from a layer's page or from the graph: the stories of that layer, or one stop per graph group.
function walkFromLayer(L) {
  walkPrefs = { ...walkPrefs, layers: [L.id], custom: null, stops: 0 };
  makeWalk();
}
function walkFromGroups(groups) {
  // One stop per building of the selection: a story's stop where it has one, else the building under the name of
  // its graph group (a person's several houses become several stops). Neighbours closer than 25 m merge later.
  const seen = new Set(), custom = [];
  for (const g of groups) for (const gid of g.gids) {
    const b = building(gid), own = pois().find(p => p.bags.includes(b.bag));
    const key = own ? own.bag : b.bag;
    if (seen.has(key)) continue;
    seen.add(key);
    const w = wiki[b.wk];
    custom.push(own ? { ...own, score: 1.5 + (w?.image ? 0.4 : 0) }
      : { bag: b.bag, bags: [b.bag], x: b.x, z: b.z, name: (w && tr(w, 'label')) || g.label, notes: [], score: 1 + (w?.image ? 0.4 : 0) });
  }
  walkPrefs = { ...walkPrefs, custom, stops: Math.min(MAX_STOPS, custom.length) };
  makeWalk();
}
function openWalks() {
  renderWalkPlanner();
  walksDlg.showModal();
  if (!locationAsked && !walkPrefs.at) requestLocation();  // the walk starts where the walker is, if they agree
}
document.querySelector('.walks-open').onclick = () => { walkPrefs.custom = null; openWalks(); };
walksDlg.querySelector('.about-close').onclick = () => walksDlg.close();
walksDlg.addEventListener('click', e => { if (e.target === walksDlg) walksDlg.close(); });
// A shared link restores the walk: ?walk=km~loop~x_z~layer.layer
{
  const q = new URLSearchParams(location.search).get('walk');
  if (q) {
    const [km, loop, at, ls, ns] = q.split('~');
    const [x, z] = (at || '').split('_').map(Number);
    walkPrefs = { km: +km || 3, loop: loop !== '0', start: 0, at: Number.isFinite(x) && Number.isFinite(z) ? [x, z] : null,
      atLabel: t('Point on the map'), stops: +ns || 0, layers: (ls || '').split('.').filter(id => layers.some(L => L.id === id)) };
    setTimeout(makeWalk, 0);
  }
}

// ---------- From the graph ----------
// graph.html opens the map with ./?focus=<id>,<id>: the buildings of those people, events or places light up,
// each selection in its own colour, and the rest of the city turns into a white model.
const focusEl = document.getElementById('focus');
const focusIds = (new URLSearchParams(location.search).get('focus') || '').split(',').filter(Boolean);
if (focusIds.length) fetch('data/graph.json').then(r => r.json()).then(G => showFocus(G, focusIds)).catch(() => {});
function showFocus(G, ids) {
  const groups = [];
  ids.forEach((id, i) => {
    const node = G.nodes.find(n => n.id === id), place = G.places[id];
    if (!node && !place) return;
    const bags = place ? place.bags : G.links.filter(l => l.e === id).flatMap(l => G.places[l.p].bags);
    const label = place ? place.name : (LANG === 'nl' && node.label_nl) || node.label;
    groups.push({ label, color: i % GROUP_COLORS.length, gids: [...new Set(bags)].map(gidOf).filter(g => g >= 0) });
  });
  const gids = [], grp = [];
  for (const g of groups) for (const gid of g.gids) {
    if (!gids.includes(gid) && gids.length < FOCUS_MAX) { gids.push(gid); grp.push(g.color); }
  }
  if (!gids.length) return;
  uniforms.uFocus.value = [...gids, ...Array(FOCUS_MAX - gids.length).fill(-1)];
  uniforms.uFocusGroup.value = [...grp, ...Array(FOCUS_MAX - grp.length).fill(0)];
  uniforms.uFocusN.value = gids.length;
  const pts = gids.map(building);
  const cx = pts.reduce((a, b) => a + b.x, 0) / pts.length, cz = pts.reduce((a, b) => a + b.z, 0) / pts.length;
  const spread = Math.max(...pts.map(b => Math.hypot(b.x - cx, b.z - cz)));
  flyTo(cx, cz, null, Math.min(4200, Math.max(380, spread * 2.4)));
  const back = `graph.html?select=${encodeURIComponent(ids.join(','))}${LANG === 'nl' ? '&lang=nl' : ''}`;
  focusEl.innerHTML = `<header><b>${t('From the graph')}</b><button class="f-close" aria-label="${t('Close')}">×</button></header>
    <ul>${groups.map(g => `<li><i style="background:${GROUP_COLORS[g.color]}"></i><span>${esc(g.label)}</span>
      <small>${g.gids.length}</small></li>`).join('')}</ul>
    <div class="f-actions"><button class="make-walk">${t('Generate a walk')}</button><a class="f-back" href="${back}">${t('Back to the graph')}</a></div>`;
  focusEl.hidden = false;
  focusEl.querySelector('.make-walk').onclick = () => { focusEl.hidden = true; walkFromGroups(groups); };
  focusEl.querySelector('.f-close').onclick = () => {
    uniforms.uFocusN.value = 0;
    focusEl.hidden = true;
    const u = new URL(location.href); u.searchParams.delete('focus'); history.replaceState(null, '', u);
  };
}

// ---------- Deep links ----------
// ?b=<building id> opens the map on one building with its card pinned; ?layer=<layer id> opens that context layer.
// The pages written for search engines and agents (stop-token, scripts/lab-pages.mjs) link here.
function openDeepLink() {
  const u = new URLSearchParams(location.search);
  const L = u.get('layer') && layers.find(L => L.id === u.get('layer'));
  if (L) { document.querySelector(`.modes button[data-mode="${MODE.layers}"]`)?.click(); setLayer(L); }
  const g = u.get('b') ? gidOf(u.get('b')) : -1;
  if (g >= 0) { const b = building(g); flyTo(b.x, b.z, () => pinCard(g, innerWidth * 0.62, innerHeight * 0.22), 320); }
}

// ---------- Panel ----------
const panelEl = document.getElementById('panel');
const panel = document.getElementById('panel-body');
const sheetHandle = panelEl.querySelector('.sheet-handle');
const phone = matchMedia('(max-width: 720px)');
// On a phone the panel is a sheet: folded to one line until opened, and folded again when the city is the point.
function setCollapsed(c) {
  panelEl.classList.toggle('collapsed', c);
  sheetHandle.setAttribute('aria-expanded', String(!c));
  sheetHandle.textContent = t('Legend');
  sheetHandle.setAttribute('aria-label', t(c ? 'Show legend' : 'Hide legend'));
}
let sheetSwiped = false;
sheetHandle.onclick = () => { if (sheetSwiped) { sheetSwiped = false; return; } setCollapsed(!panelEl.classList.contains('collapsed')); };
// On a phone the open legend folds when the map is touched, or when its bar is swiped down.
let sheetDown = null;
sheetHandle.addEventListener('pointerdown', e => { sheetDown = e.clientY; });
sheetHandle.addEventListener('pointerup', e => {
  if (sheetDown !== null && e.clientY - sheetDown > 30) { setCollapsed(true); sheetSwiped = true; }
  sheetDown = null;
});
document.getElementById('scene')?.addEventListener('pointerdown', () => {
  if (phone.matches && !panelEl.classList.contains('collapsed')) setCollapsed(true);
});
function collapsePanelOnPhone() { if (phone.matches) setCollapsed(true); }
// On a phone, choosing Layers in the mode bar opens the list of layers.
document.querySelector(`.modes button[data-mode="${MODE.layers}"]`)?.addEventListener('click', () => { if (phone.matches) setCollapsed(false); });
setCollapsed(phone.matches);
const totals = periods.map(() => 0);
for (const v of Object.values(config.histogram)) v.forEach((n, i) => totals[i] += n);
const fmt = n => n.toLocaleString(fmtLocale());
let activeLayer = null;
const SECTION_ORDER = ['Discover', 'Architecture', 'Trade and empire', 'Art and craft', 'Science and learning',
  'Faith and community', 'Countries and communities', 'The modern city', 'War and occupation'];
const groupOn = {};
let maskTarget = periods.map(() => 1);

const ICON = {
  'Buildings today': '<path d="M2.5 14.5h11"/><rect x="3" y="8" width="2.6" height="6.5"/><rect x="6.7" y="4" width="2.6" height="10.5"/><rect x="10.4" y="6" width="2.6" height="8.5"/>',
  'Art and craft': '<path d="M6 1.5h4M6.6 1.5v2.6C4.2 5.5 3.6 8 4 10.5c.4 2.4 1.9 4 4 4s3.6-1.6 4-4c.4-2.5-.2-5-2.6-6.4V1.5"/><path d="M5.2 8.5c1.8.8 3.8.8 5.6 0"/>',
  'Science and learning': '<path d="M6 1.5h4M6.8 1.5v4.5L3 13.2c-.4.7.1 1.3.9 1.3h8.2c.8 0 1.3-.6.9-1.3L9.2 6V1.5"/><path d="M4.6 10.5h6.8"/>',
  'Discover': '<circle cx="8" cy="8" r="6.2"/><path d="M10.6 5.4 9 9 5.4 10.6 7 7z"/>',
  'Architecture': '<path d="M3 14.5V7l5-4.5L13 7v7.5z"/><path d="M6.5 14.5v-4h3v4"/>',
  'Trade and empire': '<path d="M2 11h12l-1.8 3H3.8z"/><path d="M8 2v9M8 3l4.5 6H8"/>',
  'Faith and community': '<path d="M8 1.5v4M6.2 3.3h3.6"/><path d="M4 14.5V8.5L8 5.5l4 3v6z"/><path d="M7 14.5v-3h2v3"/>',
  'The modern city': '<rect x="2.5" y="5" width="5" height="9.5"/><rect x="8.5" y="2" width="5" height="12.5"/><path d="M4.5 7.5h1M4.5 10h1M10.5 4.5h1M10.5 7h1M10.5 9.5h1"/>',
  'War and occupation': '<path d="M8 1.8 13 4v4c0 3.2-2.2 5.3-5 6.3-2.8-1-5-3.1-5-6.3V4z"/>',
};
const sectionIcon = sec => `<svg class="icon" viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round">${ICON[sec] || ''}</svg>`;

const backToLayers = () => { uniforms.uMode.value = MODE.layers; renderPanel(); drawHist(); };
function renderPanel() {
  const mode = uniforms.uMode.value;
  if (mode === MODE.period) {
    panel.innerHTML = `<h2>${t('Built in')}</h2><div class="swatches">${periods.map((p, i) => `
      <button class="swatch" data-i="${i}" aria-pressed="${!!maskTarget[i]}">
        <i style="background:${p.color}"></i><span>${t(p.label)}</span><span class="n">${fmt(totals[i])}</span>
      </button>`).join('')}</div>
      <p class="note">${t('Click a period to see it alone. Paler buildings have an approximate year.')}</p>`;
    panel.querySelectorAll('.swatch').forEach(b => b.onclick = () => {
      const i = +b.dataset.i, m = maskTarget;
      const solo = m.every((v, j) => (j === i) === !!v);
      maskTarget = periods.map((_, j) => (solo || j === i) ? 1 : 0);
      renderPanel(); drawHist();
    });
  } else if (mode === MODE.floors) {
    panel.innerHTML = `<button class="back">${t('All layers')}</button><h2 class="layer-title">${sectionIcon('Buildings today')}${t('Storeys')}</h2>
      <div class="ramp" style="background:linear-gradient(90deg,#dbe3e6,#7da8bf,#2b5c8c,#0d1a40)"></div>
      <div class="ramp-scale"><span>1</span><span>3</span><span>8</span><span>20</span><span>40+</span></div>
      <p class="note">${LANG === 'nl' ? `${fmt(config.stats.floorsBag3d)} gebouwen krijgen hun verdiepingen uit het 3D BAG-model; de rest, ${fmt(config.stats.floorsHeight)}, uit hun hoogte gedeeld door 3,2 m.` : `${fmt(config.stats.floorsBag3d)} buildings take their storeys from the 3D BAG model; the rest, ${fmt(config.stats.floorsHeight)}, from their height divided by 3.2 m.`}</p>`;
    panel.querySelector('.back').onclick = backToLayers;
  } else if (mode === MODE.energy) {
    const e = config.energy;
    panel.innerHTML = `<button class="back">${t('All layers')}</button><h2 class="layer-title">${sectionIcon('Buildings today')}${t('Energy label')}</h2><div class="energy-scale">${e.labels.map((l, i) => `
      <div><i style="background:${ENERGY_COLORS[i + 1]}"></i><span>${l}</span><span class="n">${fmt(e.counts[i + 1])}</span></div>`).reverse().join('')}</div>
      <p class="note">${LANG === 'nl' ? `Het label dat de meeste woningen in een gebouw hebben. ${fmt(e.counts[0])} gebouwen, wit op de kaart, hebben geen geregistreerd label.` : `The label most homes in a building carry. ${fmt(e.counts[0])} buildings, white on the map, have no registered label.`}</p>
      <a class="src" href="https://www.atlasleefomgeving.nl/energielabels-van-gebouwen" target="_blank" rel="noopener">${t('RVO energy labels, via Atlas Leefomgeving')}</a>`;
    panel.querySelector('.back').onclick = backToLayers;
  } else if (activeLayer && activeLayer === residentsLayer) {
    const notes = Object.entries(residentsLayer?.notes || {});
    const people = notes.flatMap(([bag, n]) => n.people.map(p => ({ ...p, bag, at: n.at })))
      .sort((a, b) => b.links - a.links);
    panel.innerHTML = `<button class="back">${t('All layers')}</button><h2 class="layer-title">${esc(tr(residentsLayer, 'title'))}</h2>
      <button class="make-walk">${t('Generate a walk')}</button>
      <p class="layer-intro">${esc(tr(residentsLayer, 'text') || '')}</p>
      <input class="filter" type="search" placeholder="${t('Find a person')}" aria-label="${t('Find a person')}">
      <ul class="stories people">${people.map(p => `<li data-q="${esc((p.person + ' ' + (p.desc || '')).toLowerCase())}">
        <button class="story" data-bag="${p.bag}"><b>${esc(p.person)}</b>
        <span>${[p.born && p.died ? `${p.born}–${p.died}` : p.born, p.desc].filter(Boolean).map(esc).join(', ')}</span>
        <span class="addr">${esc(p.address)}</span></button></li>`).join('')}</ul>
      ${residentsLayer?.caveat ? `<p class="caveat">${esc(tr(residentsLayer, 'caveat'))}</p>` : ''}`;
    panel.querySelector('.back').onclick = () => setLayer(null);
    panel.querySelector('.make-walk').onclick = () => { collapsePanelOnPhone(); walkFromLayer(residentsLayer); };
    panel.querySelector('.filter').oninput = e => {
      const q = e.target.value.toLowerCase();
      panel.querySelectorAll('.people li').forEach(li => { li.hidden = q && !li.dataset.q.includes(q); });
    };
    panel.querySelectorAll('.story').forEach(b => b.onclick = () => {
      const n = residentsLayer.notes[b.dataset.bag];
      collapsePanelOnPhone();
      flyTo(n.at[0], n.at[1], () => { const gid = gidOf(b.dataset.bag); if (gid >= 0) pinCard(gid, innerWidth * 0.62, innerHeight * 0.18); });
    });
  } else if (!activeLayer) {
    const sections = [...new Set(contextLayers.map(L => L.section))].sort((a, b) => SECTION_ORDER.indexOf(a) - SECTION_ORDER.indexOf(b));
    const secTitle = sec => tr(contextLayers.find(L => L.section === sec), 'section');
    panel.innerHTML = `<nav class="jump" aria-label="${t('Layers')}">${sections.map(sec => `
      <button data-sec="${esc(sec)}" title="${esc(secTitle(sec))}" aria-label="${esc(secTitle(sec))}">${sectionIcon(sec)}</button>`).join('')}</nav>` +
      sections.map(sec => `<h2 class="section" id="sec-${sec.replace(/\W+/g, '-')}">${sectionIcon(sec)}${esc(secTitle(sec))}</h2><div class="layers">${contextLayers.filter(L => L.section === sec).map(L => `
      <button class="layer" data-id="${L.id}">
        <b>${esc(tr(L, 'title'))}</b><span class="n">${fmt(L.count)}</span><span class="era">${esc(tr(L, 'era'))}</span>
      </button>`).join('')}</div>`).join('');
    // The buildings as they are today: storeys and energy labels, first in the list.
    const labelled = config.energy.counts.slice(1).reduce((a, b) => a + b, 0);
    panel.querySelector('.jump').insertAdjacentHTML('afterbegin', `<button data-sec="today" title="${t('Buildings today')}" aria-label="${t('Buildings today')}">${sectionIcon('Buildings today')}</button>`);
    panel.querySelector('.jump').insertAdjacentHTML('afterend', `<h2 class="section" id="sec-today">${sectionIcon('Buildings today')}${t('Buildings today')}</h2>
      <div class="layers"><button class="layer view" data-view="floors"><b>${t('Storeys')}</b><span class="n">${fmt(config.stats.buildings)}</span><span class="era">${t('3D BAG')}</span></button>
      <button class="layer view" data-view="energy"><b>${t('Energy label')}</b><span class="n">${fmt(labelled)}</span><span class="era">${t('RVO')}</span></button></div>`);
    panel.querySelectorAll('.layer.view').forEach(b => b.onclick = () => setBuildingView(MODE[b.dataset.view]));
    panel.insertAdjacentHTML('beforeend', `<p class="contribute"><a href="https://github.com/alexbarakov/amsterdam-by-building/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener">${t('Add a layer on GitHub')}</a></p>`);
    panel.querySelectorAll('.jump button').forEach(b => b.onclick = () =>
      panel.querySelector(`#sec-${b.dataset.sec.replace(/\W+/g, '-')}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' }));
    panel.querySelectorAll('.layer:not(.view)').forEach(b => b.onclick = () => {
      const L = contextLayers.find(l => l.id === b.dataset.id);
      setLayer(L); fitToLayer(L);
    });
  } else {
    panel.innerHTML = `<button class="back">${t('All layers')}</button>
      <h2 class="layer-title">${sectionIcon(activeLayer.section)}${esc(tr(activeLayer, 'title'))}</h2><p class="layer-era">${esc(tr(activeLayer, 'era'))}</p>
      ${Object.values(activeLayer.notes || {}).some(n => n.at) ? `<button class="make-walk">${t('Generate a walk')}</button>` : ''}${layerDetail(activeLayer)}`;
    panel.querySelector('.make-walk')?.addEventListener('click', () => { collapsePanelOnPhone(); walkFromLayer(activeLayer); });
    panel.querySelector('.back').onclick = () => setLayer(null);
    panel.querySelectorAll('.story').forEach(b => b.onclick = () => {
      const n = activeLayer.notes[b.dataset.bag];
      collapsePanelOnPhone();
      flyTo(n.at[0], n.at[1], () => {
        const gid = gidOf(b.dataset.bag);
        if (gid >= 0) pinCard(gid, innerWidth * 0.62, innerHeight * 0.18);
      });
    });
    panel.querySelectorAll('.swatch').forEach(b => b.onclick = () => {
      groupOn[b.dataset.bit] = groupOn[b.dataset.bit] === false;
      setLayer(activeLayer); fitToLayer(activeLayer);
    });
  }
}

function layerDetail(L) {
  const groups = L.groups.length > 1 ? `<div class="swatches">${L.groups.map((g, i) => `
    <button class="swatch" data-bit="${g.bit}" aria-pressed="${groupOn[g.bit] !== false}">
      <i style="background:${GROUP_COLORS[i]}"></i><span>${esc(tr(g, 'label'))}</span><span class="n">${fmt(g.count)}</span>
    </button>`).join('')}</div>` : '';
  // One line per story: a building made of several BAG parts carries the same note on each.
  const seenName = new Set();
  const named = Object.entries(L.notes || {}).filter(([, n]) => n.name && n.at && !seenName.has(n.name) && seenName.add(n.name));
  const stories = named.length ? `<h2 class="section">${t('Buildings and their stories')}</h2><ul class="stories">${named.map(([bag, n]) => `
    <li><button class="story" data-bag="${bag}"><b>${esc(tr(n, 'name'))}</b><span>${esc(tr(n, 'story'))}</span></button></li>`).join('')}</ul>` : '';
  return `<div class="layer-detail"><p>${esc(tr(L, 'text'))}</p>${groups}${stories}
    ${L.caveat ? `<p class="caveat">${esc(tr(L, 'caveat'))}</p>` : ''}
    <a href="${L.source.url}" target="_blank" rel="noopener">${esc(tr(L.source, 'label'))}</a></div>`;
}

function fitToLayer(L) {
  if (!L) return;
  const bits = L.groups.filter(g => groupOn[g.bit] !== false).map(g => g.bit);
  if (!bits.length) return;
  const xs = [], zs = [], n = config.stats.buildings, st = config.attrStride;
  for (let gid = 0; gid < n; gid++) {
    const o = gid * st, lay0 = attrs.getUint32(o + 20, true), lay1 = attrs.getUint32(o + 24, true);
    if (bits.some(b => b < 32 ? (lay0 >>> b) & 1 : (lay1 >>> (b - 32)) & 1)) {
      xs.push(attrs.getFloat32(o + 36, true)); zs.push(attrs.getFloat32(o + 40, true));
    }
  }
  if (!xs.length) return;
  const cut = a => { a.sort((p, q) => p - q); const k = a.length > 50 ? Math.floor(a.length * 0.02) : 0; return [a[k], a[a.length - 1 - k]]; };
  const [x0, x1] = cut(xs), [z0, z1] = cut(zs);
  // On a wide screen the panel covers the left of the view: frame the points in the part to its right.
  const pr = !phone.matches && !panelEl.classList.contains('collapsed') ? panelEl.getBoundingClientRect().right : 0;
  const free = Math.max(0.4, 1 - pr / innerWidth);
  const half = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
  const span = Math.max(z1 - z0, (x1 - x0) / (camera.aspect * free), 120);
  const distance = Math.min(7000, Math.max(320, span / 2 / half * 1.35));
  const right = new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld, 0).setY(0).normalize();
  const shift = (pr / innerWidth / 2) * 2 * distance * half * camera.aspect;
  const cx = (x0 + x1) / 2 - right.x * shift, cz = (z0 + z1) / 2 - right.z * shift;
  if (Number.isFinite(cx) && Number.isFinite(cz) && Number.isFinite(distance)) flyTo(cx, cz, null, distance);
}

function setLayer(L) {
  if (L) uniforms.uLayerAt.value = performance.now() / 1000;
  activeLayer = L;
  const bits = Array(MAX_GROUPS).fill(-1);
  if (L) L.groups.forEach((g, i) => { if (i < MAX_GROUPS && groupOn[g.bit] !== false) bits[i] = g.bit; });
  uniforms.uGroupBit.value = bits;
  renderPanel(); drawHist();
}

document.querySelectorAll('.modes button[data-mode]').forEach(b => b.onclick = () => {
  uniforms.uMode.value = +b.dataset.mode;
  document.querySelectorAll('.modes button[data-mode]').forEach(x => x.setAttribute('aria-pressed', x === b));
  const bits = Array(MAX_GROUPS).fill(-1);
  if (activeLayer) activeLayer.groups.forEach((g, i) => { if (groupOn[g.bit] !== false) bits[i] = g.bit; });
  uniforms.uGroupBit.value = bits;
  if (uniforms.uMode.value === MODE.layers && activeLayer) uniforms.uLayerAt.value = performance.now() / 1000;
  // On a phone the sheet opens only when there is a choice to make: a layer to pick.
  if (!phone.matches || (uniforms.uMode.value === MODE.layers && !activeLayer)) setCollapsed(false);
  renderPanel(); drawHist();
});

// ---------- Timeline ----------
const hist = document.getElementById('hist');
const hctx = hist.getContext('2d');
const T0 = Math.floor(config.yearMin / 50) * 50, T1 = config.yearMax + 1;
const years = Object.entries(config.histogram).map(([y, v]) => [+y, v]);
const yMax = Math.max(...years.map(([, v]) => v.reduce((a, b) => a + b, 0)));
const xOf = y => (y - T0) / (T1 - T0) * hist.clientWidth;
const yearOf = x => Math.round(T0 + x / hist.clientWidth * (T1 - T0));

function layerGroupsShown() {
  if (uniforms.uMode.value !== MODE.layers || !activeLayer) return [];
  return activeLayer.groups.map((g, i) => ({ ...g, color: GROUP_COLORS[i] })).filter(g => groupOn[g.bit] !== false);
}

function visibleCount() {
  const Y = uniforms.uYear.value;
  const shown = layerGroupsShown();
  if (shown.length) return shown.reduce((n, g) => n + Object.entries(g.years).reduce((m, [y, c]) => m + (+y <= Y ? c : 0), 0), 0);
  let n = 0;
  for (const [y, v] of years) if (y <= Y) v.forEach((c, i) => { if (uniforms.uMode.value !== MODE.period || maskTarget[i]) n += c; });
  return n;
}

function drawHist() {
  const w = hist.clientWidth, h = hist.clientHeight, dpr = devicePixelRatio;
  hist.width = w * dpr; hist.height = h * dpr;
  hctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  hctx.clearRect(0, 0, w, h);
  const plotH = h - 20, bw = Math.max(1, w / (T1 - T0));
  const Y = uniforms.uYear.value, Yf = uniforms.uYearFrom.value;
  const shown = layerGroupsShown();
  const bar = (y, bh, top, color, on) => {
    hctx.fillStyle = color;
    hctx.globalAlpha = on ? (y <= Yf ? 0.3 : 1) : 0.18;
    hctx.fillRect(xOf(y), top - bh, bw, bh);
  };
  if (shown.length) {
    // Layer mode: the city in grey behind, the layer's own buildings in its colours.
    for (const [y, v] of years) {
      const bh = Math.sqrt(v.reduce((a, b) => a + b, 0) / yMax) * (plotH - 6);
      bar(y, bh, plotH, '#b9c0c4', false);
    }
    // Stack the groups per year; the stack's total height follows sqrt(total), split in proportion.
    const total = {};
    for (const g of shown) for (const [y, c] of Object.entries(g.years)) total[y] = (total[y] || 0) + c;
    const lMax = Math.max(1, ...Object.values(total));
    const stack = {};
    for (const g of shown) for (const [ys, c] of Object.entries(g.years)) {
      const y = +ys, full = Math.sqrt(total[ys] / lMax) * (plotH - 6) * 0.9, bh = full * c / total[ys];
      bar(y, bh, plotH - (stack[y] || 0), g.color, y <= Y);
      stack[y] = (stack[y] || 0) + bh;
    }
  } else {
    for (const [y, v] of years) {
      let top = plotH;
      v.forEach((c, i) => {
        if (!c) return;
        const bh = Math.sqrt(c / yMax) * (plotH - 6);
        const masked = uniforms.uMode.value === MODE.period && !maskTarget[i];
        bar(y, bh, top, periods[i].color, !masked && y <= Y);
        top -= bh;
      });
    }
  }
  hctx.globalAlpha = 1;
  hctx.fillStyle = '#5d6266';
  hctx.font = '500 11px "Schibsted Grotesk", sans-serif';
  const step = w < 500 ? 200 : 100;
  for (let y = Math.ceil(T0 / step) * step; y <= T1; y += step) hctx.fillText(y, Math.min(w - 28, Math.max(0, xOf(y) - 13)), h - 4);
  hctx.fillStyle = '#000';
  hctx.fillRect(xOf(Y) - 1, 0, 2, plotH);
  if (Yf >= T0) { hctx.fillStyle = '#5d6266'; hctx.fillRect(xOf(Yf) - 0.5, 0, 1, plotH); }
  // at the end of the timeline the map shows the city as it stands, not a year that reads like a date
  document.getElementById('year').textContent = Y >= config.yearMax ? t('Today') : Math.round(Y);
  document.getElementById('count').textContent = fmt(visibleCount());
}

let handle = null;
hist.addEventListener('pointerdown', e => {
  hist.setPointerCapture(e.pointerId);
  const x = e.offsetX;
  handle = Math.abs(x - xOf(uniforms.uYearFrom.value)) < Math.abs(x - xOf(uniforms.uYear.value)) ? 'uYearFrom' : 'uYear';
  moveHandle(x);
  stopPlay();
});
hist.addEventListener('pointermove', e => handle && moveHandle(e.offsetX));
hist.addEventListener('pointerup', () => handle = null);
function moveHandle(x) {
  const y = Math.max(T0, Math.min(config.yearMax, yearOf(x)));
  if (handle === 'uYear') uniforms.uYear.value = Math.max(y, uniforms.uYearFrom.value + 1);
  else uniforms.uYearFrom.value = Math.min(y, uniforms.uYear.value - 1);
  drawHist();
}

// Play: quickly through the sparse centuries, then slowly through the dense ones.
let playing = false, playT0 = 0, playStart = 0;
const playBtn = document.getElementById('play');
const playIcon = document.getElementById('play-icon');
const DURATION = (+new URLSearchParams(location.search).get('film') || 30) * 1000; // ?film=6 for a short film
function playYear(t) {
  const k = 0.35; // share of time spent before 1850
  return t < k ? T0 + (1850 - T0) * (t / k) : 1850 + (config.yearMax - 1850) * ((t - k) / (1 - k));
}
function startPlay() {
  playing = true; playStart = performance.now();
  if (uniforms.uYear.value >= config.yearMax) uniforms.uYear.value = T0;
  playT0 = 0;
  while (playT0 < 1 && playYear(playT0) < uniforms.uYear.value) playT0 += 0.001;
  playIcon.setAttribute('d', 'M4 2.5h3v11H4zM9 2.5h3v11H9z');
  uniforms.uPlaying.value = 1;
  playBtn.setAttribute('aria-label', t('Pause'));
}
function stopPlay() {
  playing = false;
  uniforms.uPlaying.value = 0;
  uniforms.uRise.value = 0.01;
  uniforms.uYear.value = Math.round(uniforms.uYear.value);
  playIcon.setAttribute('d', 'M4 2.5v11l9-5.5z');
  playBtn.setAttribute('aria-label', "Play the city's growth");
}
playBtn.onclick = () => playing ? stopPlay() : startPlay();

// ---------- Loop ----------
function resize() {
  const w = innerWidth, h = innerHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
  drawHist();
}
addEventListener('resize', resize);
// ---------- Search ----------
// The index (pipeline/s14_search.py) loads on the first use of the search box: street names and named buildings.
// House numbers live in one file per first letter of the street, loaded when needed.
let index = null;
const shards = {};
const normal = s => String(s).toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
const shardOf = key => /^[a-z]/.test(key) ? key[0] : '0';
function loadIndex() {
  index ??= fetch('data/search/index.json').then(r => r.json()).then(d => {
    d.streets = d.streets.map(([n, nb]) => ({ n, nb, key: normal(n) }));
    d.names.forEach(n => { n.key = normal(n[0]); n.keyNl = n[1] ? normal(n[1]) : null; });
    return d;
  });
  return index;
}
function numbersOf(st) {
  const k = shardOf(st.key);
  shards[k] ??= fetch(`data/search/${k}.json`).then(r => r.json());
  return shards[k].then(sh => sh[st.n] || []);
}
const findInput = document.getElementById('find-input');
const findList = document.getElementById('find-results');
const findSel = document.getElementById('find-sel');
// The field stands just right of the mode bar, whose width depends on the language and the fonts.
const findBox = findInput.closest('.find'), modesBar = document.querySelector('.modes');
function placeFind() {
  if (phone.matches) { findBox.style.left = ''; return; }
  // while in use it widens, and must stay on screen
  const open = findBox.matches(':focus-within') || !findSel.hidden;
  const w = open ? 300 : findBox.offsetWidth;
  findBox.style.left = `${Math.min(modesBar.getBoundingClientRect().right + 8, innerWidth - w - 16)}px`;
}
addEventListener('resize', placeFind);
document.fonts?.ready.then(placeFind);
setTimeout(placeFind, 0);
findInput.addEventListener('focus', placeFind);
findInput.addEventListener('blur', () => setTimeout(placeFind, 200));
let results = [], active = -1, searchSeq = 0;

const streetsFor = (d, k) => d.streets.filter(st => st.key.startsWith(k))
  .concat(d.streets.filter(st => !st.key.startsWith(k) && st.key.includes(k)));
async function search(q, d) {
  const k = normal(q);
  if (k.length < 2) return [];
  const out = [];
  const m = k.match(/^(.*\D)\s*(\d+)\s*([a-z]?)$/);
  if (m) {
    const want = +m[2], letter = m[3] || '', sk = m[1].trim();
    const streets = streetsFor(d, sk).slice(0, 4);
    const nums = await Promise.all(streets.map(numbersOf));
    streets.forEach((st, i) => {
      const a = nums[i];
      const exact = a.find(x => x[0].toLowerCase() === `${want}${letter}`) || a.find(x => parseInt(x[0]) === want);
      if (exact) { out.push({ kind: 'address', label: `${st.n} ${exact[0]}`, gid: exact[1] }); return; }
      // not in the register: the nearest number on the same side of the street
      const near = a.filter(x => parseInt(x[0]) % 2 === want % 2)
        .sort((p, q) => Math.abs(parseInt(p[0]) - want) - Math.abs(parseInt(q[0]) - want))[0];
      if (near) out.push({ kind: 'address', label: `${st.n} ${near[0]}`, gid: near[1],
        note: t('{n} is not in the register; nearest on the same side').replace('{n}', `${st.n} ${want}${letter}`) });
    });
  }
  const starts = n => n.key.startsWith(k) || !!n.keyNl?.startsWith(k);
  const named = d.names.filter(n => n.key.includes(k) || n.keyNl?.includes(k)).sort((p, q) => starts(q) - starts(p));
  for (const n of named.slice(0, 5)) out.push({ kind: n[3], label: LANG === 'nl' && n[1] ? n[1] : n[0], gid: n[2] });
  if (!m) for (const st of streetsFor(d, k).slice(0, 4)) out.push({ kind: 'street', label: st.n, street: st });
  return out.slice(0, 8);
}
const KIND = { address: 'Address', building: 'Building', person: 'Lived here', street: 'Street' };
function renderResults() {
  findList.innerHTML = results.map((r, i) => `<li role="option" data-i="${i}" aria-selected="${i === active}">
    <b>${esc(r.label)}</b><span>${t(KIND[r.kind])}${r.kind === 'street' ? ` · ${fmt(r.street.nb)} ${t('buildings')}` : ''}</span>
    ${r.note ? `<em>${esc(r.note)}</em>` : ''}</li>`).join('') || (findInput.value.trim().length > 1 ? `<li class="none">${t('Nothing found')}</li>` : '');
  findList.hidden = !findList.innerHTML;
  findInput.setAttribute('aria-expanded', String(!findList.hidden));
  findList.querySelectorAll('[data-i]').forEach(li => li.onmousedown = e => { e.preventDefault(); choose(results[+li.dataset.i]); });
}
findInput.addEventListener('focus', loadIndex);
findInput.addEventListener('input', async () => {
  const seq = ++searchSeq;
  const d = await loadIndex();
  const r = await search(findInput.value, d);
  if (seq !== searchSeq) return;   // a later keystroke already searched
  results = r; active = results.length ? 0 : -1;
  renderResults();
});
findInput.addEventListener('keydown', e => {
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    e.preventDefault();
    if (results.length) active = (active + (e.key === 'ArrowDown' ? 1 : -1) + results.length) % results.length;
    renderResults();
  } else if (e.key === 'Enter' && results[active]) { choose(results[active]); }
  else if (e.key === 'Escape') { findList.hidden = true; findInput.blur(); }
  e.stopPropagation();
});
findInput.addEventListener('blur', () => setTimeout(() => { findList.hidden = true; }, 150));

// What the search found stays lit while the rest of the city dims.
let found = null;
function setLit(gids) {
  pickData.fill(0);
  for (const g of gids) pickData[g * 4] = 255;
  pickTex.needsUpdate = true;
  uniforms.uPickOn.value = gids.length ? 1 : 0;
}
function clearFound() {
  found = null; findSel.hidden = true; setLit([]); orbit = false; placeFind();
}
async function choose(r) {
  findList.hidden = true; findInput.blur();
  findInput.value = r.label;
  found = r;
  renderSel();
  if (r.kind === 'street') {
    const gids = [...new Set((await numbersOf(r.street)).map(a => a[1]))];
    if (found !== r || !gids.length) return;
    setLit(gids);
    pinCard(-1);
    const bs = gids.map(building), xs = bs.map(b => b.x), zs = bs.map(b => b.z);
    const span = Math.max(Math.max(...xs) - Math.min(...xs), Math.max(...zs) - Math.min(...zs), 150);
    flyTo((Math.max(...xs) + Math.min(...xs)) / 2, (Math.max(...zs) + Math.min(...zs)) / 2, null, Math.min(5000, span * 1.5));
  } else {
    setLit([r.gid]);
    const b = building(r.gid);
    flyTo(b.x, b.z, () => { if (found === r) { pinCard(r.gid, innerWidth * 0.62, innerHeight * 0.2); orbit = true; } }, 300);
  }
}
function renderSel() {
  if (!found) { findSel.hidden = true; return; }
  findSel.innerHTML = `<span>${esc(found.label)}</span><button class="sel-clear" aria-label="${t('Clear')}">×</button>`;
  findSel.hidden = false;
  placeFind();
  findSel.querySelector('.sel-clear').onclick = () => { clearFound(); findInput.value = ''; };
}
addEventListener('keydown', e => { if (e.key === 'Escape' && found && !document.querySelector('dialog[open]')) { clearFound(); findInput.value = ''; } });

// The camera slowly circles what was found, until the viewer takes over.
let orbit = false;
canvas.addEventListener('pointerdown', () => { orbit = false; });
canvas.addEventListener('wheel', () => { orbit = false; }, { passive: true });
controls.autoRotateSpeed = 0.6;
const orbitTick = () => { controls.autoRotate = orbit && !flight; requestAnimationFrame(orbitTick); };
orbitTick();

function applyStaticText() {
  document.documentElement.lang = LANG;
  document.querySelector('.dek').textContent = t('Every building standing today, by age and historical context.');
  document.querySelector('.about-open').textContent = t('About');
  setTimeout(placeFind, 0);
  findInput.placeholder = t('Search'); findInput.setAttribute('aria-label', t('Search a building, address or street'));
  if (found) renderSel();
  document.querySelector('.walks-open span').textContent = LANG === 'nl' ? 'Route' : 'Walk';
  document.querySelectorAll('[data-lang-block]').forEach(a => { a.hidden = a.dataset.langBlock !== LANG; });
  document.querySelectorAll('.modes button[data-mode]').forEach(b => { b.textContent = t(b.dataset.label); });
  document.querySelector('.graph-open span').textContent = t('Graph');
  document.querySelector('.graph-open').href = LANG === 'nl' ? 'graph.html?lang=nl' : 'graph.html';
  document.querySelector('.quests-open span').textContent = LANG === 'nl' ? 'Raadsels' : 'Quests';  // short, so the bar fits a phone
  document.querySelector('.tally-count').childNodes[1].textContent = ' ' + t('buildings');
  document.querySelector('.howto').textContent = t('Drag to turn. Right-drag or Shift-drag to move. Scroll to zoom.');
  const ld = document.getElementById('loading'); if (ld.firstChild) ld.firstChild.textContent = t('Building the city') + ' ';
  playBtn.setAttribute('aria-label', t(playing ? 'Pause' : "Play the city's growth"));
  document.querySelectorAll('.lang [data-lang]').forEach(b => b.setAttribute('aria-pressed', b.dataset.lang === LANG));
  sheetHandle.textContent = t('Legend');
  sheetHandle.setAttribute('aria-label', t(panelEl.classList.contains('collapsed') ? 'Show legend' : 'Hide legend'));
}
document.querySelectorAll('.modes button[data-mode]').forEach(b => { b.dataset.label = b.textContent.trim(); });
const about = document.getElementById('about');
document.querySelector('.about-open').onclick = () => about.showModal();
about.querySelector('.about-close').onclick = () => about.close();
about.addEventListener('click', e => { if (e.target === about) about.close(); });

function setLang(l) {
  LANG = l;
  try { localStorage.setItem('lang', l); } catch {}
  const u = new URL(location.href); u.searchParams.set('lang', l); history.replaceState(null, '', u);
  applyStaticText(); renderPanel(); drawHist();
  if (pinnedGid >= 0) pinCard(pinnedGid, ...lastPin);
  if (quest && !questEl.hidden && !questEl.classList.contains('done')) renderQuest();
  if (questsDlg.open) renderQuestList();
  if (walksDlg.open) renderWalkPlanner();
  if (walkRoute) renderWalk();
}
document.querySelectorAll('.lang [data-lang]').forEach(b => b.onclick = () => setLang(b.dataset.lang));
applyStaticText();
renderPanel();
resize();
document.fonts?.ready.then(drawHist);

let frame = 0;
renderer.setAnimationLoop(now => {
  frame++;
  stepFlight(now);
  uniforms.uNow.value = now / 1000;
  uniforms.uMask.value = maskTarget;
  controls.update();
  const dist = camera.position.distanceTo(controls.target);
  uniforms.uFog.value.set(dist * 1.6, dist * 4);
  if (frame % 6 === 0) updateLabels(dist);
  if (playing) {
    const t = Math.min(1, playT0 + (now - playStart) / DURATION);
    uniforms.uYear.value = playYear(t);
    // A flight lasts about 0.8 s on screen whatever the film's pace: as many years as the film covers in that time.
    uniforms.uRise.value = Math.max(2, (playYear(Math.min(1, t + 800 / DURATION)) - playYear(t)));
    if (t >= 1) stopPlay();
    drawHist();
  }
  if (pointer && !dragging && frame % 3 === 0) {
    const gid = pick(pointer[0], pointer[1]);
    uniforms.uHover.value = gid;
    showCard(gid, pointer[0], pointer[1]);
  }
  renderer.render(scene, camera);
});


window.__dbg = { loadIndex, search, choose, numbersOf, pick, uniforms, camera, controls, setLayer, layers, pinCard, showCard, building, labelGroup, labels, flyTo, startPlay, gidOf, questClick, startQuest, get quests() { return quests; } };
