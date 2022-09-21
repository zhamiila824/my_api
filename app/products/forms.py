from flask_wtf import Form
from wtforms import StringField, RadioField, SelectField, IntegerField, FloatField, validators


class ProductForm(Form):
    product_name = StringField('Title:', [validators.DataRequired()])
    price = FloatField('Price:', [validators.DataRequired()])
    quantity = IntegerField('Quantity:', [validators.DataRequired()])
    status = RadioField('Status:', [validators.DataRequired()], choices=[('0', 'draft'), ('1', 'active')])
