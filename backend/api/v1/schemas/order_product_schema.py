from marshmallow import fields

from backend.api.utils import EntitySchema
from .order_schema import OrderSchema
from .product_schema import ProductSchema


class OrderProductSchema(EntitySchema):
    unit_price_rands = fields.Float()
    order = fields.Nested(OrderSchema)
    product = fields.Nested(ProductSchema)

    class Meta:
        strict = True
