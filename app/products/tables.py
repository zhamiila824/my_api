from flask_table import Table, Col, LinkCol


class ProductsTable(Table):
    id = Col('Id', show=False)
    product_name = Col('Title')
    price = Col('Price')
    quantity = Col('Quantity')
    status = Col('Status')
    # edit = LinkCol('Edit', 'products.edit', url_kwargs=dict(product_id='id'))
    # delete = LinkCol('Delete', 'products.delete', url_kwargs=dict(product_id='id'))
