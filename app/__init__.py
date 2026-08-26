import os
from flask import Flask
from sqlalchemy import inspect, text
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(app.instance_path, "app.db")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=True,
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads'),
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    csrf.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.shop import shop_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp
    from app.routes.admin import admin_bp
    from app.routes.errors import errors_bp
    from app.routes.api import api_bp
    from app.routes.employee import employee_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(employee_bp)

    with app.app_context():
        db.create_all()
        user_columns = {column['name'] for column in inspect(db.engine).get_columns('user')}
        with db.engine.begin() as connection:
            if 'designation' not in user_columns:
                connection.execute(text('ALTER TABLE user ADD COLUMN designation VARCHAR(80)'))
            if 'company' not in user_columns:
                connection.execute(text('ALTER TABLE user ADD COLUMN company VARCHAR(120)'))
            address_columns = {
                'address_full_name': 'VARCHAR(120)',
                'address_mobile': 'VARCHAR(20)',
                'address_house': 'VARCHAR(120)',
                'address_street': 'VARCHAR(160)',
                'address_city': 'VARCHAR(80)',
                'address_state': 'VARCHAR(80)',
                'address_pincode': 'VARCHAR(12)',
            }
            for column_name, column_type in address_columns.items():
                if column_name not in user_columns:
                    connection.execute(text(f'ALTER TABLE user ADD COLUMN {column_name} {column_type}'))
            order_columns = {column['name'] for column in inspect(db.engine).get_columns('order')}
            if 'payment_method' not in order_columns:
                connection.execute(text('ALTER TABLE "order" ADD COLUMN payment_method VARCHAR(40)'))
            product_columns = {column['name'] for column in inspect(db.engine).get_columns('product')}
            if 'ingredients' not in product_columns:
                connection.execute(text('ALTER TABLE product ADD COLUMN ingredients TEXT'))
        from app.utils import sync_product_catalog
        sync_product_catalog()

    return app
