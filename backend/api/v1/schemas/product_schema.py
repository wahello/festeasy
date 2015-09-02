from marshmallow import fields

from backend.api.utils import EntitySchema


class ProductSchema(EntitySchema):
    name = fields.String()
    price_rands = fields.Float()
    cost_rands = fields.Float()

    class Meta:
        strict = True
