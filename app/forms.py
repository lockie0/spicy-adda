from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Admin Login')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[Optional(), Length(max=140)])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    sort = SelectField('Sort by', choices=[('newest', 'Newest'), ('price_asc', 'Price low to high'), ('price_desc', 'Price high to low')])
    submit = SubmitField('Find')


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=800)])
    price = IntegerField('Price (₹)', validators=[DataRequired(), NumberRange(min=1)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    image = FileField('Product Image', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'svg', 'gif'], 'Images only')])
    submit = SubmitField('Save Product')


class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Save Category')


class CheckoutForm(FlaskForm):
    address = TextAreaField('Shipping Address', validators=[DataRequired(), Length(min=10, max=255)])
    payment_method = SelectField('Payment Method', choices=[('razorpay', 'Razorpay Placeholder'), ('stripe', 'Stripe Placeholder')], validators=[DataRequired()])
    submit = SubmitField('Place Order')


class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[('5', '5 Stars'), ('4', '4 Stars'), ('3', '3 Stars'), ('2', '2 Stars'), ('1', '1 Star')], validators=[DataRequired()])
    comment = TextAreaField('Review', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Review')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Send Message')


class SubscribeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField('Subscribe')
