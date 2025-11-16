import { createRng } from '../utils/random.js';
import { gridToDataUrl } from '../utils/canvas.js';

const MIN_SIZE = 11;
const MAX_SIZE = 25;

function makeGrid(size) {
  return Array.from({ length: size }, () => Array(size).fill(null));
}

function autoSize(entries) {
  const total = entries.reduce((acc, cur) => acc + cur.answer.length, 0);
  const base = Math.max(MIN_SIZE, Math.ceil(Math.sqrt(total * 1.4)) + 2);
  const odd = base % 2 === 0 ? base + 1 : base;
  return Math.min(MAX_SIZE, odd);
}

function canPlace(grid, word, row, col, dir) {
  const size = grid.length;
  const dr = dir === 'across' ? 0 : 1;
  const dc = dir === 'across' ? 1 : 0;
  const len = word.length;
  if (row + dr * (len - 1) >= size || col + dc * (len - 1) >= size) return false;
  if (row - dr >= 0 && col - dc >= 0 && grid[row - dr][col - dc]) return false;
  if (
    row + dr * len < size &&
    col + dc * len < size &&
    grid[row + dr * len]?.[col + dc * len]
  ) {
    return false;
  }
  for (let i = 0; i < len; i += 1) {
    const r = row + dr * i;
    const c = col + dc * i;
    const existing = grid[r][c];
    if (existing && existing !== word[i]) return false;
    const around = [
      grid[r + (dir === 'across' ? 1 : 0)]?.[c + (dir === 'across' ? 0 : 1)],
      grid[r - (dir === 'across' ? 1 : 0)]?.[c - (dir === 'across' ? 0 : 1)],
    ];
    if (!existing && around.some(Boolean)) return false;
  }
  return true;
}

function placeWord(grid, word, row, col, dir) {
  const dr = dir === 'across' ? 0 : 1;
  const dc = dir === 'across' ? 1 : 0;
  for (let i = 0; i < word.length; i += 1) {
    grid[row + dr * i][col + dc * i] = word[i];
  }
  return { row, col, dir };
}

function annotate(grid) {
  const size = grid.length;
  const numbers = Array.from({ length: size }, () => Array(size).fill(null));
  let counter = 0;
  const across = [];
  const down = [];
  for (let r = 0; r < size; r += 1) {
    for (let c = 0; c < size; c += 1) {
      if (!grid[r][c]) continue;
      const startAcross = c === 0 || !grid[r][c - 1];
      const startDown = r === 0 || !grid[r - 1]?.[c];
      if (!startAcross && !startDown) continue;
      counter += 1;
      numbers[r][c] = counter;
      if (startAcross) {
        let word = '';
        let k = c;
        while (k < size && grid[r][k]) {
          word += grid[r][k];
          k += 1;
        }
        across.push({ number: counter, answer: word });
      }
      if (startDown) {
        let word = '';
        let k = r;
        while (k < size && grid[k][c]) {
          word += grid[k][c];
          k += 1;
        }
        down.push({ number: counter, answer: word });
      }
    }
  }
  return { numbers, across, down };
}

export function buildCrossword(entries, desiredSize, seed = 0) {
  if (!entries.length) return null;
  const size = desiredSize === 'auto' ? autoSize(entries) : Number(desiredSize);
  const grid = makeGrid(size);
  const rng = createRng(seed);
  const ordered = [...entries].sort((a, b) => b.answer.length - a.answer.length);
  const placed = [];
  const first = ordered.shift();
  const startCol = Math.max(0, Math.floor((size - first.answer.length) / 2));
  placeWord(grid, first.answer, Math.floor(size / 2), startCol, 'across');
  placed.push({ ...first, row: Math.floor(size / 2), col: startCol, dir: 'across' });

  for (const entry of ordered) {
    const matches = [];
    for (let r = 0; r < size; r += 1) {
      for (let c = 0; c < size; c += 1) {
        if (!grid[r][c]) continue;
        const idx = entry.answer.indexOf(grid[r][c]);
        if (idx === -1) continue;
        const col = c - idx;
        if (canPlace(grid, entry.answer, r, col, 'across')) {
          matches.push({ row: r, col, dir: 'across' });
        }
        const row = r - idx;
        if (canPlace(grid, entry.answer, row, c, 'down')) {
          matches.push({ row, col: c, dir: 'down' });
        }
      }
    }
    const pick = matches[Math.floor(rng() * matches.length)] || null;
    if (pick) {
      placeWord(grid, entry.answer, pick.row, pick.col, pick.dir);
      placed.push({ ...entry, ...pick });
    }
  }
  const meta = annotate(grid);
  return { grid, ...meta, placed };
}

export function renderCrossword(result, container, legendContainer) {
  if (!result) return;
  const { grid, numbers, across, down } = result;
  container.innerHTML = '';
  const gridEl = document.createElement('div');
  gridEl.className = 'crossword-grid';
  gridEl.style.gridTemplateColumns = `repeat(${grid.length}, 36px)`;
  const inputs = [];
  for (let r = 0; r < grid.length; r += 1) {
    for (let c = 0; c < grid.length; c += 1) {
      const cell = document.createElement('div');
      cell.className = 'crossword-cell';
      if (!grid[r][c]) {
        cell.classList.add('black');
        gridEl.appendChild(cell);
        continue;
      }
      const input = document.createElement('input');
      input.maxLength = 1;
      input.autocomplete = 'off';
      input.dataset.row = r;
      input.dataset.col = c;
      input.dataset.solution = grid[r][c];
      input.ariaLabel = `Satır ${r + 1}, Sütun ${c + 1}`;
      cell.appendChild(input);
      if (numbers[r][c]) {
        const badge = document.createElement('span');
        badge.className = 'num';
        badge.textContent = numbers[r][c];
        cell.appendChild(badge);
      }
      inputs.push(input);
      gridEl.appendChild(cell);
    }
  }
  container.appendChild(gridEl);

  legendContainer.innerHTML = '';
  const acrossBox = document.createElement('div');
  acrossBox.className = 'legend-section';
  acrossBox.innerHTML = '<h3>Yatay</h3>';
  const acrossList = document.createElement('ol');
  across.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = `${item.number}. (${item.answer.length})`;
    acrossList.appendChild(li);
  });
  acrossBox.appendChild(acrossList);

  const downBox = document.createElement('div');
  downBox.className = 'legend-section';
  downBox.innerHTML = '<h3>Dikey</h3>';
  const downList = document.createElement('ol');
  down.forEach((item) => {
    const li = document.createElement('li');
    li.textContent = `${item.number}. (${item.answer.length})`;
    downList.appendChild(li);
  });
  downBox.appendChild(downList);

  legendContainer.append(acrossBox, downBox);
}

export function createCrosswordPdf(result) {
  if (!result) return null;
  const blank = gridToDataUrl(result.grid, result.numbers, { showLetters: false });
  const solved = gridToDataUrl(result.grid, result.numbers, { showLetters: true });
  return [
    { title: 'Kare Bulmaca', images: [{ src: blank, alt: 'Boş bulmaca' }, { src: solved, alt: 'Cevaplı bulmaca' }] },
  ];
}
