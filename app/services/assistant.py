import re
from collections import Counter

from app.models import Order, Product
from app.services.cart import calculate_cart_total, get_cart_items
from app.utils import COMBO_ITEMS, OFFER_CATALOG, get_product_ingredients


PAYMENT_OPTIONS = 'PhonePe, Google Pay, Paytm, and Net Banking'


def _money(value):
    return f'INR {value}'


def _find_products(products, query):
    normalized = query.casefold()
    return [product for product in products if product.name.casefold() in normalized or normalized in product.name.casefold()]


def _product_line(product):
    return f'{product.name} - {_money(product.price)}. {product.description}'


def _ingredient_text(product):
    ingredients = get_product_ingredients(product)
    if isinstance(ingredients, dict):
        groups = ingredients.get('ingredient_groups', {})
        included = ingredients.get('included_items', [])
        if included:
            text = f'{product.name} includes: {", ".join(included)}.'
        else:
            text = f'{product.name} ingredients: '
        if groups:
            return text + ' ' + ' '.join(f'{name}: {", ".join(items)}.' for name, items in groups.items())
        return text
    return f'{product.name} ingredients: {", ".join(ingredients)}.' if ingredients else f'Ingredient details are not available for {product.name} yet.'


def _combo_text(combo):
    items = COMBO_ITEMS.get(combo.name, [])
    counts = Counter(items)
    included = ', '.join(f'{quantity} x {name}' for name, quantity in counts.items())
    return f'{combo.name} includes {included}. Price: {_money(combo.price)}.'


def answer_question(message, user=None):
    query = ' '.join((message or '').strip().split())
    lowered = query.casefold()
    products = Product.query.order_by(Product.price.asc(), Product.name.asc()).all()
    combos = [product for product in products if product.category and product.category.name.casefold() == 'combos']
    regular_products = [product for product in products if not product.category or product.category.name.casefold() != 'combos']

    if not query:
        return 'Ask me about our menu, combos, offers, ingredients, orders, cart, delivery, or payments.'

    matched_combo = next((combo for combo in combos if combo.name.casefold() in lowered), None)
    if matched_combo and any(word in lowered for word in ('include', 'contain', 'inside', 'item', 'what')):
        return _combo_text(matched_combo)

    matched_product = next((product for product in products if product.name.casefold() in lowered), None)
    if matched_product and any(word in lowered for word in ('ingredient', 'made', 'use', 'contains')):
        return _ingredient_text(matched_product)

    if any(word in lowered for word in ('offer', 'discount', 'deal', 'sale')):
        return 'Current offers: ' + ' '.join(f'{name}: {description}' for name, description in OFFER_CATALOG)

    if any(word in lowered for word in ('payment', 'pay with', 'upi')):
        return f'You can pay using {PAYMENT_OPTIONS}. Select your preferred option during checkout.'

    if any(word in lowered for word in ('address', 'delivery location', 'deliver to')):
        if user and all(getattr(user, field, None) for field in ('address_city', 'address_state', 'address_pincode')):
            return f'Your saved delivery address is in {user.address_city}, {user.address_state} - {user.address_pincode}. You can review or change it at checkout.'
        return 'Add or update your delivery address during checkout. A saved address will be available for your next order.'

    budget_match = re.search(r'(?:under|within|below|have|budget(?:\s+is)?)[^0-9]{0,12}(\d+)', lowered)
    if budget_match:
        budget = int(budget_match.group(1))
        options = [product for product in products if product.price <= budget]
        if options:
            return f'With {_money(budget)}, you can order: ' + '; '.join(_product_line(product) for product in options[:8])
        return f'I could not find an item at or below {_money(budget)}.'

    if any(word in lowered for word in ('famous', 'popular', 'best seller', 'bestseller', 'favorite', 'favourite', 'top pick', 'must try')):
        popular_names = ('Mirchi Bajji', 'Bottani Chaat', 'Onion Bonda', 'Samosa Big', 'Chaat Special')
        popular = [product for name in popular_names for product in products if product.name == name]
        return 'Our popular picks are: ' + '; '.join(_product_line(product) for product in popular)

    if any(word in lowered for word in ('cart', 'basket', 'quantity', 'total')):
        if not user:
            return 'Please log in to view your cart quantity and total.'
        items = get_cart_items(user.id)
        if not items:
            return 'Your cart is empty.'
        summary = '; '.join(f'{item.product.name} x {item.quantity}' for item in items)
        return f'Your cart has {summary}. Current total: {_money(calculate_cart_total(items))}.'

    if any(word in lowered for word in ('order status', 'where is my order', 'track order', 'my order')):
        if not user:
            return 'Please log in so I can check your order status.'
        order_match = re.search(r'order\s*#?\s*(\d+)', lowered)
        order_query = Order.query.filter_by(user_id=user.id)
        order = order_query.filter_by(id=int(order_match.group(1))).first() if order_match else order_query.order_by(Order.created_at.desc()).first()
        if not order:
            return 'I could not find an order for your account.'
        return f'Order #{order.id} is {order.status}. Total: {_money(order.total)}. Payment: {order.payment_method or "not recorded"}.'

    if any(word in lowered for word in ('spicy', 'hot', 'fiery')):
        spicy = [product for product in regular_products if any(term in f'{product.name} {product.description}'.casefold() for term in ('spicy', 'chili', 'mirchi', 'masala'))]
        return 'For a spicy choice, try: ' + '; '.join(_product_line(product) for product in spicy[:5]) if spicy else 'Try Mirchi Bajji or Mirchi Bajji with Chaat from our menu.'

    if any(word in lowered for word in ('vegetarian', 'veg')):
        vegetarian = [product for product in regular_products if 'egg' not in product.name.casefold() and 'egg' not in product.description.casefold()]
        return 'Vegetarian choices include: ' + '; '.join(_product_line(product) for product in vegetarian[:8])

    if matched_product:
        return _product_line(matched_product) + f' Stock available: {matched_product.stock}.'

    if any(word in lowered for word in ('menu', 'price', 'item', 'recommend', 'suggest')):
        return 'Popular choices: ' + '; '.join(_product_line(product) for product in products[:8])

    return 'I can help with Spicy Adda menu, combos, offers, ingredients, orders, and payments.'
