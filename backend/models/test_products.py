import datetime

from backend import db
from backend.models import Product, User
from backend.models import UserCartProduct
from backend.utils import ModelTestCase


class TestProduct(ModelTestCase):
    def test_create_product(self):
        """ Test that a product can be created.
        """
        product = self.create_product(name='test_product', price_rands=99)
        db.session.add(product)
        db.session.commit()

        fetched_product = Product.query.one()
        self.assertEqual(fetched_product, product)

    def test_product_deletion_leaves_users(self):
        """ Test that deleting a product which has 
        cart_users does not delete those users.
        """
        user = self.create_user()
        product = self.create_product(name='test_product', price_rands=99, cart_users=[user])
        db.session.add(product)
        db.session.commit()

        self.assertEqual(User.query.one(), user)
        self.assertEqual(UserCartProduct.query.one().user, user)

        db.session.delete(product)
        db.session.commit()

        self.assertEqual(User.query.one(), user)
        self.assertEqual(UserCartProduct.query.all(), list())
        self.assertEqual(Product.query.all(), list())

