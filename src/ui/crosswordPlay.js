export function wireCrossword(container) {
  const inputs = Array.from(container.querySelectorAll('input'));
  if (!inputs.length) return;
  let direction = 'across';

  function focusAt(row, col) {
    const target = inputs.find((input) => Number(input.dataset.row) === row && Number(input.dataset.col) === col);
    if (target) target.focus();
  }

  inputs.forEach((input) => {
    input.addEventListener('keydown', (event) => {
      const row = Number(event.currentTarget.dataset.row);
      const col = Number(event.currentTarget.dataset.col);
      if (event.key === 'ArrowRight' || (event.key === 'Tab' && !event.shiftKey)) {
        event.preventDefault();
        focusAt(row, col + 1);
      } else if (event.key === 'ArrowLeft' || (event.key === 'Tab' && event.shiftKey)) {
        event.preventDefault();
        focusAt(row, col - 1);
      } else if (event.key === 'ArrowUp') {
        event.preventDefault();
        focusAt(row - 1, col);
      } else if (event.key === 'ArrowDown') {
        event.preventDefault();
        focusAt(row + 1, col);
      } else if (event.key === ' ') {
        event.preventDefault();
        direction = direction === 'across' ? 'down' : 'across';
      } else if (event.key === 'Backspace' && !event.currentTarget.value) {
        event.preventDefault();
        if (direction === 'across') focusAt(row, col - 1);
        else focusAt(row - 1, col);
      }
    });
    input.addEventListener('input', (event) => {
      event.currentTarget.value = event.currentTarget.value.toUpperCase().slice(0, 1);
      const row = Number(event.currentTarget.dataset.row);
      const col = Number(event.currentTarget.dataset.col);
      if (direction === 'across') focusAt(row, col + 1);
      else focusAt(row + 1, col);
    });
  });
}
