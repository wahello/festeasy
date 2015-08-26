import json
from flask import url_for

from backend import db
from backend.models import User, Product, Invoice
from backend.testing import APITestCase


class TestGetUserInvoices(APITestCase):
    def test_get_user_invoices_returns_user_invoice(self):
        """ Test that v1.get_user_invoice returns a users
        invoices.
        """
        user = self.create_user(normal_user=True, valid_session=True, with_cart=True)
        product = self.create_product(create_valid_product=True)
        product_2 = self.create_product(create_valid_product=True)
        event = self.create_event(name='asd')
        user.cart.products.append(product)
        user.cart.products.append(product_2)
        user.cart.event = event
        
        order = self.create_order()
        order.from_cart(user.cart)

        invoice = self.create_invoice()
        invoice.from_order(order)

        db.session.add(invoice)
        db.session.add(user)
        db.session.commit()

        response = self.api_request('get',
            url_for('v1.get_user_invoice', user_id=user.id, invoice_id=invoice.id),
            as_user=user,
            with_session=user.sessions[0],
        )
        self.assertIsNotNone(response.json['invoice'])
        self.assertEqual(response.json['invoice']['id'], 1)
