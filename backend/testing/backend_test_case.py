import datetime
from flask.ext.testing import TestCase

from backend import create_app, db
from backend.models import User, Session, Product
from backend.models import Festival, Order, Cart, Invoice
from backend.models import OrderProduct, CartProduct
from backend.models import Payment, InvoiceProduct, Category
from backend.testing.utils import template_entity


class BackendTestCase(TestCase):
    def create_app(self):
        app = create_app(config='testing')
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_category(self, *args, **kwargs):
        category = Category(*args, **kwargs)
        return category

    def create_cart(self, *args, **kwargs):
        cart = Cart(*args, **kwargs)
        return cart

    def create_payment(self, *args, **kwargs):
        payment = Payment(*args, **kwargs)
        return payment

    def create_invoice(self, *args, **kwargs):
        invoice = Invoice(*args, **kwargs)
        return invoice

    def create_invoice_product(self, *args, **kwargs):
        invoice_product = InvoiceProduct(*args, **kwargs)
        return invoice_product

    def create_cart_product(self, *args, **kwargs):
        cart_product = CartProduct(*args, **kwargs)
        return cart_product

    def create_order_product(self, *args, **kwargs):
        order_product = OrderProduct(*args, **kwargs)
        return order_product

    def create_order(self, *args, **kwargs):
        order = Order(*args, **kwargs)
        return order

    def create_festival(self, *args, pre_populate=False, **kwargs):
        if pre_populate:
            template = {
                'name': 'My Festival',
            }
            kwargs = template_entity(template, kwargs)
        festival = Festival(*args, **kwargs)
        return festival

    def create_product(self, *args, create_valid_product=None, **kwargs):
        if create_valid_product:
            product_template = {
                'name': 'Auto Product',
                'price_rands': 999.12345,
                'cost_rands': 88.12345
            }
            #kwargs = dict(chain(product_template.items(), kwargs.items()))
            kwargs = template_entity(product_template, kwargs)
        product = Product(*args, **kwargs)
        return product

    def create_session(self, *args, valid_session=False, **kwargs):
        now = datetime.datetime.now()
        if valid_session:
            session_template = {
                'expires_on': now,
            }
            kwargs = template_entity(session_template, kwargs)
        session = Session(*args, **kwargs)
        if valid_session:
            session.generate_token()
        return session

    def create_user(self, *args, normal_user=False,
            valid_session=False, with_cart=False, **kwargs):
        now = datetime.datetime.now()
        if normal_user:
            user_template = {
                'email_address': 'auto-test@festeasy.co.za',
                'password': 'autotest_password',
                'first_name': 'autotest_first_name',
            }
            kwargs = template_entity(user_template, kwargs)
        user = User(*args, **kwargs)

        if valid_session:
            expires_on = now + datetime.timedelta(seconds=30)
            session = self.create_session(
                expires_on=expires_on,
                user=user,
            )
            session.generate_token()
            user.sessions.append(session)
        if with_cart:
            user.cart = Cart()
        return user
