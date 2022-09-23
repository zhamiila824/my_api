from flask_table import Table, Col, LinkCol
from app.users.constants import STATUS, ROLE
from app.users.models import User


class UsersTable(Table):
    id = Col("Id", show=False)
    username = Col("Username")
    email = Col("Email")
    role = Col("Role")
    status = Col("Status")
    edit = LinkCol("Edit", "users.edit", url_kwargs=dict(user_id="id"))
    delete = LinkCol("Delete", "users.delete", url_kwargs=dict(user_id="id"))
