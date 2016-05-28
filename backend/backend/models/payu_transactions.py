from sqlalchemy import Column, String, ForeignKey, Boolean, Integer
from sqlalchemy.orm import relationship

from backend import db

from .utils import Entity


class PayUTransaction(db.Model, Entity):
    payu_reference = Column(Integer, unique=True, nullable=False)
    merchant_reference = Column(Integer)
    successful = Column(Boolean)
    result_message = Column(String)
    result_code = Column(String)
    display_message = Column(String)
    point_of_failure = Column(String)

    invoice_id = Column(ForeignKey('invoice.id'), nullable=False)
    invoice = relationship(
        'Invoice',
        back_populates='payu_transactions',
    )
