# Spicy Adda Architecture

## Runtime Map

The repository contains three intentionally separate runtime surfaces:

```text
Spicy Adda repository
├── Flask website (complete application)
│   ├── run.py
│   ├── app/
│   └── instance/app.db
│
├── Django API + React catalog (optional integration)
│   ├── django_backend/
│   └── frontend/
│
└── Static storefront demo (standalone, legacy)
    ├── index.html
    ├── style.css
    ├── script.js
    └── image-mapping.js
```

The Flask website is the primary application because it owns authentication, employee dashboards, cart rows, checkout, saved addresses, payments, orders, and company reports.

## Primary Flask Application

```text
run.py
└── app.create_app()
    ├── app/__init__.py       Flask and extension setup
    ├── app/models.py         SQLAlchemy database models
    ├── app/forms.py          WTForms validation
    ├── app/routes/           HTTP route handlers
    ├── app/services/         Reusable business logic
    ├── app/templates/        Jinja pages
    └── app/static/           CSS, JavaScript, and images
```

### Route Ownership

| Area | Blueprint | Main paths |
|---|---|---|
| Authentication | `app/routes/auth.py` | `/account`, `/login`, `/register`, `/logout` |
| Shop | `app/routes/shop.py` | `/`, `/products`, `/product/<id>`, `/wishlist` |
| Cart | `app/routes/cart.py` | `/cart`, `/cart/add/<id>`, `/cart/update/<id>` |
| Orders | `app/routes/orders.py` | `/orders/checkout`, `/orders/history`, `/orders/<id>` |
| Employee | `app/routes/employee.py` | `/employee/dashboard` |
| Admin | `app/routes/admin.py` | `/admin/...` |
| JSON API | `app/routes/api.py` | `/api/products`, `/api/cart`, `/api/orders` |

### Service Ownership

| Service | Responsibility |
|---|---|
| `app/services/auth.py` | Registration, password hashing, email normalization, login. |
| `app/services/cart.py` | Cart lookup, quantity validation, item subtotal, cart total, add/update. |
| `app/services/address.py` | Saved address detection, loading, saving, updating, formatting. |
| `app/services/orders.py` | Order creation, order lines, stock recheck, inventory decrement, cart clearing. |
| `app/services/dashboard.py` | User orders, company filtering, today's order count and revenue. |
| `app/utils.py` | Company mapping, catalog synchronization, images, shared catalog constants. |

## Database

The Flask application uses `instance/app.db` (SQLite). `app/__init__.py` creates missing tables and adds newer nullable columns without deleting existing data.

```text
User
├── saved address fields
├── CartItem rows
├── WishlistItem rows
├── Order rows
└── Review / ContactMessage rows

Category
└── Product rows
Order
└── OrderDetail rows
```

`Product.price * quantity` is the authoritative item subtotal calculation in `app/services/cart.py`. Checkout calls the same cart-total service before `app/services/orders.py` persists the order.

## Frontend Ownership

### Flask templates

The complete user workflow uses `app/templates/`. `base.html` supplies shared navigation, flash messages, CSS, and JavaScript. `products.html` owns the current dark/gold Shop page with `ALL ITEMS MENU`, `COMBOS`, and `OFFERS`.

### Django and React

`django_backend/` is an optional Django REST API that reads the shared product/category tables. `frontend/` is a Vite React catalog that consumes that API for product browsing, search, filtering, and sorting.

React is not the owner of Flask login sessions, cart mutations, checkout, or orders. Do not treat it as a replacement for the complete Flask application unless a deliberate migration is planned.

### Static demo

The root `index.html`, `style.css`, `script.js`, and `image-mapping.js` are a separate Live Server demo. Its cart uses browser localStorage and is intentionally independent of Flask sessions and SQLite.

## Local Commands

Primary complete website:

```powershell
.\.venv\Scripts\python.exe run.py
```

Open `http://127.0.0.1:5000/`.

Django API:

```powershell
.\.venv\Scripts\python.exe django_backend\manage.py runserver 127.0.0.1:8000
```

React development catalog:

```powershell
Push-Location frontend
npm install
npm run dev
Pop-Location
```

Build React for the Django host:

```powershell
Push-Location frontend
npm run build
Pop-Location
```

## Safe Maintenance Rules

- Keep `run.py` at the repository root because it is the Flask entry point.
- Keep `django_backend/` and `frontend/` at the root because their settings and Vite paths depend on that location.
- Keep the four root static demo files together because `index.html` references them by relative path.
- Do not run `setup_db.py` against a valuable database without reviewing it first; it is a seed/reset script.
- Add new business logic to the relevant service before adding logic to a route.
- Use `app/templates/base.html` and existing shared CSS classes before creating new page-level patterns.
- Run Python compilation, Flask smoke tests, and the end-to-end workflow after changes to auth, cart, checkout, or orders.
