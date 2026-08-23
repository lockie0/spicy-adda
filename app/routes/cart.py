from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import CartItem, Product
from app.services.cart import add_product_to_cart, calculate_cart_total, get_cart_items, set_cart_quantity

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart')
@login_required
def cart():
    items = get_cart_items(current_user.id)
    total = calculate_cart_total(items)
    return render_template('cart.html', items=items, total=total)


@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    try:
        add_product_to_cart(current_user.id, product, request.form.get('quantity'))
    except ValueError as error:
        flash(str(error), 'danger')
        return redirect(url_for('shop.product_detail', product_id=product.id))

    db.session.commit()
    flash('Added to cart successfully.', 'success')
    return redirect(url_for('cart.cart'))


@cart_bp.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id != current_user.id:
        flash('Invalid cart update.', 'danger')
        return redirect(url_for('cart.cart'))

    try:
        set_cart_quantity(item, request.form.get('quantity'))
    except ValueError as error:
        flash(str(error), 'danger')
    else:
        flash('Cart updated successfully.', 'success')
    db.session.commit()
    return redirect(url_for('cart.cart'))


@cart_bp.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == current_user.id:
        db.session.delete(item)
        db.session.commit()
        flash('Item removed from cart.', 'success')
    return redirect(url_for('cart.cart'))
