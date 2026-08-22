# Spicy Adda Cypress Automation

This folder contains browser automation for the root `index.html` storefront. It is separate from the website implementation.

## Run the tests

1. Open this project in VS Code.
2. Install the test dependency from the project root:

   ```bash
   npm install
   ```

3. Start the existing website with VS Code Live Server. The default URL must be `http://127.0.0.1:5500/`.
4. Run Cypress in interactive mode:

   ```bash
   npm run test:open
   ```

   Or run headlessly:

   ```bash
   npm test
   ```

   Chrome can be used with `npm run test:chrome`.

The tests clear the `spicyAddaCart` localStorage entry before each test, load customer values from `cypress/fixtures/customerData.json`, and use reusable commands from `cypress/support/commands.js`.
