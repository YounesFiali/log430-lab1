from daos.product_dao import ProductDAO
from models.product import Product

dao = ProductDAO()

def setup_function():
    dao.delete_all()


def test_product_select():
    product = Product(None, 'iPhone 14', 'Apple', 999.99)
    dao.insert(product)
    product_list = dao.select_all()
    assert len(product_list) >= 1
        
def test_product_insert():
    product = Product(None, 'iPhone 14', 'Apple', 999.99)
    dao.insert(product)
    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert product.name in names

def test_product_update():
    product = Product(None, 'Pixel 8', 'Google', 699.99)
    assigned_id = dao.insert(product)
    product.id = assigned_id
    product.price = 599.99
    dao.update(product)
    product_list = dao.select_all()
    prices = [p.price for p in product_list]
    assert float(product.price) in [float(p.price) for p in product_list]    
    dao.delete(assigned_id)

def test_product_delete():
    product = Product(None, 'Pixel 8', 'Google', 699.99)
    assigned_id = dao.insert(product)
    dao.delete(assigned_id)
    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert product.name not in names