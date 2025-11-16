import { createRng } from '../utils/random.js';
import { normalize } from '../utils/text.js';

const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';

function buildMapping(seed = 0) {
  const rng = createRng(seed);
  const letters = alphabet.split('');
  for (let i = letters.length - 1; i > 0; i -= 1) {
    const j = Math.floor(rng() * (i + 1));
    [letters[i], letters[j]] = [letters[j], letters[i]];
  }
  const map = new Map();
  alphabet.split('').forEach((letter, index) => {
    map.set(letter, letters[index]);
  });
  return map;
}

export function buildCryptogram(entries, seed = 0) {
  const text = entries.map((entry) => entry.clue).join(' ');
  const normalized = normalize(text).replace(/\d+/g, '');
  const map = buildMapping(seed || normalized.length);
  const encoded = normalized
    .split('')
    .map((char) => map.get(char) || char)
    .join('');
  return { encoded, map, text: normalized };
}

export function renderCryptogram(result, container, legendContainer) {
  if (!result) return;
  container.innerHTML = '';
  legendContainer.innerHTML = '';
  const area = document.createElement('div');
  area.className = 'cryptogram-area';
  const text = document.createElement('p');
  text.className = 'crypto-text';
  text.textContent = result.encoded;
  area.appendChild(text);

  const mapBox = document.createElement('div');
  mapBox.className = 'crypto-map';
  alphabet.split('').forEach((letter) => {
    const label = document.createElement('label');
    label.innerHTML = `<span>${letter}</span>`;
    const input = document.createElement('input');
    input.maxLength = 1;
    input.dataset.target = result.map.get(letter);
    label.appendChild(input);
    mapBox.appendChild(label);
  });
  area.appendChild(mapBox);
  container.appendChild(area);
}

export function createCryptogramPdf(result) {
  if (!result) return null;
  const wrapper = document.createElement('div');
  wrapper.innerHTML = '<h2>Şifreli Alfabe</h2>';
  const cipher = document.createElement('p');
  cipher.textContent = result.encoded;
  wrapper.appendChild(cipher);
  return [
    { title: 'Şifreli Alfabe', html: wrapper.outerHTML },
  ];
}
