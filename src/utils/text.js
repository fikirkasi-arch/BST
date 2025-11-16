export function normalize(value = '') {
  return value
    .toUpperCase()
    .replace(/[Ç]/g, 'C')
    .replace(/[Ğ]/g, 'G')
    .replace(/[İI]/g, 'I')
    .replace(/[Ö]/g, 'O')
    .replace(/[Ş]/g, 'S')
    .replace(/[Ü]/g, 'U')
    .replace(/[^A-Z0-9]/g, '');
}

export function parseInput(raw) {
  return raw
    .split(/\n+/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line, idx) => {
      const [answerPart, ...clueParts] = line.split('|');
      const answer = normalize(answerPart || '');
      const clue = (clueParts.join('|') || `Soru ${idx + 1}`).trim();
      return { answer, clue };
    })
    .filter((entry) => entry.answer.length > 1);
}

export function formatList(items) {
  return items
    .map((item, idx) => `${idx + 1}. ${item}`)
    .join('\n');
}
