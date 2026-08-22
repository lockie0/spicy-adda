Cypress.Commands.add('startWithEmptyCart', () => {
  cy.clearLocalStorage('spicyAddaCart');
  cy.reload();
  cy.get('.cart-count').first().should('have.text', '0');
});

Cypress.Commands.add('addProductToCart', (productIndex = 0) => {
  cy.get('.product-card').eq(productIndex).find('.add-button').click();
});

Cypress.Commands.add('openCart', () => {
  cy.get('[data-open-cart]').click();
  cy.get('.cart-drawer').should('have.class', 'open');
});

Cypress.Commands.add('proceedToOrder', () => {
  cy.get('.checkout-button').click();
  cy.get('.checkout-modal').should('be.visible');
  cy.get('[data-step="details"]').should('be.visible');
});

Cypress.Commands.add('fillCustomerDetails', (customer) => {
  cy.get('[name="name"]').clear().type(customer.name);
  cy.get('[name="email"]').clear().type(customer.email);
  cy.get('[name="mobile"]').clear().type(customer.phone);
  cy.get('[name="address"]').clear().type(customer.address);
});

Cypress.Commands.add('selectPaymentMethod', (method) => {
  cy.get(`input[name="payment"][value="${method}"]`).check().should('be.checked');
});

Cypress.Commands.add('completePayment', (method) => {
  cy.selectPaymentMethod(method);
  cy.get('.pay-button').click();
  cy.get('.processing-step').should('be.visible');
  cy.get('.success-message', { timeout: 3000 }).should('be.visible');
});

Cypress.Commands.add('verifyOrderSuccess', (customer, total, method) => {
  cy.get('.success-message').should('contain.text', 'PAYMENT SUCCESSFUL');
  cy.get('.success-message').should('contain.text', customer.name);
  cy.get('.success-total').should('have.text', total);
  cy.get('.success-method').should('have.text', method);
  cy.get('.cart-count').first().should('have.text', '0');
  cy.window().its('localStorage.spicyAddaCart').should('equal', '[]');
});
