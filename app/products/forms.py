from flask_wtf import Form
from wtforms import StringField,RadioField, SelectField, IntegerField, FloatField, validators


class AddProductForm(Form):
    product_name = StringField('Title:', [validators.DataRequired()])
    price = FloatField('Price:', [validators.DataRequired()])
    quantity = IntegerField('Quantity:')
    status = RadioField('Status:', choices=[('0', 'draft'), ('1', 'active'), [validators.DataRequired()]])
