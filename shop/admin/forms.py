from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField,DateField, StringField, PasswordField, SubmitField,BooleanField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,InputRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password=StringField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('login')


class ProductForm(FlaskForm):
    categories = [
        ('Refrigerator', 'Refrigerator'),
        ('Audiovideo', 'Audiovideo'),
        ('AirConditioner', 'Air Conditioner'),
        ('Smartphone', 'Smartphone'),
        ('KitchenAppliances', 'Kitchen Appliances'),
        ('Pcs&Laptop', 'PCs & Laptop'),
        ('SmartHome', 'Smart Home'),
    ]

    category = SelectField('Category', choices=categories, validators=[DataRequired()])
  
    title = StringField('Product Title', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired()])
    description = TextAreaField('Product Description', validators=[DataRequired()])
    features = TextAreaField('Product Features', validators=[DataRequired()])
    submit = SubmitField('Add Product')



class CustomerForm(FlaskForm):
    active_choices = [
        (1, 'Yes'),
        (0, 'No'),
    ]

    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    registration_date = StringField('Registration Date', validators=[DataRequired()])
    last_login = StringField('Last Login', validators=[DataRequired()])
    is_active = SelectField('Active', choices=active_choices, validators=[DataRequired()])
    submit = SubmitField('Submit')



class OrderForm(FlaskForm):
    customer_id = IntegerField('Customer ID', validators=[InputRequired()])
    order_date = DateField('Order Date',validators=[InputRequired()])
    total_amount = DecimalField('Total Amount', validators=[InputRequired()])
    order_status = StringField('Order Status', validators=[InputRequired()])
    payment_method = SelectField('Payment Method', choices=[('Credit Card', 'Credit Card'), ('Cash on Delivery', 'Cash on Delivery'), ('Online Transfer', 'Online Transfer'), ('PayPal', 'PayPal')])

class OrderDetailForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[InputRequired()])
    quantity = IntegerField('Quantity', validators=[InputRequired()])
    price_per_unit = DecimalField('Price per Unit', validators=[InputRequired()])
    subtotal = DecimalField('Subtotal', validators=[InputRequired()])