describe('Spicy Adda storefront', () => {
  beforeEach(() => {
    cy.visit('/');
    cy.startWithEmptyCart();
  });

  function productPrice(productIndex) {
    return cy.get('.product-card').eq(productIndex).find('.product-bottom strong').invoke('text').then((text) => Number(text.replace(/[^0-9]/g, '')));
  }

  function completeCheckoutWith(method) {
    cy.fixture('customerData').then(({ validCustomer }) => {
      cy.addProductToCart(0);
      cy.openCart();
      cy.get('.total-price').invoke('text').then((total) => {
        cy.proceedToOrder();
        cy.fillCustomerDetails(validCustomer);
        cy.get('#checkout-form button[type="submit"]').click();
        cy.get('.pay-amount').should('have.text', total);
        cy.completePayment(method);
        cy.verifyOrderSuccess(validCustomer, total, method);
      });
    });
  }

  it('loads the homepage and its main sections', () => {
    cy.title().should('contain', 'Spicy Adda');
    cy.get('.brand').should('be.visible').and('contain.text', 'SPICY ADDA');
    cy.get('.nav > .brand').should('have.css', 'background-image').and('not.equal', 'none');
    cy.get('#menu, #combos, #offers, #about, footer').should('have.length', 5).and('be.visible');
  });

  it('renders multiple menu products with images, prices, and add buttons', () => {
    cy.get('.product-card').should('have.length.at.least', 3).each(($product) => {
      cy.wrap($product).find('h3').should('not.be.empty');
      cy.wrap($product).find('img').should('be.visible').and('have.attr', 'src');
      cy.wrap($product).find('.product-bottom strong').should('contain', '₹');
      cy.wrap($product).find('.add-button').should('be.visible');
    });
  });

  it('adds multiple products and calculates the cart total', () => {
    cy.then(() => productPrice(0)).as('firstPrice');
    cy.then(() => productPrice(1)).as('secondPrice');
    cy.addProductToCart(0);
    cy.addProductToCart(1);
    cy.openCart();
    cy.get('@firstPrice').then((firstPrice) => cy.get('@secondPrice').then((secondPrice) => {
      cy.get('.cart-count').first().should('have.text', '2');
      cy.get('.cart-row').should('have.length', 2);
      cy.get('.subtotal').should('have.text', `₹${firstPrice + secondPrice}`);
      cy.get('.total-price').should('have.text', `₹${firstPrice + secondPrice}`);
    }));
  });

  it('updates quantity in both directions and prevents an invalid quantity', () => {
    cy.addProductToCart(0);
    cy.openCart();
    cy.get('.cart-row [data-cart-qty][data-change="1"]').click();
    cy.get('.cart-row .qty span').should('have.text', '2');
    cy.get('.cart-row [data-cart-qty][data-change="-1"]').click();
    cy.get('.cart-row .qty span').should('have.text', '1');
    cy.get('.cart-row [data-cart-qty][data-change="-1"]').click();
    cy.get('.cart-row').should('not.exist');
    cy.get('.cart-empty').should('be.visible');
    cy.get('.cart-count').first().should('have.text', '0');
    cy.get('.total-price').should('have.text', '₹0');
  });

  it('removes a product and supports the empty-cart state', () => {
    cy.addProductToCart(0);
    cy.openCart();
    cy.get('.cart-row [data-remove]').click();
    cy.get('.cart-row').should('not.exist');
    cy.get('.cart-empty').should('be.visible').and('contain.text', 'Your cart is waiting');
    cy.get('.cart-count').first().should('have.text', '0');
    cy.get('.total-price').should('have.text', '₹0');
  });

  it('validates required and malformed customer details', () => {
    cy.addProductToCart(0);
    cy.openCart();
    cy.proceedToOrder();
    const invalidFields = [
      { selector: '[name="name"]', value: '' },
      { selector: '[name="email"]', value: '' },
      { selector: '[name="email"]', value: 'not-an-email' },
      { selector: '[name="address"]', value: '' },
      { selector: '[name="mobile"]', value: '' },
      { selector: '[name="mobile"]', value: '12345' },
    ];
    invalidFields.forEach(({ selector, value }) => {
      cy.get(selector).clear();
      if (value) cy.get(selector).type(value, { force: true });
      cy.get('#checkout-form').then(($form) => {
        expect($form[0].checkValidity(), `${selector} should be invalid`).to.be.false;
      });
    });
  });

  it('opens the payment step with the cart total and all payment options', () => {
    cy.fixture('customerData').then(({ validCustomer }) => {
      cy.addProductToCart(0);
      cy.openCart();
      cy.get('.total-price').invoke('text').then((total) => {
        cy.proceedToOrder();
        cy.fillCustomerDetails(validCustomer);
        cy.get('#checkout-form button[type="submit"]').click();
        cy.get('[data-step="payment"]').should('be.visible');
        cy.get('.pay-amount').should('have.text', total);
        cy.get('.payment-options label').should('have.length', 3).each(($option) => cy.wrap($option).find('span').should('be.visible'));
        cy.get('input[name="payment"][value="UPI"]').should('exist');
        cy.get('input[name="payment"][value="PhonePe"]').should('exist');
        cy.get('input[name="payment"][value="Net Banking"]').should('exist');
        cy.get('.pay-button').should('be.visible');
      });
    });
  });

  it('completes a UPI payment and clears the cart', () => completeCheckoutWith('UPI'));
  it('completes a PhonePe payment and clears the cart', () => completeCheckoutWith('PhonePe'));
  it('completes a Net Banking payment and clears the cart', () => completeCheckoutWith('Net Banking'));

  it('returns to shopping after a successful order', () => {
    completeCheckoutWith('UPI');
    cy.get('.continue-shopping').click();
    cy.get('.checkout-modal').should('not.be.visible');
    cy.get('#menu').should('be.visible');
  });
});
