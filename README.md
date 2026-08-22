# Spicy Adda E-Commerce

## Standalone static storefront

The root `index.html`, `style.css`, and `script.js` provide a framework-free storefront that can be opened directly with VS Code Live Server. Open `index.html`, choose **Open with Live Server**, and use the menu, combo cards, cart drawer, and checkout form in the browser.

Menu items and prices are maintained in the `menuItems` array near the top of `script.js`; combo offers are in the `combos` array. The phone number, hours, and business copy are in `index.html`.

A complete full-stack e-commerce website built with Python Flask, SQLite, and modern front-end technologies.

## Project Structure

- `app/` - Flask application package
- `app/routes/` - Blueprints and route modules
- `app/static/` - CSS, JavaScript, and images
- `app/templates/` - Jinja2 templates
- `instance/` - Local configuration and database file
- `requirements.txt` - Python dependencies
- `run.py` - Application entry point
- `setup_db.py` - Database initialization script

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

## Initialize database

```bash
python setup_db.py
```

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

## Run the project

```bash
python run.py
```

## Access the application

- Open `http://127.0.0.1:5000/`
- Admin dashboard: `http://127.0.0.1:5000/admin/dashboard`

## Stop the server

- Press `Ctrl+C` in the terminal where the Flask server is running.
