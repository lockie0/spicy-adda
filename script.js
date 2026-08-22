const menuItems = [
  { name: 'Challapunukulu', quantity: '10 PCS', price: 30, category: 'Special' },
  { name: 'Mirchi Bajji', quantity: '4 PCS · WITHOUT CHAT', price: 30, category: 'Bajji' },
  { name: 'Mirchi Bajji', quantity: '4 PCS · WITH CHAT', price: 40, category: 'Bajji' },
  { name: 'Onion Bonda', quantity: '4 PCS', price: 30, category: 'Bonda' },
  { name: 'Banana Bajji', quantity: '4 PCS · WITHOUT CHAT', price: 30, category: 'Bajji' },
  { name: 'Banana Bajji', quantity: '4 PCS · WITH CHAT', price: 40, category: 'Bajji' },
  { name: 'Onion Pakodi', quantity: '', price: 30, category: 'Pakodi' },
  { name: 'Maramaralu Mirchire', quantity: '', price: 35, category: 'Special' },
  { name: 'Tomato Mirchire', quantity: '', price: 35, category: 'Special' },
  { name: 'Maramaralu With Kaju Mirchire', quantity: '', price: 50, category: 'Special' },
  { name: 'Bottani Chat', quantity: '', price: 30, category: 'Chat' },
  { name: 'Chanagapindi Pakodi', quantity: '', price: 30, category: 'Pakodi' },
  { name: 'Egg Bajji', quantity: '', price: 30, category: 'Special' },
  { name: 'Bread Bajji', quantity: '', price: 30, category: 'Special' },
  { name: 'Samosa Big', quantity: '1 PC', price: 15, category: 'Special' },
];

const combos = [
  { name: 'SPICY STARTER', items: ['Mirchi Bajji (Without Chat)', 'Onion Bonda'], originalPrice: 60, price: 49, savings: 11 },
  { name: 'CHAT SPECIAL', items: ['Mirchi Bajji (With Chat)', 'Bottani Chat'], originalPrice: 70, price: 59, savings: 11 },
  { name: 'BONDA BLAST', items: ['Onion Bonda', 'Challapunukulu', 'Samosa Big'], originalPrice: 75, price: 59, savings: 16 },
  { name: 'BAJJI LOVERS', items: ['Banana Bajji (With Chat)', 'Mirchi Bajji (Without Chat)', 'Samosa Big'], originalPrice: 85, price: 69, savings: 16 },
  { name: 'FRIENDS COMBO', items: ['Mirchi Bajji (Without Chat)', 'Onion Pakodi', 'Bottani Chat'], originalPrice: 90, price: 69, savings: 21 },
  { name: 'FAMILY SAVER', items: ['Onion Bonda', 'Mirchi Bajji (Without Chat)', 'Challapunukulu'], originalPrice: 120, price: 89, savings: 31 },
  { name: 'SPICY ADDA MEGA COMBO', items: ['Mirchi Bajji (With Chat)', 'Banana Bajji (With Chat)', 'Onion Bonda', 'Onion Pakodi', 'Samosa Big'], originalPrice: 155, price: 119, savings: 36 },
];

const offers = [
  { icon: '✦', label: 'GRAND OPENING', title: 'FIRST 7 DAYS', content: 'BUY 2 MIRCHI BAJJI<br>GET 1 FREE', featured: true },
  { icon: '⌁', label: 'STUDENTS OFFER', title: '10% OFF', content: 'Show Student ID · Orders above ₹200' },
  { icon: '◷', label: 'HAPPY HOURS', title: 'ANY 2 FOR ₹50', content: 'Monday–Thursday · 4 PM–6 PM' },
  { icon: '⌂', label: 'FAMILY OFFER', title: '₹30 OFF', content: 'Spend ₹300 on your adda' },
  { icon: '★', label: 'LOYALTY OFFER', title: '10TH SNACK FREE', content: 'Buy 9 times, your next one is on us' },
];

