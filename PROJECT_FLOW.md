# Spicy Adda Project Flow

## 1. Project Overview

Spicy Adda is a Flask and SQLite e-commerce website for ordering Indian snacks, beverages, and combo products. Visitors can browse the shop, search and filter products, register with an office email, log in, add products to a cart, update quantities, save a delivery address, choose a payment method, place orders, and view personal or company order information.

The primary production flow is the Flask application started by `run.py`. A Django REST API and a React/Vite catalog also exist as a separate integration path, described in the final sections of this document.

The main Flask request flow is:

```text
Browser request
    -> Flask blueprint route
    -> WTForms/request validation
    -> service/helper
    -> SQLAlchemy model and SQLite database
    -> Jinja template or JSON response
```

## 2. Project Folder Structure

```text
spicy.py/
├── run.py
├── setup_db.py
├── requirements.txt
├── README.md
├── PROJECT_FLOW.md
├── app/
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── utils.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── shop.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   ├── admin.py
│   │   ├── employee.py
│   │   ├── api.py
│   │   ├── errors.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── auth.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   ├── address.py
│   │   └── dashboard.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── products.html
│   │   ├── product_detail.html
│   │   ├── cart.html
│   │   ├── checkout.html
│   │   ├── history.html
│   │   ├── order_detail.html
│   │   ├── success.html
│   │   ├── cancel.html
│   │   ├── payment_placeholder.html
│   │   ├── account.html
│   │   ├── contact.html
│   │   ├── faq.html
│   │   ├── about.html
│   │   ├── wishlist.html
│   │   ├── employee_dashboard.html
│   │   └── admin/
│   └── static/
│       ├── css/style.css
│       ├── js/main.js
│       └── images/
├── instance/app.db
├── instance/uploads/
├── images/
├── cypress/e2e/
├── django_backend/
└── frontend/
```

Important files:

| File | Responsibility | Used by |
|---|---|---|
| `run.py` | Creates the Flask app and starts the development server. | Local application startup. |
| `app/__init__.py` | Creates Flask, configures SQLAlchemy, LoginManager, CSRF, registers blueprints, creates missing schema columns, and synchronizes the catalog. | `run.py` and every Flask request. |
| `app/models.py` | Defines SQLAlchemy models and the Flask-Login user loader. | Routes and services. |
| `app/forms.py` | Defines registration, login, search, checkout, review, contact, and admin form fields/validation. | Auth, shop, and order routes. |
| `app/utils.py` | Image saving, currency/recently-viewed helpers, company detection, catalog constants, and catalog synchronization. | App startup, auth, shop, and admin flows. |
| `app/routes/*.py` | Converts HTTP requests into service calls and templates/redirects/JSON. | Flask routing. |
| `app/services/auth.py` | Normalizes emails, registers users, hashes passwords, and authenticates users. | `routes/auth.py`. |
| `app/services/cart.py` | Owns cart lookup, quantity validation, add/update operations, and price calculations. | Cart and order routes. |
| `app/services/address.py` | Checks, loads, saves, formats, and updates the current user's saved address. | Checkout route/template. |
| `app/services/orders.py` | Creates orders and order lines, verifies stock, decrements stock, and clears cart rows. | Checkout route. |
| `app/services/dashboard.py` | Retrieves orders, filters by company, and calculates today's completed order metrics. | Employee dashboard. |
| `app/templates/base.html` | Shared navigation, flash messages, CSS, JavaScript, and footer. | All Flask templates. |
| `app/templates/products.html` | Shop UI with filters and the `ALL ITEMS MENU`, `COMBOS`, and `OFFERS` sections. | `shop.products`. |
| `app/templates/cart.html` | Cart rows, quantity controls, subtotals, total, update/remove forms. | `cart.cart`. |
| `app/templates/checkout.html` | Saved/new address form, payment radios, and order summary. | `orders.checkout`. |
| `app/static/css/style.css` | Shared dark black and gold/yellow visual system and responsive layouts. | All Flask pages. |
| `app/static/js/main.js` | Flash-message dismissal, Change Address toggle, and immediate cart total preview. | `base.html`, cart, checkout. |
| `instance/app.db` | SQLite database used by the Flask application. | SQLAlchemy. |

## 3. Application Startup Flow

