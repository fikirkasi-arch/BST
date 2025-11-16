import { parseInput } from './utils/text.js';

const STORAGE_KEY = 'bst-progress';

export const state = {
  entries: [],
  mode: 'crossword',
  gridSize: 'auto',
  seed: 0,
  result: null,
};

export function loadProgress() {
  try {
    const payload = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (payload) {
      Object.assign(state, payload);
    }
  } catch (error) {
    console.warn('Progress load failed', error);
  }
}

export function persistProgress() {
  const payload = {
    entries: state.entries,
    mode: state.mode,
    gridSize: state.gridSize,
    seed: state.seed,
  };
  localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
}

export function resetProgress() {
  localStorage.removeItem(STORAGE_KEY);
  state.entries = [];
  state.result = null;
}

export function updateEntries(rawText) {
  state.entries = parseInput(rawText);
  return state.entries;
}
