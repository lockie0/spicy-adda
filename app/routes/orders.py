from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user

from app import db
from app.forms import CheckoutForm
from app.models import CartItem, Order, OrderDetail, Product

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('shop.products'))

    total = sum(item.product.price * item.quantity for item in items)
    form = CheckoutForm()

    if form.validate_on_submit():
        order = Order(
            user_id=current_user.id,
            total=total,
            shipping_address=form.address.data.strip(),
            status='Processing',
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            detail = OrderDetail(
                order_id=order.id,
                product_id=item.product.id,
                quantity=item.quantity,
                price=item.product.price,
            )
            db.session.add(detail)
            item.product.stock -= item.quantity
            db.session.delete(item)

        db.session.commit()
        session['last_order'] = order.id

        if form.payment_method.data == 'stripe':
            return redirect(url_for('orders.payment_placeholder', order_id=order.id))

        return redirect(url_for('orders.success', order_id=order.id))

    return render_template('checkout.html', items=items, total=total, form=form)


@orders_bp.route('/payment/<int:order_id>')
@login_required
def payment_placeholder(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('payment_placeholder.html', order=order)


@orders_bp.route('/success/<int:order_id>')
@login_required
def success(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('success.html', order=order)


@orders_bp.route('/cancel/<int:order_id>')
@login_required
def cancel(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    order.status = 'Cancelled'
    db.session.commit()
    flash('Payment cancelled. Your order has been marked as cancelled.', 'warning')
    return render_template('cancel.html', order=order)


@orders_bp.route('/history')
@login_required
def history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('history.html', orders=orders)


@orders_bp.route('/<int:order_id>')
@login_required
def detail(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('order_detail.html', order=order)