```text
run.py imports create_app()
    -> Flask app is created
    -> SECRET_KEY, SQLite path, upload path, and cookie settings load
    -> SQLAlchemy, Flask-Login, and CSRFProtect initialize
    -> auth, shop, cart, orders, admin, errors, API, and employee blueprints register
    -> db.create_all() creates missing tables
    -> user/order columns are checked and added when needed
    -> sync_product_catalog() creates missing categories/products
    -> app.run() serves http://127.0.0.1:5000
```

`app/__init__.py` uses additive `ALTER TABLE` operations for the newer designation, company, saved-address, and payment columns. Existing records are not dropped.

## 4. Registration Flow

```text
GET /account
    -> auth.account() creates RegistrationForm and LoginForm
    -> account.html displays registration fields
POST /account
    -> RegistrationForm validates username, designation, email, password, confirmation
    -> register_user() trims the username and normalizes the email
    -> get_company_from_email() maps pixelvide.com, tcs.com, or infosys.com
    -> generate_password_hash() securely hashes the password
    -> User is inserted into SQLite
    -> user is redirected to /account?mode=login
```

Files and functions: `app/routes/auth.py:account`, `app/forms.py:RegistrationForm`, `app/services/auth.py:register_user`, and `app/utils.py:get_company_from_email`.

## 5. Login Flow

```text
GET /account?mode=login
    -> account.html displays LoginForm
POST /account?mode=login
    -> LoginForm validates email/password presence and email format
    -> authenticate_user() normalizes the email and loads User
    -> User.check_password() verifies the password hash
    -> login_user() creates the Flask-Login session
    -> safe_next_url() accepts only a local-host redirect
    -> user goes to the employee dashboard
```

Files and functions: `app/routes/auth.py:account`, `safe_next_url`, and `logout`; `app/forms.py:LoginForm`; `app/services/auth.py:authenticate_user`; and `app/models.py:User.check_password`.

Logout uses `GET /logout`, calls `logout_user()`, flashes a message, and redirects to the home page.

## 6. Shop Flow

`GET /products` is handled by `app/routes/shop.py:products`.

```text
Shop request
    -> read q, category, sort, and page query parameters
    -> filter Product and Category query
    -> order by newest or price
    -> create the existing SearchForm
    -> split results into menu_products and combo_products
    -> pass offers, combo item names, and image mappings to products.html
    -> render ALL ITEMS MENU, COMBOS, and OFFERS
```

The page keeps existing product detail links and POST Add to Cart forms. Product data comes from `Product` rows synchronized by `sync_product_catalog()` in `app/utils.py`. Product images are stored in the product row or mapped to related existing food image URLs in `products.html`; failed images use `food-fallback.svg`.

The shop page preserves filtering through `q`, `category`, `sort`, and `page`. `GET /product/<product_id>` renders product details and accepts reviews for authenticated users.

## 7. Cart Flow

```text
POST /cart/add/<product_id>
    -> login_required checks the session
    -> Product is loaded
    -> add_product_to_cart() validates requested quantity and stock
    -> existing CartItem quantity increases, or a new row is created
    -> database commits
    -> redirect to /cart
```

Cart updates and removals are handled by `cart.update_cart` and `cart.remove_from_cart`. Both verify ownership before changing a cart row.

The reusable functions are in `app/services/cart.py`:

- `get_cart_items(user_id)` loads the user's rows.
- `calculate_item_total(cart_item)` returns `product.price * quantity`.
- `calculate_cart_total(cart_items)` sums item totals.
- `validate_quantity(quantity, available_stock)` rejects invalid or over-stock quantities.
- `add_product_to_cart(user_id, product, quantity)` creates or increases a row.
- `set_cart_quantity(cart_item, quantity)` validates and stores a new quantity.

The cart template displays the same server-calculated values. `main.js` gives immediate browser feedback when the quantity input or plus/minus controls change; the server recalculates and validates on submit.

## 8. Quantity and Price Calculation Flow

The authoritative formula is:

```text
item subtotal = product price * cart quantity
cart total = sum of all item subtotals
```

For a ₹30 product:

```text
quantity 1 -> ₹30
quantity 2 -> ₹60
quantity 3 -> ₹90
quantity 5 -> ₹150
```

For products priced at ₹30 and ₹50:

```text
₹30 * 2 + ₹50 * 3 = ₹60 + ₹150 = ₹210
```

The server source is `app/services/cart.py:calculate_item_total` and `calculate_cart_total`. Checkout calls `calculate_cart_total(items)` again from the current database rows. `save_order()` stores each order line's product price and quantity and uses the same cart quantities before clearing them. Order history, order details, dashboard totals, company orders, and API order responses read the persisted order total.

