from sqlalchemy import Column, Integer, Numeric
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, column_property

from backend import db
from backend.models import Entity


class OrderProduct(db.Model, Entity):
    __tablename__ = 'order_product'

    def __init__(self, unit_price_rands=None, quantity=None,
            order=None, product=None):
        self.unit_price_rands = unit_price_rands
        self.quantity = quantity
        self.order = order
        self.product = product

    def __repr__(self):
        return '<OrderProduct {id}>'.format(id=self.id)

    unit_price_rands = Column(Numeric, nullable=False)
    quantity = Column(Integer, nullable=False)

    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    order = relationship(
        'Order',
        back_populates='order_products',
        cascade='save-update, merge'
    )

    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship(
        'Product',
        back_populates='order_products',
        cascade='save-update, merge'
    )

    sub_total_rands = column_property(
        unit_price_rands * quantity
    )

    __table_args__ = (
        UniqueConstraint('order_id', 'product_id'),
    )