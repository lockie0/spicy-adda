import os
from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user, login_user
from werkzeug.utils import secure_filename

from app import db
from app.forms import CategoryForm
from app.models import User, Product, Category, Order

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Administrator access required.', 'danger')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)

    return wrapper


@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email, is_admin=True).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))

        flash('Invalid admin credentials.', 'danger')
        return redirect(url_for('admin.admin_login'))

    return render_template('admin_login.html')


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_products = Product.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='Processing').count()
    return render_template(
        'admin/dashboard.html',
        total_products=total_products,
        total_users=total_users,
        total_orders=total_orders,
        pending_orders=pending_orders,
    )


@admin_bp.route('/products')
@login_required
@admin_required
def products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)


@admin_bp.route('/products/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_product():
    categories = Category.query.order_by(Category.name).all()
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', type=int)
        stock = request.form.get('stock', type=int)
        category_id = request.form.get('category', type=int)
        image_file = request.files.get('image')
        filename = 'default.jpg'

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)

        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            image=filename,
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', categories=categories, product=None)


@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    categories = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
        product.name = request.form.get('name', '').strip()
        product.description = request.form.get('description', '').strip()
        product.price = request.form.get('price', type=int)
        product.stock = request.form.get('stock', type=int)
        product.category_id = request.form.get('category', type=int)
        image_file = request.files.get('image')

        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            product.image = filename

        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', categories=categories, product=product)


@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product removed successfully.', 'success')
    return redirect(url_for('admin.products'))


@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('admin/categories.html', categories=categories)


@admin_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        existing = Category.query.filter_by(name=form.name.data.strip()).first()
        if existing:
            flash('Category already exists.', 'warning')
            return redirect(url_for('admin.categories'))

        category = Category(name=form.name.data.strip())
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully.', 'success')
        return redirect(url_for('admin.categories'))

    return render_template('admin/category_form.html', form=form)


@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted.', 'success')
    return redirect(url_for('admin.categories'))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/orders')
@login_required
@admin_required
def admin_orders():
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)


@admin_bp.route('/orders/<int:order_id>/status', methods=['POST'])
@login_required
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status', 'Processing')
    order.status = status
    db.session.commit()
    flash('Order status updated.', 'success')
    return redirect(url_for('admin.admin_orders'))
