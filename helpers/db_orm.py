import json
import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy import MetaData, Table, Column, Integer, VARCHAR, REAL, BOOLEAN

engine = create_engine("sqlite+pysqlite:///../testDB", echo=True, future=True)
metadata_obj = MetaData()
products_table = Table(
    "productsPositive",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('product_name', VARCHAR(255)),
    Column('price', REAL),
    Column('quantity', Integer),
    Column('active', BOOLEAN)
)
metadata_obj.create_all(engine)
products_table.c.name
# conn = sqlite3.connect("testDB", check_same_thread=False)
# cursor = conn.cursor()

#
# def show_products():
#     resp = []
#     for i in cursor.execute("""SELECT * FROM productsPositive""").fetchall():
#         resp.append({
#             "id": i[0],
#             "product_name": i[1],
#             "price": i[2],
#             "quantity": i[3],
#             "active": i[4]
#         })
#     return resp
#
#
# def get_product(product_id):
#     resp = []
#     for i in cursor.execute("""SELECT * FROM productsPositive WHERE id='{}'""".format(product_id)).fetchall():
#         resp.append({
#             "id": i[0],
#             "product_name": i[1],
#             "price": i[2],
#             "quantity": i[3],
#             "active": i[4]
#         })
#     return resp
#
#
# def add_product(request):
#     req = json.loads(request.data)
#     (id, product_name, price, quantity, active) = (req['id'],
#                                                    req['product_name'],
#                                                    req['price'],
#                                                    req['quantity'],
#                                                    req['active'])
#     cursor.execute("""INSERT INTO productsPositive
#               VALUES ('{id}', '{product_name}', '{price}', '{quantity}',
#               '{active}')""".format(id=id, product_name=product_name, price=price, quantity=quantity, active=active))
#     conn.commit()
#
#
# def search_product(request):
#     req = json.loads(request.data)
#     resp = []
#     for i in cursor.execute("""SELECT * FROM productsPositive WHERE product_name LIKE '%{}%'""".format(
#             req['product_name'])).fetchall():
#         resp.append({
#             "id": i[0],
#             "product_name": i[1],
#             "price": i[2],
#             "quantity": i[3],
#             "active": i[4]
#         })
#     return resp
#
#
# def delete_product(request):
#     req = json.loads(request.data)
#     cursor.execute("""DELETE FROM productsPositive WHERE id = '{}'""".format(req['id']))
#     conn.commit()
