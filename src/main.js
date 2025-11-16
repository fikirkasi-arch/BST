import { state, loadProgress, persistProgress, resetProgress, updateEntries } from './state.js';
import { buildCrossword, renderCrossword, createCrosswordPdf } from './puzzles/crossword.js';
import { buildAkrostis, renderAkrostis, createAkrostisPdf } from './puzzles/akrostis.js';
import { buildCryptogram, renderCryptogram, createCryptogramPdf } from './puzzles/cryptogram.js';
import { buildLadder, renderLadder, createLadderPdf } from './puzzles/ladder.js';
import { renderPrintable, printNow } from './ui/print.js';
import { wireCrossword } from './ui/crosswordPlay.js';

const SAMPLE = `ANKARA | Türkiye'nin başkenti nedir?\nALGORITMA | Programlamada işlem adımları?\nKEDILER | Miyavlayan evcil hayvanlar?\nGALATASARAY | Sarı kırmızı renkleri olan takım?`;

const refs = {
  bulkInput: document.getElementById('bulkInput'),
  gridSize: document.getElementById('gridSize'),
  seed: document.getElementById('seedValue'),
  mode: document.getElementById('modeSelect'),
  status: document.getElementById('statusMessage'),
  interactive: document.getElementById('interactiveArea'),
  legend: document.getElementById('legendArea'),
  modeTitle: document.getElementById('modeTitle'),
  printMode: document.getElementById('printMode'),
  printAll: document.getElementById('printAll'),
  resetProgress: document.getElementById('resetProgress'),
  generate: document.getElementById('generate'),
  sample: document.getElementById('sampleData'),
  clear: document.getElementById('clearData'),
};

const modeLabels = {
  crossword: 'Kare Bulmaca',
  akrostis: 'Akrostiş',
  cryptogram: 'Şifreli Alfabe',
  ladder: 'Söz Zinciri',
};

loadProgress();

function hydrateFromState() {
  if (state.entries.length) {
    refs.bulkInput.value = state.entries.map((entry) => `${entry.answer} | ${entry.clue}`).join('\n');
  } else {
    refs.bulkInput.value = SAMPLE;
  }
  refs.gridSize.value = state.gridSize;
  refs.seed.value = state.seed;
  refs.mode.value = state.mode;
}

hydrateFromState();

function setStatus(message) {
  refs.status.textContent = message;
}

function buildCurrent() {
  const entries = updateEntries(refs.bulkInput.value);
  state.mode = refs.mode.value;
  state.gridSize = refs.gridSize.value;
  state.seed = Number(refs.seed.value) || 0;
  persistProgress();
  if (!entries.length) {
    setStatus('Geçerli satır bulunamadı.');
    refs.interactive.innerHTML = '';
    refs.legend.innerHTML = '';
    return;
  }
  refs.modeTitle.textContent = modeLabels[state.mode];
  let printable = null;
  if (state.mode === 'crossword') {
    state.result = buildCrossword(entries, state.gridSize, state.seed);
    renderCrossword(state.result, refs.interactive, refs.legend);
    wireCrossword(refs.interactive);
    printable = createCrosswordPdf(state.result);
  } else if (state.mode === 'akrostis') {
    state.result = buildAkrostis(entries, state.seed);
    renderAkrostis(state.result, refs.interactive, refs.legend);
    printable = createAkrostisPdf(state.result);
  } else if (state.mode === 'cryptogram') {
    state.result = buildCryptogram(entries, state.seed);
    renderCryptogram(state.result, refs.interactive, refs.legend);
    printable = createCryptogramPdf(state.result);
  } else {
    state.result = buildLadder(entries);
    renderLadder(state.result, refs.interactive, refs.legend);
    printable = createLadderPdf(state.result);
  }
  renderPrintable(printable);
  setStatus(`${entries.length} satır işlendi.`);
}

refs.generate.addEventListener('click', buildCurrent);
refs.sample.addEventListener('click', () => {
  refs.bulkInput.value = SAMPLE;
  buildCurrent();
});
refs.clear.addEventListener('click', () => {
  refs.bulkInput.value = '';
  setStatus('Temizlendi');
});
refs.mode.addEventListener('change', buildCurrent);
refs.gridSize.addEventListener('change', buildCurrent);
refs.seed.addEventListener('change', buildCurrent);

refs.resetProgress.addEventListener('click', () => {
  resetProgress();
  refs.bulkInput.value = SAMPLE;
  refs.interactive.innerHTML = '';
  refs.legend.innerHTML = '';
  setStatus('İlerleme temizlendi');
});

refs.printMode.addEventListener('click', () => {
  printNow();
});
refs.printAll.addEventListener('click', () => {
  printNow();
});

buildCurrent();
