import json
import sqlite3

conn = sqlite3.connect("testDB", check_same_thread=False)
cursor = conn.cursor()


def show_products():
    resp = []
    for i in cursor.execute("""SELECT * FROM productsPositive""").fetchall():
        resp.append({
            "id": i[0],
            "product_name": i[1],
            "price": i[2],
            "quantity": i[3],
            "active": i[4]
        })
    return resp


def get_product(product_id):
    resp = []
    for i in cursor.execute("""SELECT * FROM productsPositive WHERE id='{}'""".format(product_id)).fetchall():
        resp.append({
            "id": i[0],
            "product_name": i[1],
            "price": i[2],
            "quantity": i[3],
            "active": i[4]
        })
    return resp


def add_product(request):
    req = json.loads(request.data)
    (id, product_name, price, quantity, active) = (req['id'],
                                                   req['product_name'],
                                                   req['price'],
                                                   req['quantity'],
                                                   req['active'])
    cursor.execute("""INSERT INTO productsPositive
              VALUES ('{id}', '{product_name}', '{price}', '{quantity}',
              '{active}')""".format(id=id, product_name=product_name, price=price, quantity=quantity, active=active))
    conn.commit()


def search_product(request):
    req = json.loads(request.data)
    resp = []
    for i in cursor.execute("""SELECT * FROM productsPositive WHERE product_name LIKE '%{}%'""".format(
            req['product_name'])).fetchall():
        resp.append({
            "id": i[0],
            "product_name": i[1],
            "price": i[2],
            "quantity": i[3],
            "active": i[4]
        })
    return resp


def delete_product(request):
    req = json.loads(request.data)
    cursor.execute("""DELETE FROM productsPositive WHERE id = '{}'""".format(req['id']))
    conn.commit()
