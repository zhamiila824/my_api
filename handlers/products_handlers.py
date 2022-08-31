from flask import request
from helpers.db_queries import show_products, get_product, add_product, search_product, delete_product


def show():
    response = show_products()
    return response


def product(product_id):
    response = get_product(product_id)
    return response


def add():
    try:
        add_product(request)
        return "Successfully saved", 201
    except Exception as e:
        return "Already exists", 208


def search():
    response = search_product(request)
    return response


def delete():
    delete_product(request)
    return "Successfully deleted"

