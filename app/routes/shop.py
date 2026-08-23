from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_required
from app import db
from app.forms import SearchForm, ReviewForm, ContactForm
from app.models import Product, Category, Review, WishlistItem, ContactMessage, Subscriber
from app.utils import COMBO_ITEMS, SHOP_CATEGORIES, OFFER_CATALOG, add_recently_viewed, get_recently_viewed

shop_bp = Blueprint('shop', __name__)


def build_search_form(sort_by='newest'):
    categories = Category.query.order_by(Category.name).all()
    form = SearchForm(meta={'csrf': False})
    form.category.choices = [(0, 'All Categories')] + [(category.id, category.name) for category in categories]
    form.sort.data = sort_by
    return form, categories


@shop_bp.route('/')
def home():
    categories = Category.query.order_by(Category.name).all()
    latest = Product.query.order_by(Product.created_at.desc()).limit(8).all()
    featured = Product.query.order_by(Product.price.asc()).limit(6).all()
    popular = Product.query.order_by(Product.stock.desc()).limit(6).all()
    recently = []
    for product_id in get_recently_viewed(session):
        product = Product.query.get(product_id)
        if product:
            recently.append(product)
    return render_template('home.html', categories=categories, latest=latest, featured=featured, popular=popular, recently=recently)


@shop_bp.route('/products')
def products():
    query = request.args.get('q', '').strip()
    category_filter = request.args.get('category', 'all').strip().lower() or 'all'
    if category_filter.isdigit():
        selected_category = Category.query.get(int(category_filter))
        category_filter = selected_category.name.lower().replace(' ', '-') if selected_category else 'all'
    sort_by = request.args.get('sort', 'newest')
    page = request.args.get('page', 1, type=int)

    products_query = Product.query
    if query:
        products_query = products_query.join(Category).filter(
            Product.name.ilike(f'%{query}%') |
            Product.description.ilike(f'%{query}%') |
            Category.name.ilike(f'%{query}%')
        )
    if category_filter == 'menu':
        products_query = products_query.join(Category).filter(Category.name != 'Combos')
    elif category_filter == 'combos':
        products_query = products_query.join(Category).filter(Category.name == 'Combos')
    elif category_filter == 'offers':
        products_query = products_query.filter(Product.id == -1)
    elif category_filter in {'snacks', 'chaat', 'beverages', 'street-food', 'sweets'}:
        category_name = category_filter.replace('-', ' ').title()
        products_query = products_query.join(Category).filter(Category.name == category_name)

    if sort_by == 'price_asc':
        products_query = products_query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        products_query = products_query.order_by(Product.price.desc())
    else:
        products_query = products_query.order_by(Product.created_at.desc())

    products = products_query.paginate(page=page, per_page=12, error_out=False)
    form, categories = build_search_form(sort_by=sort_by)
    product_images = {product.name: product.image for product in Product.query.all()}
    return render_template('products.html', products=products, categories=categories, category_options=SHOP_CATEGORIES, offers=OFFER_CATALOG, combo_items=COMBO_ITEMS, product_images=product_images, query=query, selected_category=category_filter, sort_by=sort_by, form=form)


@shop_bp.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    review_form = ReviewForm()
    categories = Category.query.order_by(Category.name).all()
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()

    add_recently_viewed(session, product.id)

    if review_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Please log in to submit a review.', 'warning')
            return redirect(url_for('auth.login'))

        review = Review(
            user_id=current_user.id,
            product_id=product.id,
            rating=int(review_form.rating.data),
            comment=review_form.comment.data.strip(),
        )
        db.session.add(review)
        db.session.commit()
        flash('Review submitted successfully.', 'success')
        return redirect(url_for('shop.product_detail', product_id=product.id))

    return render_template('product_detail.html', product=product, categories=categories, reviews=reviews, review_form=review_form)


@shop_bp.route('/wishlist')
@login_required
def wishlist():
    items = WishlistItem.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', items=items)


@shop_bp.route('/wishlist/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_wishlist(product_id):
    product = Product.query.get_or_404(product_id)
    existing = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
    if existing:
        flash('Product is already in your wishlist.', 'info')
    else:
        item = WishlistItem(user_id=current_user.id, product_id=product.id)
        db.session.add(item)
        db.session.commit()
        flash('Added to wishlist.', 'success')
    return redirect(request.referrer or url_for('shop.product_detail', product_id=product_id))


@shop_bp.route('/wishlist/remove/<int:product_id>', methods=['POST'])
@login_required
def remove_from_wishlist(product_id):
    item = WishlistItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        flash('Removed from wishlist.', 'success')
    return redirect(url_for('shop.wishlist'))


@shop_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        message = ContactMessage(
            user_id=current_user.id if current_user.is_authenticated else None,
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            subject='Customer Inquiry',
            message=form.message.data.strip(),
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent. Our team will contact you shortly.', 'success')
        return redirect(url_for('shop.contact'))
    return render_template('contact.html', form=form)


@shop_bp.route('/faq')
def faq():
    return render_template('faq.html')


@shop_bp.route('/about')
def about():
    return render_template('about.html')


@shop_bp.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email', '').strip().lower()
    if not email:
        flash('Please enter a valid email address.', 'danger')
        return redirect(request.referrer or url_for('shop.home'))

    existing = Subscriber.query.filter_by(email=email).first()
    if existing:
        flash('You are already subscribed.', 'info')
    else:
        subscriber = Subscriber(email=email)
        db.session.add(subscriber)
        db.session.commit()
        flash('Subscribed to the newsletter successfully.', 'success')
    return redirect(request.referrer or url_for('shop.home'))
