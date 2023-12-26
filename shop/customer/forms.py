from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField,DateField, StringField, PasswordField, SubmitField,BooleanField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo,InputRequired

class CustomerRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class CustomerLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password=StringField('Password',validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('login')
