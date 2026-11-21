(() => {
  'use strict';

  const products = Array.isArray(window.KAZISAFI_PRODUCTS) ? window.KAZISAFI_PRODUCTS : [];
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const escapeHTML = value => String(value ?? '').replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const slug = value => String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const firstImageByCategory = {};
  products.forEach(product => {
    if (product.image && !firstImageByCategory[product.category]) firstImageByCategory[product.category] = product.image;
  });
  const imageFor = product => product.image || firstImageByCategory[product.category] || '';
  const categories = ['All', ...new Set(products.map(product => product.category))];
  const queryParams = new URLSearchParams(window.location.search);
  const requestedCategory = queryParams.get('category');
  const initialCategory = categories.includes(requestedCategory) ? requestedCategory : 'All';
  const initialSearch = queryParams.get('q') || '';
  const state = { category: initialCategory, search: initialSearch.trim(), sort: 'featured', activeProduct: null, quote: loadQuote() };

  function loadQuote() {
    try {
      const value = JSON.parse(localStorage.getItem('kazisafiiQuoteV1') || '[]');
      return Array.isArray(value) ? value.filter(item => item && typeof item.id === 'string' && Number.isFinite(Number(item.quantity))) : [];
    } catch (_) { return []; }
  }

  function saveQuote() {
    try { localStorage.setItem('kazisafiiQuoteV1', JSON.stringify(state.quote)); }
    catch (_) { showToast('Your browser could not save the list. It will remain available during this visit.'); }
    renderQuote();
  }

  function productImageMarkup(product, className = '') {
    const src = imageFor(product);
    if (src) {
      return `<img class="${className}" src="/${escapeHTML(src)}" alt="${escapeHTML(product.name)}" loading="lazy" decoding="async" onerror="this.hidden=true;this.nextElementSibling.hidden=false"><div class="image-fallback" hidden>${placeholderMarkup(product)}</div>`;
    }
    return placeholderMarkup(product);
  }

  function placeholderMarkup(product) {
    const initials = product.name.split(/\s+/).slice(0, 2).map(word => word[0]).join('').toUpperCase();
    return `<div class="image-placeholder" aria-label="${escapeHTML(product.name)}"><span>${escapeHTML(initials)}</span><small>${escapeHTML(product.category)}</small></div>`;
  }

  function renderCategories() {
    const target = $('#categoryTabs');
    target.innerHTML = categories.map(category => `<button class="category-tab${state.category === category ? ' active' : ''}" data-category="${escapeHTML(category)}" type="button" aria-pressed="${state.category === category}">${category === 'All' ? 'All products' : escapeHTML(category)}</button>`).join('');
  }

  function filteredProducts() {
    let items = products.filter(product => {
      const categoryMatch = state.category === 'All' || product.category === state.category;
      const searchable = `${product.name} ${product.category}`.toLowerCase();
      const searchMatch = !state.search || searchable.includes(state.search.toLowerCase());
      return categoryMatch && searchMatch;
    });
    if (state.sort === 'name') items.sort((a, b) => a.name.localeCompare(b.name));
    else items.sort((a, b) => Number(b.popular) - Number(a.popular) || Number(b.new) - Number(a.new) || a.name.localeCompare(b.name));
    return items;
  }

  function renderProducts() {
    const items = filteredProducts();
    const grid = $('#productGrid');
    $('#resultCount').textContent = `Showing ${items.length} of ${products.length} products`;
    $('#clearFilters').hidden = state.category === 'All' && !state.search;
    $('#emptyState').hidden = items.length > 0;
    grid.hidden = items.length === 0;
    grid.innerHTML = items.map(product => {
      const label = product.popular ? 'Popular' : product.new ? 'New' : '';
      return `<article class="product-card" data-id="${escapeHTML(product.id)}">
        <button class="product-image" type="button" data-details="${escapeHTML(product.id)}" aria-label="View ${escapeHTML(product.name)} details">
          ${productImageMarkup(product)}
          ${label ? `<span class="product-label">${label}</span>` : ''}
        </button>
        <div class="product-content">
          <p class="product-category">${escapeHTML(product.category)}</p>
          <h3 class="product-name">${escapeHTML(product.name)}</h3>
          <div class="product-bottom"><div><div class="product-price"><small>Pricing</small>Request a quote</div><div class="product-min">Quantity confirmed with your quote</div></div><button class="product-add" type="button" data-add="${escapeHTML(product.id)}" aria-label="Add ${escapeHTML(product.name)} to quote list">+</button></div>
        </div>
      </article>`;
    }).join('');
  }

  function renderAll() { renderCategories(); renderProducts(); }

  function addToQuote(product, quantity) {
    const min = 1;
    const qty = Math.max(min, Math.floor(Number(quantity) || min));
    const existing = state.quote.find(item => item.id === product.id);
    if (existing) existing.quantity += qty;
    else state.quote.push({id: product.id, quantity: qty});
    saveQuote();
    showToast(`${product.name} added to your quote list`);
  }

  function productFromId(id) { return products.find(product => product.id === id); }

  function renderQuote() {
    const count = state.quote.reduce((sum, item) => sum + Number(item.quantity || 0), 0);
    $('#quoteCount').textContent = String(count);
    $('#drawerCount').textContent = `(${count})`;
    $('#sendQuote').disabled = state.quote.length === 0;
    $('#clearQuote').hidden = state.quote.length === 0;
    const target = $('#quoteItems');
    if (!state.quote.length) {
      target.innerHTML = `<div class="drawer-empty"><span>＋</span><h3>Your list is empty</h3><p>Add products from the catalogue and they’ll appear here.</p></div>`;
      return;
    }
    target.innerHTML = state.quote.map(item => {
      const product = productFromId(item.id);
      if (!product) return '';
      return `<div class="quote-item" data-quote-id="${escapeHTML(item.id)}">${productImageMarkup(product)}<div><strong>${escapeHTML(product.name)}</strong><small>Final pricing confirmed by our team</small><div class="quote-qty"><button type="button" data-qty="-1" aria-label="Decrease quantity">−</button><span>${Number(item.quantity)}</span><button type="button" data-qty="1" aria-label="Increase quantity">+</button></div></div><button class="quote-remove" data-remove="${escapeHTML(item.id)}" type="button" aria-label="Remove ${escapeHTML(product.name)}">×</button></div>`;
    }).join('');
  }

  function showToast(message) {
    const toast = $('#toast');
    toast.textContent = message;
    toast.classList.add('show');
    window.clearTimeout(showToast.timer);
    showToast.timer = window.setTimeout(() => toast.classList.remove('show'), 2300);
  }

  function openDrawer() {
    $('#quoteBackdrop').hidden = false;
    $('#quoteDrawer').classList.add('open');
    $('#quoteDrawer').setAttribute('aria-hidden', 'false');
    document.body.classList.add('locked');
    $('#closeQuote').focus();
  }

  function closeDrawer() {
    $('#quoteDrawer').classList.remove('open');
    $('#quoteDrawer').setAttribute('aria-hidden', 'true');
    $('#quoteBackdrop').hidden = true;
    document.body.classList.remove('locked');
    $('#openQuote').focus();
  }

  function openProduct(id) {
    const product = productFromId(id);
    if (!product) return;
    state.activeProduct = product;
    $('#dialogCategory').textContent = product.category.toUpperCase();
    $('#dialogProductName').textContent = product.name;
    $('#dialogPrice').textContent = 'Request a tailored quote';
    const min = 1;
    $('#dialogMinimum').textContent = 'Minimum order quantity confirmed with your quote';
    $('#dialogQuantity').min = String(min);
    $('#dialogQuantity').value = String(min);
    $('#dialogImage').innerHTML = productImageMarkup(product);
    const dialog = $('#productDialog');
    if (typeof dialog.showModal === 'function') dialog.showModal();
    else dialog.setAttribute('open', '');
  }

  function closeProduct() {
    const dialog = $('#productDialog');
    if (typeof dialog.close === 'function') dialog.close();
    else dialog.removeAttribute('open');
    state.activeProduct = null;
  }

  function buildWhatsAppMessage() {
    const lines = ['Hello Kazisafii, I would like a quote for these items:', ''];
    state.quote.forEach(item => {
      const product = productFromId(item.id);
      if (product) lines.push(`• ${product.name} (${product.category}) — Quantity: ${item.quantity}`);
    });
    lines.push('', 'Please confirm available options, minimum order quantities, final pricing, production timeline and delivery/collection details.', '', 'Name:', 'Location:');
    return `https://wa.me/254743288927?text=${encodeURIComponent(lines.join('\n'))}`;
  }

  function sendQuote() {
    if (!state.quote.length) return;
    const url = buildWhatsAppMessage();
    window.open(url, '_blank', 'noopener,noreferrer');
  }

  $('#categoryTabs').addEventListener('click', event => {
    const button = event.target.closest('[data-category]');
    if (!button) return;
    state.category = button.dataset.category;
    renderAll();
  });

  $('#productGrid').addEventListener('click', event => {
    const details = event.target.closest('[data-details]');
    const add = event.target.closest('[data-add]');
    if (details) openProduct(details.dataset.details);
    if (add) {
      const product = productFromId(add.dataset.add);
      if (product) addToQuote(product, 1);
    }
  });

  function updateSearch(value) {
    state.search = value.trim();
    $('#catalogueSearch').value = value;
    $('#globalSearch').value = value;
    renderProducts();
    $('#catalogue').scrollIntoView({behavior:'smooth', block:'start'});
  }
  $('#catalogueSearch').addEventListener('input', event => { state.search = event.target.value.trim(); $('#globalSearch').value = event.target.value; renderProducts(); });
  $('#globalSearch').addEventListener('input', event => { state.search = event.target.value.trim(); $('#catalogueSearch').value = event.target.value; renderProducts(); });
  $('#headerSearch').addEventListener('submit', event => { event.preventDefault(); $('#catalogue').scrollIntoView({behavior:'smooth'}); $('#catalogueSearch').focus(); });
  $('#sortProducts').addEventListener('change', event => { state.sort = event.target.value; renderProducts(); });
  $('#clearFilters').addEventListener('click', () => { state.category = 'All'; state.search = ''; state.sort = 'featured'; $('#catalogueSearch').value = ''; $('#globalSearch').value = ''; $('#sortProducts').value = 'featured'; renderAll(); });
  $('#resetSearch').addEventListener('click', () => $('#clearFilters').click());
  $('#openQuote').addEventListener('click', openDrawer);
  $('#mobileQuote').addEventListener('click', () => { $('#mobileNav').hidden = true; $('#mobileMenu').setAttribute('aria-expanded','false'); openDrawer(); });
  $('#closeQuote').addEventListener('click', closeDrawer);
  $('#quoteBackdrop').addEventListener('click', closeDrawer);
  $('#sendQuote').addEventListener('click', sendQuote);
  $('#clearQuote').addEventListener('click', () => { state.quote = []; saveQuote(); showToast('Quote list cleared'); });
  $('#quoteItems').addEventListener('click', event => {
    const remove = event.target.closest('[data-remove]');
    const qty = event.target.closest('[data-qty]');
    const row = event.target.closest('[data-quote-id]');
    if (remove) {
      state.quote = state.quote.filter(item => item.id !== remove.dataset.remove);
      saveQuote();
    } else if (qty && row) {
      const item = state.quote.find(entry => entry.id === row.dataset.quoteId);
      const product = item && productFromId(item.id);
      if (item && product) {
        item.quantity = Math.max(1, Number(item.quantity) + Number(qty.dataset.qty));
        saveQuote();
      }
    }
  });
  $('#closeProduct').addEventListener('click', closeProduct);
  $('#productDialog').addEventListener('click', event => { if (event.target === $('#productDialog')) closeProduct(); });
  $('#addToQuote').addEventListener('click', () => {
    if (!state.activeProduct) return;
    const quantity = Math.floor(Number($('#dialogQuantity').value));
    const min = 1;
    if (!Number.isFinite(quantity) || quantity < min) { $('#dialogQuantity').setCustomValidity('Quantity must be at least 1.'); $('#dialogQuantity').reportValidity(); $('#dialogQuantity').setCustomValidity(''); return; }
    addToQuote(state.activeProduct, quantity);
    closeProduct();
  });
  $('#mobileMenu').addEventListener('click', () => {
    const nav = $('#mobileNav');
    nav.hidden = !nav.hidden;
    $('#mobileMenu').setAttribute('aria-expanded', String(!nav.hidden));
  });
  $$('#mobileNav a').forEach(link => link.addEventListener('click', () => { $('#mobileNav').hidden = true; $('#mobileMenu').setAttribute('aria-expanded','false'); }));
  document.addEventListener('keydown', event => {
    if (event.key === '/' && !['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)) { event.preventDefault(); $('#globalSearch').focus(); }
    if (event.key === 'Escape' && $('#quoteDrawer').classList.contains('open')) closeDrawer();
  });

  $('#year').textContent = new Date().getFullYear();
  $('#catalogueSearch').value = initialSearch;
  $('#globalSearch').value = initialSearch;
  renderAll();
  renderQuote();
})();