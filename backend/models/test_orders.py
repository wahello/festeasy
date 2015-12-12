from backend import db
from backend.models import Order
from backend.testing import ModelTestCase


class TestOrder(ModelTestCase):
    def test_order_total_rands(self):
        """ Test that Order.total_rands is equal to the sum
        of all OrderProduct.sub_total_rands for an Order.
        """
        festival = self.create_festival(
            pre_populate=True,
            name='test',
            base_festival=self.create_base_festival(),
        )
        price = 10
        product_1 = self.create_product(
            create_valid_product=True,
            product_prices=[
                self.create_product_price(
                    amount_rands=price,
                )
            ],
        )
        product_2 = self.create_product(
            create_valid_product=True,
            product_prices=[
                self.create_product_price(
                    amount_rands=price,
                )
            ],
        )
        db.session.add(product_1)
        db.session.add(product_2)
        db.session.commit()
        user = self.create_user(
            normal_user=True,
            with_cart=True
        )
        order = self.create_order(
            festival=festival,
            user=user,
        )
        order_product_1 = self.create_order_product(
            unit_price_rands=product_1.price_rands,
            order=order,
            product=product_1,
        )
        order_product_2 = self.create_order_product(
            unit_price_rands=product_2.price_rands,
            order=order,
            product=product_2,
        )
        db.session.add(user)
        db.session.commit()
        fetched_order = Order.query.one()
        self.assertEqual(fetched_order.total_rands, price * 2)

    def test_from_cart(self):
        """ Test that Order.from_cart creates an order
        from a Cart.
        """
        user = self.create_user(normal_user=True, with_cart=True)
        product = self.create_product(
            create_valid_product=True,
            product_prices=[
                self.create_product_price(
                    amount_rands=11,
                )
            ],
        )
        festival = self.create_festival(
            pre_populate=True,
            name='qwe',
            base_festival=self.create_base_festival(),
        )
        user.cart.festival = festival
        user.cart.products.append(product)
        db.session.add(user)
        db.session.commit()
        order = Order.from_cart(user.cart)
        db.session.add(order)
        db.session.commit()
        self.assertEqual(order.total_rands, 11)
        self.assertEqual(order.products, [product])
