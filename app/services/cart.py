from app import db
from app.models import CartItem


def get_cart_items(user_id):
    return CartItem.query.filter_by(user_id=user_id).all()


def calculate_item_total(cart_item):
    return cart_item.product.price * cart_item.quantity


def calculate_cart_total(cart_items):
    return sum(calculate_item_total(item) for item in cart_items)


def _parse_quantity(quantity):
    try:
        return int(quantity)
    except (TypeError, ValueError):
        raise ValueError('Quantity must be at least 1 and a valid number.')


def validate_quantity(quantity, available_stock):
    quantity = _parse_quantity(quantity)
    if quantity < 1:
        raise ValueError('Quantity must be at least 1 and a valid number.')
    if quantity > available_stock:
        raise ValueError('Requested quantity is greater than available stock.')
    return quantity


def add_product_to_cart(user_id, product, quantity):
    quantity = validate_quantity(quantity, product.stock)
    cart_item = CartItem.query.filter_by(user_id=user_id, product_id=product.id).first()
    requested_quantity = (cart_item.quantity if cart_item else 0) + quantity
    validate_quantity(requested_quantity, product.stock)

    if cart_item:
        cart_item.quantity = requested_quantity
    else:
        cart_item = CartItem(user_id=user_id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
    return cart_item


def set_cart_quantity(cart_item, quantity):
    cart_item.quantity = validate_quantity(quantity, cart_item.product.stock)
    return cart_item
