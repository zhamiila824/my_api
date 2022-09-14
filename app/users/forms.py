from flask_wtf import Form
from wtforms import EmailField, StringField, PasswordField, BooleanField, \
    RadioField, SelectField, SelectMultipleField, validators


class LoginForm(Form):
    email = EmailField('Email:', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password:', [validators.DataRequired()])


class RegisterForm(Form):
    username = StringField('Username:', [validators.DataRequired()])
    email = EmailField('Email:', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password:', [validators.DataRequired()])
    confirm = PasswordField('Repeat Password:', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    accept_tou = BooleanField('I agree to Terms of Use', [validators.DataRequired()])

class UserEditForm(Form):
    username = StringField('Username:', [validators.DataRequired()])
    email = EmailField('Email:', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Password:', [validators.DataRequired()])
    confirm = PasswordField('Repeat Password:', [
        validators.DataRequired(),
        validators.EqualTo('password', message='Passwords must match')
    ])
    role = RadioField('Role:', choices=[('0','admin'),('1','staff'),('2','user')])
    status = RadioField('Status:', choices=[('0','inactive'),('1','new'),('2','active')])

class UserSearchForm(Form):
    choices = [('role', 'role'),
               ('status', 'status')]
    roleChoices = [('0', 'admin'),
                   ('1', 'staff'),
                   ('2', 'user')]
    statusChoices = [('0', 'inactive'),
                     ('1', 'new'),
                     ('2', 'active')]
    select = SelectField('Search for users:', choices=choices)
    search = SelectMultipleField('')

