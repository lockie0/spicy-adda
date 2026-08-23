from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import LoginForm, RegistrationForm
from app.services.auth import authenticate_user, register_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/account', methods=['GET', 'POST'])
def account():
    if current_user.is_authenticated:
        return redirect(url_for('employee.dashboard'))

    mode = request.args.get('mode', 'register')
    registration_form = RegistrationForm()
    login_form = LoginForm()

    if mode == 'login':
        if login_form.validate_on_submit():
            user = authenticate_user(login_form.email.data, login_form.password.data)
            if user:
                login_user(user)
                return redirect(request.args.get('next') or url_for('employee.dashboard'))
            flash('Invalid email or password.', 'danger')
        return render_template('account.html', mode='login', registration_form=registration_form, login_form=login_form)

    if registration_form.validate_on_submit():
        try:
            register_user(
                registration_form.username.data,
                registration_form.designation.data,
                registration_form.email.data,
                registration_form.password.data,
            )
        except ValueError as error:
            flash(str(error), 'danger')
        else:
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('auth.account', mode='login'))

    return render_template('account.html', mode='register', registration_form=registration_form, login_form=login_form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return redirect(url_for('auth.account', mode='register'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return redirect(url_for('auth.account', mode='login', next=request.args.get('next')))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('shop.home'))