const paymentMethods = [
  { value: 'UPI', description: 'Pay securely using any UPI app' },
  { value: 'PhonePe', description: 'Pay using PhonePe' },
  { value: 'Net Banking', description: 'Choose your bank' },
];

const cartStorageKey = 'spicyAddaCart';
let cart = loadCart();
let activeFilter = '';

const money = (value) => `₹${value}`;

function loadCart() {
  try {
    const savedCart = JSON.parse(localStorage.getItem(cartStorageKey) || '[]');
    return Array.isArray(savedCart) ? savedCart : [];
  } catch {
    return [];
  }
}

function saveCart() {
  localStorage.setItem(cartStorageKey, JSON.stringify(cart));
}

function getCartQuantity(name) {
  return cart.find((item) => item.name === name)?.qty || 0;
}

function calculateSubtotal() {
  return cart.reduce((total, item) => total + item.price * item.qty, 0);
}

function calculateDiscount(subtotal = calculateSubtotal()) {
  return subtotal >= 200 ? Math.round(subtotal * 0.1) : 0;
}

function calculateTotal() {
  const subtotal = calculateSubtotal();
  return subtotal - calculateDiscount(subtotal);
}

function renderProducts() {
  const query = document.querySelector('#search-input').value.toLowerCase();
  const filteredProducts = menuItems
    .map((product, index) => ({ product, index }))
    .filter(({ product }) => {
      const matchesSearch = !query || product.name.toLowerCase().includes(query) || product.quantity.toLowerCase().includes(query);
      return matchesSearch && (!activeFilter || product.category === activeFilter);
    });

  document.querySelector('.result-count').textContent = `${filteredProducts.length} snacks`;
  document.querySelector('.no-results').hidden = filteredProducts.length > 0;
  document.querySelector('#product-grid').innerHTML = filteredProducts.map(({ product, index }) => `
    <article class="product-card">
      <div class="product-image-wrap">
        <img src="${imageFor(`${product.name} ${product.quantity}`)}" alt="${product.name}" loading="lazy">
        <button class="quick-add" data-add="${index}" aria-label="Add ${product.name}">+</button>
      </div>
      <div class="product-info">
        <p class="product-category">${product.category}</p>
        <h3>${product.name}</h3>
        <span>${product.quantity || 'Freshly prepared'}</span>
        <div class="product-bottom">
          <strong>${money(product.price)}</strong>
          <div class="inline-qty">
            <button data-product-qty="${index}" data-change="-1">&minus;</button>
            <span>${getCartQuantity(product.name)}</span>
            <button data-product-qty="${index}" data-change="1">+</button>
          </div>
        </div>
        <button class="add-button" data-add="${index}">Add to cart <span>&rarr;</span></button>
      </div>
    </article>`).join('');
}

function renderCombos() {
  document.querySelector('#combo-grid').innerHTML = combos.map((combo, index) => `
    <article class="combo-card">
      <div class="combo-top">
        <span class="combo-number">0${index + 1}</span>
        <div><p class="product-category">COMBO OFFER</p><h3>${combo.name}</h3></div>
        <span class="save">SAVE ${money(combo.savings)}</span>
      </div>
      <div class="combo-images">${combo.items.map((name) => `<img src="${imageFor(name)}" alt="${name}">`).join('')}</div>
      <p class="combo-items">${combo.items.join(' + ')}</p>
      <div class="combo-bottom">
        <span><del>${money(combo.originalPrice)}</del><strong>${money(combo.price)}</strong></span>
        <button class="add-button" data-combo="${index}">Add combo <span>+</span></button>
      </div>
    </article>`).join('');
}

function renderOffers() {
  document.querySelector('.offers-grid').innerHTML = offers.map((offer) => `
    <article class="offer-card${offer.featured ? ' featured' : ''}">
      <span>${offer.icon}</span><p>${offer.label}</p><h3>${offer.title}</h3>
      ${offer.featured ? `<strong>${offer.content}</strong>` : `<small>${offer.content}</small>`}
    </article>`).join('');
}

