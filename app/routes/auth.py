from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash

from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('shop.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first():
            flash('Username or email already exists.', 'danger')
            return redirect(url_for('auth.register'))

        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower(),
            password_hash=generate_password_hash(form.password.data),
        )
        db.session.add(user)
        db.session.commit()

        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('shop.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next') or url_for('shop.home')
            return redirect(next_page)

        flash('Invalid email or password.', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('shop.home'))
