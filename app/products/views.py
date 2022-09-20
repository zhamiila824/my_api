from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app import db
from app.products.forms import ProductForm
from app.products.models import Product
from app.products.tables import ProductsTable


products = Blueprint('products', __name__, url_prefix='/products')


@products.route("/")
def all_products():
    qry = db.session.query(Product)
    products_result = qry.all()
    if not products_result:
        flash('No products found!')
        return redirect('/products/')
    table = ProductsTable(products_result)
    table.border = True
    return render_template('products/products.html', table=table)


@products.route('/add/', methods=['GET', 'POST'])
def add_product():
    form = ProductForm(request.form)

    print('here')
    if request.method == 'POST' and form.validate():
        product = Product(product_name=form.product_name.data, price=form.price.data,
                          quantity=form.quantity.data, status=form.status.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added')
        return redirect(url_for('products.all_products'))
    print('here')
    return render_template("products/add_product.html", form=form)
# TODO Edit product
# TODO Search product
# TODO Delete product
