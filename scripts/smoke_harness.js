// Smoke harness: serve site/, mock Open-Meteo minimally, abort every other external call,
// load each page, collect page errors + console errors, screenshot. Exit 1 on any page error.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http');
const SITE = process.argv[2], OUT = process.argv[3];
fs.mkdirSync(OUT, { recursive: true });
const mime = { '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.png': 'image/png', '.svg': 'image/svg+xml', '.json': 'application/json' };
const srv = http.createServer((req, res) => {
  let p = path.join(SITE, decodeURIComponent(req.url.split('?')[0]));
  if (p.endsWith('/')) p += 'index.html';
  if (fs.existsSync(p) && fs.statSync(p).isFile()) { res.writeHead(200, { 'content-type': mime[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res); }
  else { res.writeHead(404); res.end(); }
}).listen(8766);

function daily(n){ const t=[],mx=[],mn=[],pr=[],sn=[]; const d=new Date(Date.UTC(2024,0,1)); for(let i=0;i<n;i++){ t.push(d.toISOString().slice(0,10)); mx.push(60+10*Math.sin(i/58)); mn.push(40+10*Math.sin(i/58)); pr.push(i%5?0:0.3); sn.push(0); d.setUTCDate(d.getUTCDate()+1);} return {time:t,temperature_2m_max:mx,temperature_2m_min:mn,precipitation_sum:pr,snowfall_sum:sn,rain_sum:pr,sunrise:t.map(x=>x+'T07:00'),sunset:t.map(x=>x+'T19:00')}; }
const omForecast = { latitude: 40.5, longitude: -86.83, elevation: 165, timezone: 'America/Indiana/Indianapolis',
  current: { time: '2026-10-06T13:00', temperature_2m: 61, weather_code: 2, is_day: 1, relative_humidity_2m: 55, wind_speed_10m: 8, wind_direction_10m: 240, surface_pressure: 1012, cloud_cover: 40, apparent_temperature: 60, precipitation: 0 },
  hourly: { time: Array.from({length:48},(_,i)=>'2026-10-06T'+String(i%24).padStart(2,'0')+':00'), temperature_2m: Array(48).fill(60), wind_speed_10hPa: Array(48).fill(30), wind_direction_10hPa: Array(48).fill(270), wind_speed_850hPa: Array(48).fill(20), wind_direction_850hPa: Array(48).fill(250), wind_speed_700hPa: Array(48).fill(25), wind_direction_700hPa: Array(48).fill(260), wind_speed_500hPa: Array(48).fill(40), wind_direction_500hPa: Array(48).fill(270), precipitation_probability: Array(48).fill(10), weather_code: Array(48).fill(2), relative_humidity_2m: Array(48).fill(50), dew_point_2m: Array(48).fill(45), pressure_msl: Array(48).fill(1012), cloud_cover: Array(48).fill(40), uv_index: Array(48).fill(3), us_aqi: Array(48).fill(30), pm2_5: Array(48).fill(5), ozone: Array(48).fill(60) },
  daily: daily(16) };
const omArchive = { latitude: 40.5, longitude: -86.83, timezone: 'America/Indiana/Indianapolis', daily: daily(1010) };

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const pages = ['index.html', 'atlas.html', 'calendar.html', 'directory.html', 'signals.html', 'society.html', 'about.html'];
  let bad = 0;
  for (const name of pages) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, timezoneId: 'America/Los_Angeles' });  // viewer far from the region: the site must still keep local time
    const page = await ctx.newPage();
    const errs = [], cons = [], ext = new Set();
    page.on('pageerror', e => errs.push(String(e && e.message || e)));
    page.on('console', m => { if (m.type() === 'error') cons.push(m.text()); });
    await page.route('**/*', route => {
      const u = route.request().url();
      if (u.startsWith('http://localhost:8766')) return route.continue();
      ext.add(new URL(u).host);
      if (/cdnjs\.cloudflare\.com.*maplibre-gl\.min\.js/.test(u)) { const p = '/home/claude/kit/community-field-guide-starter-kit-v1/scripts/signals_harness/node_modules/maplibre-gl/dist/maplibre-gl.js'; if (fs.existsSync(p)) return route.fulfill({ body: fs.readFileSync(p), contentType: 'application/javascript' }); }
      if (/open-meteo\.com\/v1\/(forecast|air-quality)/.test(u)) return route.fulfill({ json: omForecast });
      if (/archive-api\.open-meteo\.com/.test(u)) return route.fulfill({ json: omArchive });
      return route.abort();
    });
    await page.goto('http://localhost:8766/' + name, { waitUntil: 'load' });
    await page.waitForTimeout(2500);
    const info = await page.evaluate(() => ({
      title: document.title,
      brand: (document.querySelector('.brand .stack') || {}).textContent,
      sun: (document.getElementById('skySun') || {}).textContent,
      temp: (document.getElementById('skyTemp') || {}).textContent,
      place: window.PLACE && window.PLACE.brand, tz: window.TZ, center: window.CENTER && [window.CENTER.lat, window.CENTER.lng],
      mapHome: (typeof HOME !== 'undefined') ? HOME : null,
      mapCenter: (window.map && window.map.getCenter) ? [window.map.getCenter().lat.toFixed(3), window.map.getCenter().lng.toFixed(3), window.map.getZoom()] : (typeof map!=='undefined' && map.getCenter ? [map.getCenter().lat.toFixed(3), map.getCenter().lng.toFixed(3), map.getZoom()] : null),
      tickerCount: document.querySelectorAll('.ticker-set span.tg').length,
      night: document.documentElement.getAttribute('data-theme'),
      bodyText: document.body.innerText.length
    }));
    await page.screenshot({ path: path.join(OUT, name.replace('.html', '.png')), fullPage: name !== 'index.html' && name !== 'atlas.html' });
    console.log(`\n== ${name}`, JSON.stringify(info));
    console.log('   external hosts:', [...ext].join(', '));
    if (errs.length) { bad++; console.log('   PAGE ERRORS:', errs); }
    if (cons.length) console.log('   console errors:', cons.slice(0, 6));
    await ctx.close();
  }
  await browser.close(); srv.close();
  process.exit(bad ? 1 : 0);
})();
