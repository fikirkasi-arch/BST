export function createRng(seed = 0) {
  let value = seed || 1;
  return function random() {
    value = (value * 1664525 + 1013904223) % 4294967296;
    return value / 4294967296;
  };
}
