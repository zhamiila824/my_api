from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for
from app import db
from app.products.forms import AddProductForm
from app.products.models import Products
from app.users.decorators import requires_login

products = Blueprint('products', __name__, url_prefix='/products')


