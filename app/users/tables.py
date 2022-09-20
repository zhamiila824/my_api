from flask_table import Table, Col, LinkCol


class UsersTable(Table):
    id = Col('Id', show=False)
    username = Col('Username')
    email = Col('Email')
    role = Col('Role')
    status = Col('Status')
    edit = LinkCol('Edit', 'users.edit', url_kwargs=dict(user_id='id'))
    delete = LinkCol('Delete', 'users.delete', url_kwargs=dict(user_id='id'))