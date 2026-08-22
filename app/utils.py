import os
from werkzeug.utils import secure_filename
from flask import current_app

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}


def save_image(file):
    filename = secure_filename(file.filename)
    if '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS:
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, filename)
        file.save(image_path)
        return filename
    return None


def format_currency(value):
    try:
        return f'₹{value:,}'
    except Exception:
        return str(value)


def get_recently_viewed(session):
    return session.get('recently_viewed', [])


def add_recently_viewed(session, product_id):
    recent = session.get('recently_viewed', [])
    if product_id in recent:
        recent.remove(product_id)
    recent.insert(0, product_id)
    session['recently_viewed'] = recent[:6]