function renderPaymentMethods() {
  document.querySelector('.payment-options').innerHTML = paymentMethods.map((method) => `
    <label><input type="radio" name="payment" value="${method.value}"> <span><b>${method.value}</b><small>${method.description}</small></span></label>`).join('');
}

function addToCart(name, price, image) {
  const item = cart.find((cartItem) => cartItem.name === name);
  if (item) item.qty += 1;
  else cart.push({ name, price, image, qty: 1 });
  saveCart();
  updateCartView();
}

function updateQuantity(index, change) {
  const item = cart[index];
  if (!item) return;
  item.qty += change;
  if (item.qty < 1) cart.splice(index, 1);
  saveCart();
  updateCartView();
}

function removeFromCart(index) {
  cart.splice(index, 1);
  saveCart();
  updateCartView();
}

function renderCart() {
  document.querySelector('.cart-items').innerHTML = cart.map((item, index) => `
    <div class="cart-row">
      <img src="${item.image || imageFor(item.name)}" alt="${item.name}">
      <div><h4>${item.name}</h4><p>${money(item.price)}</p><button data-remove="${index}">Remove</button></div>
      <div class="qty"><button data-cart-qty="${index}" data-change="-1">&minus;</button><span>${item.qty}</span><button data-cart-qty="${index}" data-change="1">+</button></div>
    </div>`).join('');
}

function renderOrderSummary(total) {
  document.querySelector('.checkout-items').innerHTML = cart.map((item) => `
    <p><span>${item.name} &times; ${item.qty}</span><b>${money(item.price * item.qty)}</b></p>`).join('');
  document.querySelectorAll('.modal-total').forEach((element) => { element.textContent = money(total); });
}

function updateCartView() {
  const subtotal = calculateSubtotal();
  const discount = calculateDiscount(subtotal);
  const total = calculateTotal();
  renderCart();
  document.querySelectorAll('.cart-count').forEach((element) => { element.textContent = cart.reduce((count, item) => count + item.qty, 0); });
  document.querySelector('.subtotal').textContent = money(subtotal);
  document.querySelector('.discount').textContent = `- ${money(discount)}`;
  document.querySelector('.total-price').textContent = money(total);
  renderOrderSummary(total);
  document.querySelector('.cart-empty').hidden = cart.length > 0;
  renderProducts();
}

function openCart() { document.querySelector('.cart-drawer').classList.add('open'); document.querySelector('.overlay').classList.add('open'); }
function closeCart() { document.querySelector('.cart-drawer').classList.remove('open'); document.querySelector('.overlay').classList.remove('open'); }

function handleProductQuantity(button) {
  const product = menuItems[button.dataset.productQty];
  const change = Number(button.dataset.change);
  if (change > 0) addToCart(product.name, product.price, imageFor(`${product.name} ${product.quantity}`));
  else {
    const itemIndex = cart.findIndex((item) => item.name === product.name);
    if (itemIndex !== -1) updateQuantity(itemIndex, change);
  }
}

function handleClick(event) {
  const addButton = event.target.closest('[data-add]');
  const comboButton = event.target.closest('[data-combo]');
  const cartQuantityButton = event.target.closest('[data-cart-qty]');
  const productQuantityButton = event.target.closest('[data-product-qty]');
  const removeButton = event.target.closest('[data-remove]');

  if (addButton) {
    const product = menuItems[addButton.dataset.add];
    addToCart(product.name, product.price, imageFor(`${product.name} ${product.quantity}`));
  } else if (comboButton) {
    const combo = combos[comboButton.dataset.combo];
    addToCart(combo.name, combo.price, '');
  } else if (productQuantityButton) handleProductQuantity(productQuantityButton);
  else if (cartQuantityButton) updateQuantity(Number(cartQuantityButton.dataset.cartQty), Number(cartQuantityButton.dataset.change));
  else if (removeButton) removeFromCart(Number(removeButton.dataset.remove));

  if (event.target.closest('[data-open-cart]')) openCart();
  if (event.target.closest('[data-close-cart]') || event.target.classList.contains('overlay')) closeCart();
  if (event.target.closest('.checkout-button') && cart.length) { closeCart(); document.querySelector('.checkout-modal').showModal(); }
  if (event.target.closest('.modal-close')) document.querySelector('.checkout-modal').close();
  if (event.target.closest('[data-clear-filter]')) { activeFilter = ''; document.querySelector('[data-clear-filter]').hidden = true; renderProducts(); }
  if (event.target.closest('[data-category]')) {
    const category = event.target.closest('[data-category]').dataset.category;
    if (category === 'combo') document.querySelector('#combos').scrollIntoView();
    else { activeFilter = category; document.querySelector('[data-clear-filter]').hidden = false; document.querySelector('#menu').scrollIntoView(); renderProducts(); }
  }
}

