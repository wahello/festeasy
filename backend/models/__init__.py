import datetime
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime

from backend import db


class Dumpable(object):
    whitelist = []
    def dump(self):
        return {attr: getattr(self, attr) 
            for attr in self.whitelist}

class Entity(object):
    id = Column(Integer, primary_key=True)
    created_on = Column(DateTime, default=datetime.datetime.now, 
        nullable=False)

# All the models
from sessions import Session
from users import User
from products import Product
from events import Event
from orders import Order
from order_products import OrderProduct
from carts import Cart
from cart_products import CartProduct
from invoices import Invoice
from invoice_products import InvoiceProduct
