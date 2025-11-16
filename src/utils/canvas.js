export function gridToDataUrl(grid, numbers, { showLetters = false } = {}) {
  const size = grid.length;
  const cell = Math.max(16, Math.min(40, Math.floor(1000 / size)));
  const padding = 12;
  const width = size * cell + padding * 2;
  const height = size * cell + padding * 2;
  const canvas = document.createElement('canvas');
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext('2d');
  ctx.fillStyle = '#fff';
  ctx.fillRect(0, 0, width, height);
  ctx.strokeStyle = '#000';
  ctx.lineWidth = 1;

  for (let r = 0; r < size; r += 1) {
    for (let c = 0; c < size; c += 1) {
      const x = padding + c * cell;
      const y = padding + r * cell;
      if (!grid[r][c]) {
        ctx.fillStyle = '#000';
        ctx.fillRect(x, y, cell, cell);
        continue;
      }
      ctx.fillStyle = '#fff';
      ctx.fillRect(x, y, cell, cell);
      ctx.strokeRect(x + 0.5, y + 0.5, cell - 1, cell - 1);
      if (numbers[r][c]) {
        ctx.fillStyle = '#444';
        ctx.font = '10px Inter, sans-serif';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'top';
        ctx.fillText(String(numbers[r][c]), x + 2, y + 1);
      }
      if (showLetters) {
        ctx.fillStyle = '#000';
        ctx.font = `${Math.floor(cell * 0.6)}px Inter, sans-serif`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(grid[r][c], x + cell / 2, y + cell / 2);
      }
    }
  }
  return canvas.toDataURL('image/png');
}

export function createPrintImage(src, alt) {
  const img = document.createElement('img');
  img.src = src;
  img.alt = alt;
  img.className = 'sheet';
  return img;
}
