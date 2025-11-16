import { normalize } from '../utils/text.js';

function validateWords(entries) {
  if (entries.length < 2) return { start: '', end: '', steps: [] };
  const start = entries[0].answer;
  const end = entries[entries.length - 1].answer;
  if (start.length !== end.length) return { start, end, steps: [] };
  const steps = entries.slice(1, -1).map((entry) => entry.answer);
  return { start, end, steps };
}

export function buildLadder(entries) {
  const prepared = entries.map((entry) => ({ ...entry, answer: normalize(entry.answer) }));
  return validateWords(prepared);
}

export function renderLadder(result, container, legendContainer) {
  container.innerHTML = '';
  legendContainer.innerHTML = '';
  const wrapper = document.createElement('div');
  wrapper.className = 'ladder';
  const allSteps = [result.start, ...result.steps, result.end];
  allSteps.forEach((word, index) => {
    const row = document.createElement('div');
    row.className = 'ladder-row';
    const label = document.createElement('strong');
    label.textContent = index === 0 ? 'Başlangıç' : index === allSteps.length - 1 ? 'Bitiş' : `Adım ${index}`;
    const input = document.createElement('input');
    input.value = word;
    input.readOnly = index === 0 || index === allSteps.length - 1;
    row.append(label, input);
    wrapper.appendChild(row);
  });
  container.appendChild(wrapper);
}

export function createLadderPdf(result) {
  const wrapper = document.createElement('div');
  wrapper.innerHTML = '<h2>Söz Zinciri</h2>';
  const list = document.createElement('ol');
  [result.start, ...result.steps, result.end].forEach((word) => {
    const li = document.createElement('li');
    li.textContent = word;
    list.appendChild(li);
  });
  wrapper.appendChild(list);
  return [{ title: 'Söz Zinciri', html: wrapper.outerHTML }];
}
