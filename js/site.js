(() => {
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];

  // Mobile navigation
  const menu = $('[data-nav]');
  const toggle = $('[data-nav-toggle]');
  if (menu && toggle) {
    const closeMenu = () => {
      menu.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    };

    toggle.addEventListener('click', () => {
      const isOpen = menu.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(isOpen));
    });

    $$('a', menu).forEach(link => link.addEventListener('click', closeMenu));
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape') closeMenu();
    });
  }

  // Services dropdown
  const drop = $('[data-service-menu]');
  const dropBtn = $('[data-service-toggle]');
  if (drop && dropBtn) {
    dropBtn.addEventListener('click', () => {
      const isOpen = drop.classList.toggle('open');
      dropBtn.setAttribute('aria-expanded', String(isOpen));
    });

    document.addEventListener('click', event => {
      if (!drop.contains(event.target)) {
        drop.classList.remove('open');
        dropBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // FAQ accordions
  $$('.faq-item button').forEach(button => {
    button.addEventListener('click', () => {
      const panel = document.getElementById(button.getAttribute('aria-controls'));
      const expanded = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!expanded));
      if (panel) panel.hidden = expanded;
    });
  });

  // Selected work filters
  const filters = $$('[data-filter]');
  if (filters.length) {
    filters.forEach(button => {
      button.addEventListener('click', () => {
        filters.forEach(item => item.setAttribute('aria-pressed', 'false'));
        button.setAttribute('aria-pressed', 'true');
        $$('[data-category]').forEach(card => {
          const categories = (card.dataset.category || '').split(' ');
          card.hidden = button.dataset.filter !== 'all' && !categories.includes(button.dataset.filter);
        });
      });
    });
  }

  // Landing page preview frame
  const frame = $('[data-preview-frame]');
  const picker = $('[data-demo-picker]');
  if (frame) {
    $$('[data-device]').forEach(button => {
      button.addEventListener('click', () => {
        $$('[data-device]').forEach(item => item.setAttribute('aria-pressed', 'false'));
        button.setAttribute('aria-pressed', 'true');
        frame.dataset.device = button.dataset.device;
      });
    });

    if (picker) {
      picker.addEventListener('change', () => {
        const selected = picker.selectedOptions[0];
        const iframe = $('iframe', frame);
        const openLink = $('[data-demo-open]');
        if (iframe) {
          iframe.src = selected.value;
          iframe.title = 'Live responsive preview: ' + selected.textContent;
        }
        if (openLink) openLink.href = selected.value;
      });
    }
  }

  const issueItems = [
    { title: 'Checkout total not refreshing', status: 'open', area: 'checkout' },
    { title: 'Billing table misreports totals', status: 'resolved', area: 'billing' },
    { title: 'Checkout filter count is stale', status: 'open', area: 'checkout' },
    { title: 'Mobile navigation scroll lock regression', status: 'resolved', area: 'navigation' }
  ];

  const panelContent = {
    overview: {
      title: 'Overview',
      body: 'Owner profile, company details and the current support plan are visible here.',
      points: ['Owner profile is complete', '2 collaborators are active', 'Support plan renews monthly']
    },
    billing: {
      title: 'Billing',
      body: 'Invoices, payment method and renewal timing are grouped in one reliable billing view.',
      points: ['Latest invoice was paid successfully', 'Primary card expires in 04/28', 'Auto-renew is currently enabled']
    },
    access: {
      title: 'Access',
      body: 'Team permissions and login activity are shown in a dedicated access panel.',
      points: ['Admin access is limited to 1 owner', 'Two-factor authentication is enabled', 'Last security review completed this week']
    }
  };

  function isBefore(card) {
    const scene = $('[data-repair-scene]', card);
    return scene ? scene.classList.contains('is-before') : false;
  }

  function updateRepairStatus(card) {
    const status = $('[data-repair-status]', card);
    if (!status) return;
    status.textContent = isBefore(card)
      ? 'Before: the deliberately flawed demonstration is active.'
      : 'After: the corrected demonstration is active.';
  }

  function renderPricingCard(card) {
    const qtyEl = $('[data-qty]', card);
    const seatLine = $('[data-seat-line]', card);
    const totalEl = $('[data-total]', card);
    const noteEl = $('[data-demo-note]', card);
    const qty = Number(card.dataset.qty || 2);
    const baseTotal = 60;
    const afterTotal = qty * 24 + 12;

    if (qtyEl) qtyEl.textContent = String(qty);
    if (seatLine) seatLine.textContent = `${qty} × $24`;

    if (isBefore(card)) {
      if (totalEl) totalEl.textContent = '$' + baseTotal;
      if (noteEl) noteEl.textContent = 'Before: the quantity changes, but the total remains stale.';
    } else {
      if (totalEl) totalEl.textContent = '$' + afterTotal;
      if (noteEl) noteEl.textContent = 'After: quantity, line items and monthly total stay in sync.';
    }
  }

  function renderFilterCard(card) {
    const query = ((card.dataset.searchQuery || '') + '').trim().toLowerCase();
    const status = card.dataset.ticketFilter || 'all';
    const list = $('[data-ticket-list]', card);
    const count = $('[data-ticket-count]', card);
    const note = $('[data-filter-note]', card);

    if (!list) return;

    let visibleItems = issueItems.filter(item => status === 'all' || item.status === status);
    if (!isBefore(card)) {
      visibleItems = visibleItems.filter(item => item.title.toLowerCase().includes(query));
    }

    list.innerHTML = visibleItems.map(item => `
      <div class="ticket-row">
        <div>
          <strong>${item.title}</strong>
          <small>${item.area.charAt(0).toUpperCase() + item.area.slice(1)} flow</small>
        </div>
        <span class="status-chip ${item.status}">${item.status === 'open' ? 'Open' : 'Resolved'}</span>
      </div>
    `).join('');

    if (count) {
      count.textContent = `${visibleItems.length} issue${visibleItems.length === 1 ? '' : 's'}`;
    }
    if (note) {
      note.textContent = isBefore(card)
        ? 'Before: the search input looks active, but the list does not react correctly.'
        : 'After: search text, status pills and result counts stay aligned.';
    }

    $$('[data-ticket-filter]', card).forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.ticketFilter === status));
    });
  }

  function renderTabsCard(card) {
    const activeKey = card.dataset.panelKey || 'overview';
    const title = $('[data-panel-title]', card);
    const body = $('[data-panel-body]', card);
    const list = $('[data-panel-list]', card);
    const note = $('[data-tab-note]', card);
    const active = panelContent[activeKey] || panelContent.overview;

    $$('[data-panel-tab]', card).forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.panelTab === activeKey));
    });

    if (isBefore(card)) {
      if (title) title.textContent = panelContent.overview.title;
      if (body) body.textContent = panelContent.overview.body;
      if (list) list.innerHTML = panelContent.overview.points.map(item => `<li>${item}</li>`).join('');
      if (note) note.textContent = 'Before: the active pill changes, but the content panel stays stuck on the first tab.';
    } else {
      if (title) title.textContent = active.title;
      if (body) body.textContent = active.body;
      if (list) list.innerHTML = active.points.map(item => `<li>${item}</li>`).join('');
      if (note) note.textContent = 'After: the selected tab, panel content and visible state stay synchronised.';
    }
  }

  function renderFormCard(card, errors = [], success = false) {
    const errorsBox = $('[data-form-errors]', card);
    const status = $('[data-form-status]', card);

    if (!errorsBox || !status) return;

    if (isBefore(card)) {
      errorsBox.innerHTML = '';
      status.textContent = 'Before: submit returns a generic failure with no field-level help.';
      return;
    }

    if (success) {
      errorsBox.innerHTML = '<span class="success">Validation passed. This is a demo: no message was sent.</span>';
      status.textContent = 'After: the demo confirms valid fields without sending data.';
      return;
    }

    if (errors.length) {
      errorsBox.innerHTML = errors.map(error => `<span>${error}</span>`).join('');
      status.textContent = 'After: invalid fields are explained clearly before submission.';
    } else {
      errorsBox.innerHTML = '';
      status.textContent = 'After: validation is ready. Try submitting with a name, email and summary.';
    }
  }

  function renderRepairCard(card) {
    switch (card.dataset.demo) {
      case 'pricing':
        renderPricingCard(card);
        break;
      case 'filter':
        renderFilterCard(card);
        break;
      case 'form':
        renderFormCard(card);
        break;
      case 'tabs':
        renderTabsCard(card);
        break;
      default:
        break;
    }
    updateRepairStatus(card);
  }

  const repairCards = $$('[data-repair-card]');
  repairCards.forEach(card => {
    if (!card.dataset.qty) card.dataset.qty = '2';
    if (!card.dataset.ticketFilter) card.dataset.ticketFilter = 'all';
    if (!card.dataset.searchQuery) card.dataset.searchQuery = 'checkout';
    if (!card.dataset.panelKey) card.dataset.panelKey = 'overview';

    $$('[data-repair]', card).forEach(button => {
      button.addEventListener('click', () => {
        const scene = $('[data-repair-scene]', card);
        const before = button.dataset.repair === 'before';
        $$('[data-repair]', card).forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        if (scene) scene.classList.toggle('is-before', before);
        renderRepairCard(card);
      });
    });

    $$('[data-qty-action]', card).forEach(button => {
      button.addEventListener('click', () => {
        const current = Number(card.dataset.qty || 2);
        const next = button.dataset.qtyAction === 'plus' ? current + 1 : Math.max(1, current - 1);
        card.dataset.qty = String(next);
        renderPricingCard(card);
      });
    });

    const searchInput = $('[data-ticket-search]', card);
    if (searchInput) {
      searchInput.addEventListener('input', () => {
        card.dataset.searchQuery = searchInput.value;
        renderFilterCard(card);
      });
    }

    $$('[data-ticket-filter]', card).forEach(button => {
      button.addEventListener('click', () => {
        card.dataset.ticketFilter = button.dataset.ticketFilter;
        renderFilterCard(card);
      });
    });

    const form = $('[data-repair-form]', card);
    if (form) {
      const syncFormState = () => renderFormCard(card, [], false);
      $$('input, textarea', form).forEach(field => field.addEventListener('input', syncFormState));

      form.addEventListener('submit', event => {
        event.preventDefault();

        if (isBefore(card)) {
          const status = $('[data-form-status]', card);
          if (status) status.textContent = 'Before: the form fails with a vague message and does not explain what to fix.';
          return;
        }

        const name = form.elements.namedItem('name')?.value.trim() || '';
        const email = form.elements.namedItem('email')?.value.trim() || '';
        const summary = form.elements.namedItem('summary')?.value.trim() || '';
        const errors = [];

        if (name.length < 2) errors.push('Please enter a valid contact name.');
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.push('Please enter a valid email address.');
        if (summary.length < 12) errors.push('Please provide a short description of the issue.');

        if (errors.length) {
          renderFormCard(card, errors, false);
        } else {
          renderFormCard(card, [], true);
        }
      });
    }

    $$('[data-panel-tab]', card).forEach(button => {
      button.addEventListener('click', () => {
        card.dataset.panelKey = button.dataset.panelTab;
        renderTabsCard(card);
      });
    });

    renderRepairCard(card);
  });
})();
