from werkzeug.security import generate_password_hash

from app import db
from app.models import User
from app.utils import get_company_from_email


def normalize_email(email):
    return email.strip().lower()


def register_user(username, designation, email, password):
    username = username.strip()
    email = normalize_email(email)
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existing_user:
        raise ValueError('Username or email already exists.')

    user = User(
        username=username,
        designation=designation,
        email=email,
        company=get_company_from_email(email),
        password_hash=generate_password_hash(password),
    )
    db.session.add(user)
    db.session.commit()
    return user


def authenticate_user(email, password):
    user = User.query.filter_by(email=normalize_email(email)).first()
    if user and user.check_password(password):
        return user
    return None
