from flask import Flask
from handlers.products_handlers import show, search, add, product, delete


app = Flask(__name__)
app.add_url_rule("/", view_func=show)
app.add_url_rule("/<product_id>", view_func=product)
app.add_url_rule("/add", methods=["POST"], view_func=add)
app.add_url_rule("/search", view_func=search)
app.add_url_rule("/delete", methods=["DELETE"], view_func=delete)

app.run()
