from werkzeug.security import generate_password_hash
from app import create_app, db
from app.models import Category, Product, User

PRODUCTS = [
    ('Mirchi Bajji', 'Crispy stuffed chili fritters with spicy chutney.', 40, 'Snacks', 'default1.jpg', 80),
    ('Aloo Bonda', 'Soft potato dumplings fried to golden perfection.', 35, 'Snacks', 'default2.jpg', 70),
    ('Masala Puri', 'Crunchy puri topped with spicy masala gravy and sev.', 60, 'Chaat', 'default3.jpg', 50),
    ('Thums Up', 'Classic fizzy cola beverage to complete your meal.', 30, 'Beverages', 'default4.jpg', 100),
    ('Family Combo', '2 Mirchi Bajji + 2 Punnugulu + 2 Pani Puri + Masala Soda.', 199, 'Combos', 'default5.jpg', 40),
]

CATEGORIES = ['Snacks', 'Chaat', 'Beverages', 'Combos', 'Sweets', 'Street Food']


def seed_database():
    categories = {}
    for name in CATEGORIES:
        category = Category.query.filter_by(name=name).first()
        if not category:
            category = Category(name=name)
            db.session.add(category)
        categories[name] = category

    db.session.commit()

    for name, description, price, category_name, image, stock in PRODUCTS:
        category = categories.get(category_name)
        if not category:
            continue
        product = Product.query.filter_by(name=name).first()
        if not product:
            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category_id=category.id,
                image=image,
            )
            db.session.add(product)

    admin = User.query.filter_by(email='admin@spicyadda.com').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@spicyadda.com',
            password_hash=generate_password_hash('Admin@123'),
            is_admin=True,
        )
        db.session.add(admin)

    db.session.commit()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_database()
        print('Database initialized with sample data and admin user.')
