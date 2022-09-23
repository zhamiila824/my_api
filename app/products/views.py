from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for,
)
from app import db
from app.products.forms import ProductForm
from app.products.models import Product
from app.products.tables import ProductsTable


products = Blueprint("products", __name__, url_prefix="/products")


@products.route("/")
def home():
    qry = db.session.query(Product)
    products_result = qry.all()
    if not products_result:
        flash("No products found!")
        return redirect("/products/")
    table = ProductsTable(products_result)
    table.border = True
    return render_template("products/products.html", table=table)


@products.route("/add/", methods=["GET", "POST"])
def add_product():
    form = ProductForm(request.form)
    if request.method == "POST" and form.validate():
        # create product instance, but not store in database yet
        product = Product(
            product_name=form.product_name.data,
            price=form.price.data,
            quantity=form.quantity.data,
            status=form.status.data,
        )
        # insert record in database and commit
        db.session.add(product)
        db.session.commit()

        flash("Product added!")
        # redirect user to the 'home' method of user module
        return redirect(url_for("products.home"))
    return render_template("products/add_product.html", form=form)


@products.route("/<product_id>/", methods=["GET", "POST"])
def edit(product_id):
    qry = db.session.query(Product).filter(Product.id == product_id)
    product = qry.first()
    if product:
        form = ProductForm(formdata=request.form, obj=product)
        if request.method == "POST" and form.validate():
            Product.query.filter_by(id=product_id).update(
                dict(
                    id=product_id,
                    product_name=form.product_name.data,
                    price=form.price.data,
                    quantity=form.quantity.data,
                    status=form.status.data,
                )
            )
            db.session.commit()
            flash("Product updated successfully!")
            return redirect(url_for("products.edit", product_id=product_id))
        return render_template("products/edit_product.html", form=form)
    return render_template("404.html"), 404


# TODO Search product
@products.route("delete/<product_id>", methods=["GET", "POST"])
def delete(product_id):
    qry = db.session.query(Product).filter(Product.id == product_id)
    product = qry.first()
    if product:
        form = ProductForm(formdata=request.form, obj=product)
        if request.method == "POST":
            db.session.delete(product)
            db.session.commit()
            flash("Product deleted successfully!")
            return redirect("/")
        return render_template("products/delete_product.html", form=form)
    return render_template("404.html"), 404
