import { createRng } from '../utils/random.js';

export function buildAkrostis(entries, seed = 0) {
  if (!entries.length) return null;
  const rng = createRng(seed);
  const shuffled = entries.map((entry) => {
    const letters = entry.answer.split('');
    for (let i = letters.length - 1; i > 0; i -= 1) {
      const j = Math.floor(rng() * (i + 1));
      [letters[i], letters[j]] = [letters[j], letters[i]];
    }
    const mixed = letters.join('');
    return mixed === entry.answer ? entry.answer.slice(1) + entry.answer[0] : mixed;
  });
  const keyword = entries.map((entry) => entry.answer[0]).join('');
  return { entries, shuffled, keyword };
}

export function renderAkrostis(result, container, legendContainer) {
  if (!result) return;
  container.innerHTML = '';
  legendContainer.innerHTML = '';
  const list = document.createElement('div');
  result.entries.forEach((entry, index) => {
    const row = document.createElement('div');
    row.className = 'akrostis-row';
    row.innerHTML = `<strong>${index + 1}.</strong>`;
    const clue = document.createElement('span');
    clue.textContent = entry.clue;
    const input = document.createElement('input');
    input.value = result.shuffled[index];
    input.readOnly = true;
    row.append(clue, input);
    list.appendChild(row);
  });
  container.appendChild(list);

  const keywordBox = document.createElement('div');
  keywordBox.className = 'legend-section';
  keywordBox.innerHTML = '<h3>Şifre</h3>';
  const boxes = document.createElement('div');
  boxes.style.display = 'flex';
  boxes.style.gap = '8px';
  result.keyword.split('').forEach(() => {
    const slot = document.createElement('div');
    slot.style.width = '40px';
    slot.style.height = '40px';
    slot.style.border = '2px solid rgba(255,255,255,0.3)';
    slot.style.borderRadius = '8px';
    boxes.appendChild(slot);
  });
  keywordBox.appendChild(boxes);
  legendContainer.appendChild(keywordBox);
}

export function createAkrostisPdf(result) {
  if (!result) return null;
  const blank = document.createElement('div');
  blank.innerHTML = '<h2>Akrostiş</h2>';
  const list = document.createElement('ol');
  result.entries.forEach((entry) => {
    const li = document.createElement('li');
    li.textContent = `${entry.clue} (${entry.answer.length})`;
    list.appendChild(li);
  });
  blank.appendChild(list);
  const solved = document.createElement('p');
  solved.textContent = `Anahtar kelime: ${result.keyword}`;
  blank.appendChild(solved);
  return [
    { title: 'Akrostiş', html: blank.outerHTML },
  ];
}
