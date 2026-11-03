(() => {
  const gallery = document.querySelector('.studio-demo-gallery');
  if (!gallery) return;
  const buttons = [...document.querySelectorAll('.studio-filters [data-filter]')];
  const tiles = [...gallery.querySelectorAll('[data-demo-url]')];
  const count = document.querySelector('[data-demo-count]');
  const iframe = document.querySelector('[data-preview-iframe]');
  const title = document.querySelector('[data-preview-title]');
  const open = document.querySelector('[data-preview-link]');
  const preview = document.getElementById('demo-preview');
  const frame = document.querySelector('[data-device-frame]');
  const deviceButtons = [...document.querySelectorAll('[data-demo-device]')];
  let current = tiles[0];

  function selectTile(tile, scroll = true) {
    if (!tile) return;
    current = tile;
    const nextUrl = tile.getAttribute('data-demo-url');
    const nextTitle = tile.getAttribute('data-demo-title');
    if (iframe) {
      iframe.src = nextUrl;
      iframe.title = 'Interactive preview: ' + nextTitle;
    }
    if (title) title.textContent = nextTitle;
    if (open) open.href = nextUrl;
    tiles.forEach(card => card.classList.toggle('studio-demo-selected', card === current));
    if (scroll && preview) preview.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  buttons.forEach(button => {
    button.addEventListener('click', () => {
      buttons.forEach(other => other.setAttribute('aria-pressed', String(other === button)));
      let visibleCount = 0;
      tiles.forEach(tile => {
        const matches = button.dataset.filter === 'all' || tile.dataset.category.split(' ').includes(button.dataset.filter);
        tile.hidden = !matches;
        if (matches) visibleCount += 1;
      });
      if (count) count.textContent = `${visibleCount} demonstration${visibleCount === 1 ? '' : 's'}`;
      if (current && current.hidden) selectTile(tiles.find(tile => !tile.hidden), false);
    });
  });

  tiles.forEach(tile => {
    const button = tile.querySelector('[data-preview-demo]');
    if (button) button.addEventListener('click', () => selectTile(tile));
  });

  deviceButtons.forEach(button => {
    button.addEventListener('click', () => {
      deviceButtons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
      if (frame) frame.dataset.deviceFrame = button.dataset.demoDevice;
    });
  });

  selectTile(tiles[0], false);
})();
