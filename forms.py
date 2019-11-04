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

class SearchCategoryForm(FlaskForm):
    category = StringField('Category',validators=[DataRequired()])
    submit = SubmitField('Submit')

class QuestionForm(FlaskForm):
    value_dropdown = SelectField('Value', choices = [('100',100),('200',200),('300',300),('400',400),('500',500),('600',600),('700',700),('800',800),('900',900),('1000',1000)])
    submit = SubmitField('Submit')

class ApiForm(FlaskForm):
    category = StringField('Category',validators=[DataRequired()])
    #value_dropdown = SelectField(u'Value', choices = [('100',100),('200',200),('300',300),('400',400),('500',500)])
    count = StringField('Count')
    submit = SubmitField('Submit')