function showPaymentStep(event) {
  event.preventDefault();
  if (!event.currentTarget.checkValidity()) { document.querySelector('.form-error').hidden = false; event.currentTarget.reportValidity(); return; }
  document.querySelector('.form-error').hidden = true;
  document.querySelector('.pay-amount').textContent = money(calculateTotal());
  document.querySelector('[data-step="details"]').hidden = true;
  document.querySelector('[data-step="payment"]').hidden = false;
}

function processPayment() {
  const selectedPayment = document.querySelector('input[name="payment"]:checked');
  if (!selectedPayment) { document.querySelector('.payment-error').hidden = false; return; }
  document.querySelector('.payment-error').hidden = true;
  document.querySelector('[data-step="payment"]').hidden = true;
  document.querySelector('.processing-step').hidden = false;
  setTimeout(() => showOrderSuccess(selectedPayment.value), 1200);
}

function showOrderSuccess(paymentMethod) {
  document.querySelector('.customer-name').textContent = document.querySelector('[name="name"]').value.trim();
  document.querySelector('.success-total').textContent = money(calculateTotal());
  document.querySelector('.success-method').textContent = paymentMethod;
  document.querySelector('.processing-step').hidden = true;
  document.querySelector('.success-message').hidden = false;
  clearCart();
}

function clearCart() { cart = []; saveCart(); updateCartView(); }

function resetCheckout() {
  const checkoutModal = document.querySelector('.checkout-modal');
  checkoutModal.close();
  document.querySelector('[data-step="details"]').hidden = false;
  document.querySelector('[data-step="payment"]').hidden = true;
  document.querySelector('.processing-step').hidden = true;
  document.querySelector('.success-message').hidden = true;
  document.querySelector('#checkout-form').reset();
  document.querySelector('#checkout-form').hidden = false;
}

function initializeStorefront() {
  document.addEventListener('click', handleClick);
  document.querySelector('.search-toggle').addEventListener('click', () => { document.querySelector('.search-bar').classList.toggle('open'); document.querySelector('#search-input').focus(); });
  document.querySelector('#search-input').addEventListener('input', renderProducts);
  document.querySelector('[data-clear-search]').addEventListener('click', () => { document.querySelector('#search-input').value = ''; renderProducts(); });
  document.querySelector('.menu-toggle').addEventListener('click', (event) => { const nav = document.querySelector('.nav-links'); nav.classList.toggle('open'); event.currentTarget.setAttribute('aria-expanded', nav.classList.contains('open')); });
  document.querySelectorAll('.nav-links a').forEach((link) => link.addEventListener('click', () => document.querySelector('.nav-links').classList.remove('open')));
  document.querySelector('#checkout-form').addEventListener('submit', showPaymentStep);
  document.querySelector('.pay-button').addEventListener('click', processPayment);
  document.querySelector('.continue-shopping').addEventListener('click', resetCheckout);
  document.querySelector('.modal-close').addEventListener('click', () => document.querySelector('.checkout-modal').close());
  renderOffers();
  renderPaymentMethods();
  renderCombos();
  updateCartView();
}

initializeStorefront();
