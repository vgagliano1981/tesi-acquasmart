const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');

const html = fs.readFileSync('c:/Pregetto_tesi_sperimentale/frontend/index.html', 'utf8');
const dom = new JSDOM(html);
global.window = dom.window;
global.document = dom.window.document;
global.Chart = { defaults: { font: {} } };
global.Chart = function() { return { data: { labels: [], datasets: [] }, update: () => {} }; };
global.Chart.defaults = { color: '', font: {} };
global.fetch = () => Promise.resolve({ json: () => Promise.resolve([]), ok: true });

try {
    require('c:/Pregetto_tesi_sperimentale/frontend/app.js');
    console.log('No synchronous errors during load!');
} catch(e) {
    console.error('ERROR:', e);
}
