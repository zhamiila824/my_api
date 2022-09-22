from flask import Flask, request
import json
import sqlite3

app = Flask(__name__)
conn = sqlite3.connect("testDB", check_same_thread=False)
cursor = conn.cursor()


@app.route("/", methods=["GET"])
def print_all():
    resp = []
    for i in cursor.execute("""SELECT * FROM productsPositive""").fetchall():
        resp.append(
            {
                "id": i[0],
                "product_name": i[1],
                "price": i[2],
                "quantity": i[3],
                "active": i[4],
            }
        )
    return resp


@app.route("/<id>", methods=["GET"])
def show(id):
    resp = []
    for i in cursor.execute(
        """SELECT * FROM productsPositive WHERE id='{}'""".format(id)
    ).fetchall():
        resp.append(
            {
                "id": i[0],
                "product_name": i[1],
                "price": i[2],
                "quantity": i[3],
                "active": i[4],
            }
        )
    return (resp,)


@app.route("/add", methods=["POST"])
def add():
    try:
        req = json.loads(request.data)
        cursor.execute(
            """INSERT INTO productsPositive
              VALUES ('{id}', '{product_name}', '{price}', '{quantity}',
              '{active}')""".format(
                id=req["id"],
                product_name=req["product_name"],
                price=req["price"],
                quantity=req["quantity"],
                active=req["active"],
            )
        )
        conn.commit()
        return "Successfully saved", 201
    except Exception as e:
        return "Already exists", 208


@app.route("/search", methods=["GET"])
def search():
    req = json.loads(request.data)
    resp = []
    for i in cursor.execute(
        """SELECT * FROM productsPositive WHERE product_name LIKE '%{}%'""".format(
            req["product_name"]
        )
    ).fetchall():
        resp.append(
            {
                "id": i[0],
                "product_name": i[1],
                "price": i[2],
                "quantity": i[3],
                "active": i[4],
            }
        )
    return resp


app.run()
