export function renderPrintable(sections = []) {
  const root = document.getElementById('printRoot');
  root.innerHTML = '';
  const list = Array.isArray(sections) ? sections : [];
  list.forEach((section) => {
    const block = document.createElement('article');
    block.innerHTML = `<h2>${section.title}</h2>`;
    if (section.images) {
      section.images.forEach((image) => {
        const img = document.createElement('img');
        img.src = image.src;
        img.alt = image.alt;
        img.style.maxWidth = '18cm';
        img.style.display = 'block';
        img.style.marginBottom = '12px';
        block.appendChild(img);
      });
    }
    if (section.html) {
      block.insertAdjacentHTML('beforeend', section.html);
    }
    root.appendChild(block);
  });
}

export async function printNow() {
  const images = Array.from(document.querySelectorAll('#printRoot img'));
  await Promise.all(
    images.map((img) => (img.decode ? img.decode().catch(() => {}) : Promise.resolve())),
  );
  window.print();
}
