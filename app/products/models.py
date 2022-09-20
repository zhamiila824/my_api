from app import db
from app.products import constants as PRODUCT


class Product(db.Model):

    __tablename__ = 'productsPositive'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(255))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    status = db.Column(db.SmallInteger, default=PRODUCT.DRAFT)

    def __int__(self, product_name=None, price=None, quantity=None):
        self.product_name = product_name
        self.price = price
        self.quantity = quantity

    def getStatus(self):
        return PRODUCT.STATUS[self.status]

    def __repr__(self):
        return '<Product: %r>' % self.product_name
