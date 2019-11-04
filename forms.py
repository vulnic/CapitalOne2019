from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ApiForm(FlaskForm):
    value = StringField('Value',validators=[DataRequired()])
    category = StringField('Category',validators=[DataRequired()])
    count = StringField('Count',validators=[DataRequired()])
    submit = SubmitField('Submit',validators=[DataRequired()])
    value_dropdown = SelectField(u'Value', choices = [('1001',100),('200',200),('300',300),('400',400),('500',500)], validators = [DataRequired()])
    