`cart.html` and `checkout.html` use the same multiplication for display, while the service remains authoritative for writes and final order totals.

## 9. Address Flow

Saved address data is stored on the `User` row in these nullable columns: `address_full_name`, `address_mobile`, `address_house`, `address_street`, `address_city`, `address_state`, and `address_pincode`.

```text
First checkout
    -> has_saved_address(current_user) returns false
    -> checkout.html shows the address fields
    -> CheckoutForm validates all fields
    -> save_user_address() updates the user row
    -> format_user_address() creates the order snapshot

Later checkout
    -> has_saved_address() returns true
    -> load_address_form() pre-fills the saved values
    -> checkout.html shows the saved address and Change Address

Change Address
    -> main.js hides the saved summary and shows editable fields
    -> user edits fields and submits the same checkout form
    -> save_user_address() updates the same User row
    -> the current order uses format_user_address() from the updated values
```

Files and functions: `app/services/address.py` (`has_saved_address`, `save_user_address`, `load_address_form`, `format_user_address`), `app/routes/orders.py:checkout`, `app/forms.py:CheckoutForm`, and `app/templates/checkout.html`.

## 10. Payment Flow

The active checkout choices are radio buttons and only one can be selected:

- PhonePe
- Google Pay
- Paytm
- Net Banking

```text
Checkout page
    -> CheckoutForm.payment_method renders RadioField options
    -> browser allows one selected radio value
    -> WTForms validates the selected choice
    -> checkout passes payment_method to create_order()
    -> Order.payment_method persists the choice
    -> success page is shown
```

The app currently records the selected method locally; it does not call an external PhonePe, Google Pay, Paytm, or bank gateway. `payment_placeholder.html` remains available for the older placeholder route, but the active four payment choices complete locally.

## 11. Order Creation Flow

```text
Cart
    -> GET /orders/checkout loads current CartItem rows
    -> calculate_cart_total() calculates the final amount
    -> address fields are validated/saved
    -> payment radio choice is validated
    -> create_order() builds Order with user, total, address, method, status
    -> save_order() flushes the order to get its id
    -> each CartItem becomes an OrderDetail with price and quantity
    -> stock is checked again before each decrement
    -> CartItem rows are deleted
    -> transaction commits
    -> /orders/success/<id> renders the result
```

`Order.shipping_address` stores the address snapshot for that order. `Order.payment_method` stores the selected method. The `OrderDetail` rows preserve the product price and quantity used at purchase time.

## 12. My Orders Flow

`GET /orders/history` is protected by `login_required` and loads the current user's orders ordered by newest first. `GET /orders/<order_id>` loads only an order belonging to the current user and renders its detail lines.

The API equivalents are `GET /api/orders` and `GET /api/orders/<order_id>`, both protected by Flask-Login. The API includes order total, status, payment method, address where applicable, date, and line item information.

## 13. Company Orders Flow

```text
Registration
    -> office email is normalized
    -> get_company_from_email() detects Pixelvide, TCS, or Infosys
    -> User.company stores the result

Employee dashboard
    -> employee.dashboard loads all orders
    -> filter_orders_by_company() compares order.user.company
    -> selected company tab filters the displayed list
    -> get_today_orders() keeps completed orders created today
    -> calculate_today_order_count() counts them
    -> calculate_today_revenue() sums their totals
```

Files and functions: `app/routes/employee.py:dashboard` and `app/services/dashboard.py` (`get_orders`, `get_user_orders`, `filter_orders_by_company`, `get_company_orders`, `get_today_orders`, `calculate_today_order_count`, `calculate_today_revenue`).

## 14. Database Relationships

```text
User
├── orders -> Order
├── reviews -> Review
├── cart_items -> CartItem
├── wishlist_items -> WishlistItem
└── messages -> ContactMessage

Category
└── products -> Product

Product
├── category -> Category
├── reviews -> Review
├── cart_items -> CartItem
├── wishlist_items -> WishlistItem
└── order_details -> OrderDetail

Order
└── details -> OrderDetail

CartItem -> Product
WishlistItem -> Product
OrderDetail -> Product
Review -> User and Product
ContactMessage -> User (optional)
```

The model classes are all in `app/models.py`. `CartItem` and `WishlistItem` use `back_populates` with Product. Orders use `Order.details` and `OrderDetail.product`; reviews and contact messages use SQLAlchemy backrefs.

## 15. Reusable Functions and Services

