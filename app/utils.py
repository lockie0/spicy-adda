import json
import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}


def save_image(file):
    filename = secure_filename(file.filename or '')
    if allowed_file(filename):
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        file.save(image_path)
        return filename
    return None


def allowed_file(filename):
    return bool(filename and '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS)


def format_currency(value):
    try:
        return f'₹{value:,}'
    except Exception:
        return str(value)


def get_recently_viewed(session):
    return session.get('recently_viewed', [])


def add_recently_viewed(session, product_id):
    recent = session.get('recently_viewed', [])
    if product_id in recent:
        recent.remove(product_id)
    recent.insert(0, product_id)
    session['recently_viewed'] = recent[:6]


COMPANY_DOMAINS = {
    'pixelvide.com': 'Pixelvide',
    'tcs.com': 'TCS',
    'infosys.com': 'Infosys',
}

SHOP_CATEGORIES = [
    ('all', 'All Categories'),
    ('menu', 'Menu Items'),
    ('combos', 'Combos'),
    ('offers', 'Offers'),
    ('snacks', 'Snacks'),
    ('chaat', 'Chaat'),
    ('beverages', 'Beverages'),
    ('street-food', 'Street Food'),
    ('sweets', 'Sweets'),
]

PRODUCT_CATALOG = [
    ('Challapunukulu', 'Street Food', 30, 'Crispy golden challapunukulu, freshly fried.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=900&q=85'),
    ('Mirchi Bajji', 'Snacks', 30, 'Crispy stuffed chili fritters with spicy chutney.', 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Banana_fritters.jpg'),
    ('Mirchi Bajji with Chaat', 'Chaat', 40, 'Mirchi bajji served with fresh, tangy chaat.', 'https://upload.wikimedia.org/wikipedia/commons/5/52/Onion_Pakora_or_peaji.JPG'),
    ('Onion Bonda', 'Snacks', 30, 'Crispy onion bonda with a soft, seasoned centre.', 'https://upload.wikimedia.org/wikipedia/commons/5/52/Onion_Pakora_or_peaji.JPG'),
    ('Banana Bajji', 'Snacks', 30, 'Sweet banana slices dipped in a crisp batter.', 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Banana_fritters.jpg'),
    ('Banana Bajji with Chaat', 'Chaat', 40, 'Banana bajji paired with bright, spicy chaat.', 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Banana_fritters.jpg'),
    ('Onion Pakodi', 'Snacks', 30, 'Crunchy onion pakodi with classic Indian spices.', 'https://upload.wikimedia.org/wikipedia/commons/5/52/Onion_Pakora_or_peaji.JPG'),
    ('Maramaralu Mirchi', 'Street Food', 35, 'Crispy puffed rice and chili street snack.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=900&q=85'),
    ('Tomato Mirchi', 'Street Food', 35, 'Bold tomato and chili snack with a fiery finish.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=900&q=85'),
    ('Maramaralu with Kaju Mirchi', 'Street Food', 50, 'Puffed rice, cashews, and chili in a crunchy mix.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=900&q=85'),
    ('Bottani Chaat', 'Chaat', 30, 'Tangy chaat topped with fresh herbs and crunch.', 'https://upload.wikimedia.org/wikipedia/commons/d/d6/Delhi_Chaat_in_Mumbai.jpg'),
    ('Chanagapindi Pakodi', 'Snacks', 30, 'Golden gram-flour pakodi with a crisp bite.', 'https://upload.wikimedia.org/wikipedia/commons/5/52/Onion_Pakora_or_peaji.JPG'),
    ('Egg Bajji', 'Snacks', 30, 'Spiced egg wrapped in a crisp golden coating.', 'https://upload.wikimedia.org/wikipedia/commons/5/52/Onion_Pakora_or_peaji.JPG'),
    ('Bread Bajji', 'Snacks', 30, 'Crispy bread bajji, perfect with spicy chutney.', 'https://upload.wikimedia.org/wikipedia/commons/5/52/Onion_Pakora_or_peaji.JPG'),
    ('Samosa Big', 'Snacks', 15, 'Large crisp samosa with a savoury filling.', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=85'),
    ('Spicy Starter', 'Combos', 49, 'Mirchi Bajji and Onion Bonda.', 'https://upload.wikimedia.org/wikipedia/commons/5/52/Onion_Pakora_or_peaji.JPG'),
    ('Chaat Special', 'Combos', 59, 'Mirchi Bajji with Chaat and Bottani Chaat.', 'https://upload.wikimedia.org/wikipedia/commons/d/d6/Delhi_Chaat_in_Mumbai.jpg'),
    ('Bonda Blast', 'Combos', 59, 'Onion Bonda, Challapunukulu, and Samosa Big.', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=85'),
    ('Bajji Lovers', 'Combos', 69, 'Banana Bajji, Mirchi Bajji, and Samosa Big.', 'https://upload.wikimedia.org/wikipedia/commons/9/9e/Banana_fritters.jpg'),
    ('Friends Combo', 'Combos', 69, 'Mirchi Bajji, Onion Pakodi, and Bottani Chaat.', 'https://upload.wikimedia.org/wikipedia/commons/d/d6/Delhi_Chaat_in_Mumbai.jpg'),
    ('Family Saver', 'Combos', 89, 'Onion Bonda, Mirchi Bajji, and Challapunukulu.', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?auto=format&fit=crop&w=900&q=85'),
    ('Spicy Adda Mega Combo', 'Combos', 119, 'Mirchi Bajji, Banana Bajji, Onion Bonda, Onion Pakodi, and Samosa Big.', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?auto=format&fit=crop&w=900&q=85'),
]

COMBO_ITEMS = {
    'Spicy Adda Mega Combo': ['Mirchi Bajji', 'Banana Bajji', 'Onion Bonda', 'Onion Pakodi'],
    'Family Saver': ['Onion Bonda', 'Mirchi Bajji', 'Challapunukulu', 'Samosa Big'],
    'Friends Combo': ['Mirchi Bajji', 'Onion Pakodi', 'Bottani Chaat', 'Mirchi Bajji'],
    'Bajji Lovers': ['Banana Bajji', 'Mirchi Bajji', 'Samosa Big', 'Banana Bajji'],
    'Bonda Blast': ['Onion Bonda', 'Challapunukulu', 'Samosa Big', 'Mirchi Bajji'],
    'Chaat Special': ['Mirchi Bajji with Chaat', 'Bottani Chaat', 'Mirchi Bajji with Chaat', 'Bottani Chaat'],
    'Spicy Starter': ['Mirchi Bajji', 'Onion Bonda', 'Mirchi Bajji', 'Onion Bonda'],
    'Family Combo': ['Mirchi Bajji', 'Onion Bonda', 'Challapunukulu', 'Samosa Big'],
}

COMBO_SHOWCASE_ORDER = [
    'Spicy Adda Mega Combo',
    'Family Saver',
    'Friends Combo',
    'Bajji Lovers',
    'Bonda Blast',
    'Chaat Special',
    'Spicy Starter',
    'Family Combo',
]

OFFER_CATALOG = [
    ('Grand Opening Offer', 'Buy 2 Mirchi Bajji and get 1 free.'),
    ('Student Offer', '10% off orders above ₹200 with a student ID.'),
    ('Happy Hours Offer', 'Any 2 snacks for ₹50, Monday to Thursday, 4 PM to 6 PM.'),
    ('Family Offer', 'Get ₹30 off when you spend ₹300.'),
    ('Loyalty Offer', 'Your 10th snack is free after 9 purchases.'),
]

BASE_PRODUCT_INGREDIENTS = {
    'Challapunukulu': [
        'Maida / All-Purpose Flour',
        'Sour Curd',
        'Salt',
        'Cumin Seeds',
        'Green Chillies',
        'Ginger',
        'Curry Leaves',
        'Cooking Soda / Baking Soda',
        'Water',
        'Oil for Frying',
    ],
    'Mirchi Bajji': [
        'Green Chillies',
        'Gram Flour / Besan',
        'Rice Flour',
        'Salt',
        'Turmeric',
        'Cumin Seeds',
        'Ajwain / Carom Seeds',
        'Ginger',
        'Garlic',
        'Water',
        'Oil for Frying',
    ],
    'Mirchi Bajji with Chaat': [
        'Green Chillies',
        'Gram Flour / Besan',
        'Rice Flour',
        'Salt',
        'Cumin Seeds',
        'Tangy Chaat Masala',
        'Fresh Coriander',
        'Onion',
        'Lemon Juice',
        'Water',
        'Oil for Frying',
    ],
    'Onion Bonda': [
        'Onions',
        'Gram Flour / Besan',
        'Rice Flour',
        'Salt',
        'Curry Leaves',
        'Green Chillies',
        'Turmeric',
        'Ginger',
        'Water',
        'Oil for Frying',
    ],
    'Banana Bajji': [
        'Banana Slices',
        'Gram Flour / Besan',
        'Rice Flour',
        'Salt',
        'Turmeric',
        'Cumin Seeds',
        'Chilli Powder',
        'Water',
        'Oil for Frying',
    ],
    'Banana Bajji with Chaat': [
        'Banana Slices',
        'Gram Flour / Besan',
        'Rice Flour',
        'Salt',
        'Turmeric',
        'Chaat Masala',
        'Fresh Coriander',
        'Onion',
        'Lemon Juice',
        'Water',
        'Oil for Frying',
    ],
    'Onion Pakodi': [
        'Onions',
        'Gram Flour / Besan',
        'Rice Flour',
        'Salt',
        'Chilli Powder',
        'Turmeric',
        'Curry Leaves',
        'Water',
        'Oil for Frying',
    ],
    'Maramaralu Mirchi': [
        'Green Chillies',
        'Puffed Rice',
        'Peanuts',
        'Cumin Seeds',
        'Mustard Seeds',
        'Curry Leaves',
        'Turmeric',
        'Salt',
        'Oil',
    ],
    'Tomato Mirchi': [
        'Tomatoes',
        'Green Chillies',
        'Coriander',
        'Onions',
        'Salt',
        'Lemon Juice',
        'Chilli Powder',
        'Oil',
    ],
    'Maramaralu with Kaju Mirchi': [
        'Puffed Rice',
        'Cashews',
        'Green Chillies',
        'Cumin Seeds',
        'Mustard Seeds',
        'Curry Leaves',
        'Turmeric',
        'Salt',
        'Oil',
    ],
    'Bottani Chaat': [
        'Bottle Gourd / Bottle Gourd Pieces',
        'Yogurt / Dahi',
        'Chaat Masala',
        'Tamarind Chutney',
        'Mint Chutney',
        'Onion',
        'Coriander',
        'Sev',
        'Salt',
        'Lemon Juice',
    ],
    'Chanagapindi Pakodi': [
        'Gram Flour / Besan',
        'Salt',
        'Chilli Powder',
        'Cumin Seeds',
        'Ajwain / Carom Seeds',
        'Turmeric',
        'Water',
        'Oil for Frying',
    ],
    'Egg Bajji': [
        'Eggs',
        'Gram Flour / Besan',
        'Rice Flour',
        'Salt',
        'Chilli Powder',
        'Pepper',
        'Water',
        'Oil for Frying',
    ],
    'Bread Bajji': [
        'Bread Slices',
        'Gram Flour / Besan',
        'Rice Flour',
        'Salt',
        'Chilli Powder',
        'Turmeric',
        'Water',
        'Oil for Frying',
    ],
    'Samosa Big': [
        'Maida / All-Purpose Flour',
        'Potatoes',
        'Peas',
        'Onion',
        'Green Chillies',
        'Cumin Seeds',
        'Garam Masala',
        'Salt',
        'Coriander',
        'Oil for Frying',
    ],
}

PRODUCT_INGREDIENTS = dict(BASE_PRODUCT_INGREDIENTS)
PRODUCT_INGREDIENTS.update({
    'Family Combo': {
        'included_items': ['Mirchi Bajji', 'Onion Bonda', 'Challapunukulu'],
        'ingredient_groups': {
            'Mirchi Bajji': BASE_PRODUCT_INGREDIENTS['Mirchi Bajji'],
            'Onion Bonda': BASE_PRODUCT_INGREDIENTS['Onion Bonda'],
            'Challapunukulu': BASE_PRODUCT_INGREDIENTS['Challapunukulu'],
        },
    },
    'Spicy Starter': {
        'included_items': ['Mirchi Bajji', 'Onion Bonda'],
        'ingredient_groups': {
            'Mirchi Bajji': BASE_PRODUCT_INGREDIENTS['Mirchi Bajji'],
            'Onion Bonda': BASE_PRODUCT_INGREDIENTS['Onion Bonda'],
        },
    },
    'Chaat Special': {
        'included_items': ['Mirchi Bajji with Chaat', 'Bottani Chaat'],
        'ingredient_groups': {
            'Mirchi Bajji with Chaat': BASE_PRODUCT_INGREDIENTS['Mirchi Bajji with Chaat'],
            'Bottani Chaat': BASE_PRODUCT_INGREDIENTS['Bottani Chaat'],
        },
    },
    'Bonda Blast': {
        'included_items': ['Onion Bonda', 'Challapunukulu', 'Samosa Big'],
        'ingredient_groups': {
            'Onion Bonda': BASE_PRODUCT_INGREDIENTS['Onion Bonda'],
            'Challapunukulu': BASE_PRODUCT_INGREDIENTS['Challapunukulu'],
            'Samosa Big': BASE_PRODUCT_INGREDIENTS['Samosa Big'],
        },
    },
    'Bajji Lovers': {
        'included_items': ['Banana Bajji', 'Mirchi Bajji', 'Samosa Big'],
        'ingredient_groups': {
            'Banana Bajji': BASE_PRODUCT_INGREDIENTS['Banana Bajji'],
            'Mirchi Bajji': BASE_PRODUCT_INGREDIENTS['Mirchi Bajji'],
            'Samosa Big': BASE_PRODUCT_INGREDIENTS['Samosa Big'],
        },
    },
    'Friends Combo': {
        'included_items': ['Mirchi Bajji', 'Onion Pakodi', 'Bottani Chaat'],
        'ingredient_groups': {
            'Mirchi Bajji': BASE_PRODUCT_INGREDIENTS['Mirchi Bajji'],
            'Onion Pakodi': BASE_PRODUCT_INGREDIENTS['Onion Pakodi'],
            'Bottani Chaat': BASE_PRODUCT_INGREDIENTS['Bottani Chaat'],
        },
    },
    'Family Saver': {
        'included_items': ['Onion Bonda', 'Mirchi Bajji', 'Challapunukulu'],
        'ingredient_groups': {
            'Onion Bonda': BASE_PRODUCT_INGREDIENTS['Onion Bonda'],
            'Mirchi Bajji': BASE_PRODUCT_INGREDIENTS['Mirchi Bajji'],
            'Challapunukulu': BASE_PRODUCT_INGREDIENTS['Challapunukulu'],
        },
    },
    'Spicy Adda Mega Combo': {
        'included_items': ['Mirchi Bajji', 'Banana Bajji', 'Onion Bonda', 'Onion Pakodi', 'Samosa Big'],
        'ingredient_groups': {
            'Mirchi Bajji': BASE_PRODUCT_INGREDIENTS['Mirchi Bajji'],
            'Banana Bajji': BASE_PRODUCT_INGREDIENTS['Banana Bajji'],
            'Onion Bonda': BASE_PRODUCT_INGREDIENTS['Onion Bonda'],
            'Onion Pakodi': BASE_PRODUCT_INGREDIENTS['Onion Pakodi'],
            'Samosa Big': BASE_PRODUCT_INGREDIENTS['Samosa Big'],
        },
    },
})


def parse_ingredients_value(value):
    if value is None:
        return []
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        clean = value.strip()
        if not clean:
            return []
        try:
            parsed = json.loads(clean)
            if isinstance(parsed, (list, dict)):
                return parsed
        except (TypeError, ValueError):
            pass
        items = []
        for line in clean.replace('\\n', '\n').splitlines():
            entry = line.strip().strip('•-*').strip()
            if entry:
                items.append(entry)
        if items:
            return items
        return [item.strip() for item in clean.split(',') if item.strip()]
    return []


def get_product_ingredients(product):
    if product is None:
        return []
    if product.ingredients:
        parsed = parse_ingredients_value(product.ingredients)
        if parsed:
            return parsed
    lookup_name = product.name.strip()
    if lookup_name in PRODUCT_INGREDIENTS:
        return PRODUCT_INGREDIENTS[lookup_name]
    normalized_name = lookup_name.lower().replace('_', ' ')
    for key, value in PRODUCT_INGREDIENTS.items():
        if key.lower().replace('_', ' ') == normalized_name:
            return value
    return []


def get_company_from_email(email):
    domain = email.rsplit('@', 1)[-1].strip().lower()
    return COMPANY_DOMAINS.get(domain, domain.split('.')[0].title())


def sync_product_catalog():
    from app import db
    from app.models import Category, Product

    category_map = {}
    for category_name in {item[1] for item in PRODUCT_CATALOG}:
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.flush()
        category_map[category_name] = category

    for name, category_name, price, description, image in PRODUCT_CATALOG:
        product = Product.query.filter_by(name=name).first()
        if not product:
            product = Product(name=name, description=description, price=price, stock=50, image=image, category_id=category_map[category_name].id)
            db.session.add(product)
        elif product.image.startswith('default') or not product.image:
            product.image = image
        if not product.ingredients:
            product.ingredients = json.dumps(PRODUCT_INGREDIENTS.get(name, []))
    for name, ingredients in {
        'Family Combo': PRODUCT_INGREDIENTS['Family Combo'],
    }.items():
        product = Product.query.filter_by(name=name).first()
        if product and not product.ingredients:
            product.ingredients = json.dumps(ingredients)
    db.session.commit()
