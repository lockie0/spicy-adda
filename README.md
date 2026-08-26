# Spicy Adda E-Commerce

Spicy Adda is a Flask and SQLite snack-ordering application. The complete workflow is in the Flask app: registration, login, company detection, employee dashboard, shop, cart, checkout, saved address, payment selection, orders, and company reporting.

## Start Here

```powershell
.\.venv\Scripts\python.exe run.py
```

Open `http://127.0.0.1:5000/`.

The main pages are:

- `/` - homepage
- `/products` - Shop with `ALL ITEMS MENU`, `COMBOS`, and `OFFERS`
- `/cart` - authenticated cart
- `/orders/checkout` - address, payment, and order confirmation
- `/employee/dashboard` - company orders and today's metrics
- `/admin/dashboard` - administrator dashboard

## Understand the Structure

```text
spicy.py/
├── app/                         # Primary Flask application
│   ├── routes/                  # HTTP endpoints grouped by feature
│   ├── services/                # Reusable business rules
│   ├── templates/               # Jinja pages and admin pages
│   └── static/                  # Flask CSS, JavaScript, and images
├── instance/app.db             # SQLite data used by Flask
├── run.py                      # Flask entry point
├── setup_db.py                 # Seed/reset utility; review before running
├── django_backend/             # Optional Django REST product API
├── frontend/                   # Optional React/Vite catalog client
├── index.html                  # Separate standalone static demo entry point
├── style.css / script.js       # Static demo assets
├── image-mapping.js            # Static demo image mapping
├── PROJECT_FLOW.md             # Detailed feature and data flow
├── docs/ARCHITECTURE.md        # Architecture, ownership, and maintenance guide
├── requirements.txt            # Python dependencies
└── .gitignore                  # Generated-file exclusions
```

`app/routes/` should stay thin: receive a request, validate it, call a service, and return a template, redirect, or JSON response. Cart, address, order, authentication, and dashboard rules belong in `app/services/`.

Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for ownership boundaries and [PROJECT_FLOW.md](PROJECT_FLOW.md) for the complete file-by-file flow.

## Installation

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Initialize Database

```bash
python setup_db.py
```

This utility resets and seeds the local database. Do not run it when you need to preserve existing data.

## Create admin account

1. Run Python shell inside environment:
   ```bash
   python
   ```
2. Create admin user:
   ```python
   from app import create_app, db
   from app.models import User
   from werkzeug.security import generate_password_hash

   app = create_app()
   with app.app_context():
       admin = User(username='admin', email='admin@spicyadda.com', password_hash=generate_password_hash('Admin@123'), is_admin=True)
       db.session.add(admin)
       db.session.commit()
```

## Optional Django and React Stack

The optional Django API reads the shared product/category tables:

```powershell
.\.venv\Scripts\python.exe django_backend\manage.py runserver 127.0.0.1:8000
```

The React catalog is in `frontend/`. Build it with:

```powershell
Push-Location frontend
npm install
npm run build
Pop-Location
```

This optional catalog does not replace the Flask authentication, cart, checkout, or order workflow.

## LAN Access

To allow another device on the same Wi-Fi network to view the Flask app, run Flask on all interfaces:

```powershell
.\.venv\Scripts\python.exe -c "from run import app; app.run(host='0.0.0.0', port=5000)"
```

Use the host computer's Wi-Fi IP, for example `http://192.168.1.58:5000/`.

## Stop the Server

- Press `Ctrl+C` in the terminal where the Flask server is running.