| Function/service | File | Purpose | Used by |
|---|---|---|---|
| `create_app` | `app/__init__.py` | Configure Flask, extensions, schema, blueprints, and catalog. | `run.py`. |
| `normalize_email` | `app/services/auth.py` | Trim and lowercase an email. | Registration and login. |
| `register_user` | `app/services/auth.py` | Detect duplicates, detect company, hash password, create User. | `auth.account`. |
| `authenticate_user` | `app/services/auth.py` | Find a user and verify the password. | `auth.account`. |
| `get_cart_items` | `app/services/cart.py` | Load a user's cart. | Cart, checkout, API. |
| `calculate_item_total` | `app/services/cart.py` | Calculate one product subtotal. | Cart, checkout, order logic. |
| `calculate_cart_total` | `app/services/cart.py` | Sum current cart subtotals. | Cart, checkout. |
| `validate_quantity` | `app/services/cart.py` | Validate integer quantity and stock limit. | Add/update cart and order stock check. |
| `add_product_to_cart` | `app/services/cart.py` | Create or increase a CartItem. | `cart.add_to_cart`, API. |
| `set_cart_quantity` | `app/services/cart.py` | Validate and update a CartItem. | `cart.update_cart`, API. |
| `has_saved_address` | `app/services/address.py` | Determine whether all address fields exist. | Checkout. |
| `save_user_address` | `app/services/address.py` | Save or update the same User address fields. | Checkout. |
| `load_address_form` | `app/services/address.py` | Pre-fill checkout fields from User. | Checkout. |
| `format_user_address` | `app/services/address.py` | Create an order address snapshot. | Checkout. |
| `create_order` | `app/services/orders.py` | Build an Order with total, address, status, and payment method. | Checkout. |
| `save_order` | `app/services/orders.py` | Create OrderDetail rows, recheck stock, decrement inventory, clear cart. | Checkout. |
| `get_company_from_email` | `app/utils.py` | Map supported office domains to company names. | Registration/dashboard. |
| `sync_product_catalog` | `app/utils.py` | Ensure catalog categories and products exist. | App startup. |
| `filter_orders_by_company` | `app/services/dashboard.py` | Filter orders using the user's company. | Employee dashboard. |
| `calculate_today_order_count` | `app/services/dashboard.py` | Count today's completed company orders. | Employee dashboard. |
| `calculate_today_revenue` | `app/services/dashboard.py` | Sum today's completed company order totals. | Employee dashboard. |

## 16. Complete End-to-End Flow

```text
Visitor
    -> Registration
    -> office email validation and company detection
    -> Login
    -> Employee dashboard
    -> Shop
    -> ALL ITEMS MENU / COMBOS / OFFERS
    -> Product details
    -> Add to Cart
    -> Increase or decrease quantity
    -> Product Price * Quantity subtotal
    -> Cart total
    -> Checkout
    -> Saved address check
    -> New address or Change Address
    -> PhonePe / Google Pay / Paytm / Net Banking selection
    -> Server-side total and stock validation
    -> Order creation
    -> Order items and stock update
    -> Cart cleared
    -> Success result
    -> My Orders / Order Detail
    -> Company Orders
    -> Pixelvide / TCS / Infosys filtering
    -> Today's order count and bill total
```

## Additional Application Paths

### Root static storefront

`index.html`, root `style.css`, `script.js`, and `image-mapping.js` form a separate framework-free demo storefront. It uses a browser `localStorage` cart and is not connected to Flask authentication, Flask cart rows, or Flask checkout. It is retained because it is a separately documented entry point in `README.md`; it should not be confused with the Flask application at `http://127.0.0.1:5000/`.

### Django and React integration

`django_backend/` contains a Django project configured to read the shared SQLite `category` and `product` tables through unmanaged models. Its API endpoints are:

- `GET /api/categories`
- `GET /api/products`
- `GET /api/products/<product_id>`

`frontend/` contains the React/Vite catalog. It consumes the Django product API and supports catalog search, category filtering, sorting, and product display. It does not replace the Flask authentication, cart, checkout, or order workflows. The Flask-rendered website remains the complete workflow application.

## Validation Notes

The final code should be checked with:

```text
python -m compileall -q app run.py setup_db.py
python -c "from run import app; print(app.url_map)"
```

The complete customer workflow should verify registration, login, company detection, catalog filters, cart quantities, subtotal formulas, saved address reuse/change, all four payment choices, order creation, order history, order detail, and employee company metrics. Invalid quantities, incomplete addresses, unauthenticated protected routes, and invalid redirects should be rejected safely.
