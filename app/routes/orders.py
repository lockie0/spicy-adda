from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user

from app import db
from app.forms import CheckoutForm
from app.models import Order
from app.services.cart import calculate_cart_total, get_cart_items
from app.services.orders import create_order, save_order
from app.services.address import format_user_address, has_saved_address, load_address_form, save_user_address

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')


@orders_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    items = get_cart_items(current_user.id)
    if not items:
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('shop.products'))

    total = calculate_cart_total(items)
    form = CheckoutForm()
    saved_address = has_saved_address(current_user)
    if request.method == 'GET' and saved_address:
        load_address_form(current_user, form)
    elif saved_address and not any(request.form.get(name) for name in ('full_name', 'mobile', 'house_number', 'street', 'city', 'state', 'pincode')):
        load_address_form(current_user, form)

    if form.validate_on_submit():
        save_user_address(current_user, form)
        shipping_address = format_user_address(current_user)
        order = create_order(
            user_id=current_user.id,
            total=total,
            shipping_address=shipping_address,
            payment_method=form.payment_method.data,
            status='Completed',
        )
        try:
            save_order(order, items)
        except ValueError as error:
            db.session.rollback()
            flash(str(error), 'danger')
            return redirect(url_for('cart.cart'))
        session['last_order'] = order.id

        if form.payment_method.data == 'stripe':
            return redirect(url_for('orders.payment_placeholder', order_id=order.id))

        return redirect(url_for('orders.success', order_id=order.id))

    return render_template('checkout.html', items=items, total=total, form=form, saved_address=saved_address)


@orders_bp.route('/payment/<int:order_id>')
@login_required
def payment_placeholder(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    return render_template('payment_placeholder.html', order=order)


@orders_bp.route('/success/<int:order_id>')
@login_required
def success(order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first_or_404()
    if order.status == 'Processing':
        order.status = 'Completed'
        db.session.commit()
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
