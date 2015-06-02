import datetime
from flask.ext.testing import TestCase

from backend import create_app, db
from backend.utils.random_string import random_string
from backend.models import User, Session, Product
from backend.models import Event, Order, Cart
from backend.models import OrderProduct, CartProduct


class GeneralTestCase(TestCase):
    def create_app(self):
        app = create_app(config='testing')
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_cart_product(self, cart=None, product=None,
        quantity=None):
        cart_product = CartProduct(cart=cart, product=product, quantity=quantity)
        return cart_product

    def create_order_product(self, order=None, product=None,
        unit_price_rands=None, quantity=None):
        order_product = OrderProduct(order=order, product=product,
            unit_price_rands=unit_price_rands, quantity=quantity)
        return order_product

    def create_order(self, event=None, user=None, products=[]):
        order = Order(event=event, user=user, products=products)
        return order

    def create_event(self, name=None, users=[]):
        event = Event(name=name, users=users)
        return event

    def create_product(self, name=None, cost_rands=-1, price_rands=None):
        product = Product(name=name, cost_rands=cost_rands, price_rands=price_rands)
        return product

    def create_session(self, expires_on=None, token=None, user=None, create_valid_session=False):
        now = datetime.datetime.now()
        if create_valid_session:
            expires_on = now + datetime.timedelta(seconds=30)
            token = random_string(25)
        session = Session(expires_on=expires_on, user=user, token=token)
        return session

    def create_user(self, email_address='user@GeneralTestCase.takenote', 
        password='test_password', first_name='Johannes', create_valid_session=False, create_cart=True, orders=[]):
        now = datetime.datetime.now()
        user = User(email_address=email_address, password=password, first_name=first_name, orders=orders)
        if create_valid_session:
            expires_on = now + datetime.timedelta(seconds=30)
            token = random_string(25)
            session = self.create_session(expires_on=expires_on, token=token)
            user.sessions.append(session)
        if create_cart:
            user.cart = Cart()
        return user
