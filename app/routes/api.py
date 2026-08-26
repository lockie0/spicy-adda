from flask import Blueprint, jsonify, request, abort
from flask_login import current_user, login_required
from app.models import Product, Category, CartItem, Order
from app import db, csrf
from app.services.cart import add_product_to_cart, calculate_item_total, get_cart_items, set_cart_quantity
from app.services.assistant import answer_question

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/assistant', methods=['POST'])
@csrf.exempt
def assistant():
    body = request.get_json(silent=True) or {}
    message = body.get('message', '')
    if not isinstance(message, str):
        abort(400)
    return jsonify({'reply': answer_question(message, current_user if current_user.is_authenticated else None)})


def product_to_dict(product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'stock': product.stock,
        'category': product.category.name if product.category else None,
        'image': product.image,
        'ingredients': product.ingredients,
        'created_at': product.created_at.isoformat(),
    }


@api_bp.route('/categories')
def categories():
    categories = Category.query.order_by(Category.name).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in categories])


@api_bp.route('/products')
def products():
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    sort_by = request.args.get('sort', 'newest')

    items = Product.query
    if query:
        items = items.filter(Product.name.ilike(f'%{query}%') | Product.description.ilike(f'%{query}%'))
    if category_id:
        items = items.filter_by(category_id=category_id)

    if sort_by == 'price_asc':
        items = items.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        items = items.order_by(Product.price.desc())
    else:
        items = items.order_by(Product.created_at.desc())

    return jsonify([product_to_dict(product) for product in items.all()])


@api_bp.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product_to_dict(product))


@api_bp.route('/cart')
@login_required
def cart_items():
    items = get_cart_items(current_user.id)
    data = []
    for item in items:
        data.append({
            'id': item.id,
            'product': product_to_dict(item.product),
            'quantity': item.quantity,
            'subtotal': calculate_item_total(item),
        })
    return jsonify(data)


@api_bp.route('/cart', methods=['POST'])
@login_required
def add_cart_item():
    body = request.get_json() or {}
    product_id = body.get('product_id')
    quantity = body.get('quantity', 1)
    if not product_id:
        abort(400)

    product = Product.query.get_or_404(product_id)
    try:
        item = add_product_to_cart(current_user.id, product, quantity)
    except ValueError:
        abort(400)
    db.session.commit()
    return jsonify({'success': True, 'cart_item_id': item.id})


@api_bp.route('/cart/<int:item_id>', methods=['PUT', 'DELETE'])
@login_required
def update_cart_item(item_id):
    item = CartItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    if request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return jsonify({'success': True})

    body = request.get_json() or {}
    try:
        set_cart_quantity(item, body.get('quantity'))
    except ValueError:
        abort(400)
    db.session.commit()
    return jsonify({'success': True, 'quantity': item.quantity})


@api_bp.route('/orders', methods=['GET'])
@login_required
def list_orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return jsonify([
        {
            'id': order.id,
            'total': order.total,
            'status': order.status,
                'payment_method': order.payment_method,
            'created_at': order.created_at.isoformat(),
        }
        for order in orders
    ])


@api_bp.route('/orders/<int:order_id>')
@login_required
def order_detail_api(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return jsonify({
        'id': order.id,
        'total': order.total,
        'status': order.status,
        'payment_method': order.payment_method,
        'shipping_address': order.shipping_address,
        'items': [
            {
                'product_name': detail.product.name,
                'quantity': detail.quantity,
                'price': detail.price,
            }
            for detail in order.details
        ],
    })
