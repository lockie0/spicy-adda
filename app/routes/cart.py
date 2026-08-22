from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from app.models import CartItem, Product

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/cart')
@login_required
def cart():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in items)
    return render_template('cart.html', items=items, total=total)


@cart_bp.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity', type=int, default=1)
    item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=current_user.id, product_id=product.id, quantity=quantity)
        db.session.add(item)

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

    quantity = request.form.get('quantity', type=int, default=1)
    if quantity < 1:
        db.session.delete(item)
    else:
        item.quantity = quantity
    db.session.commit()
    flash('Cart updated successfully.', 'success')
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
