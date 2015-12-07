from flask import url_for

from backend import db
from backend.testing import APITestCase


endpoint = 'v1.invoicesingleton'


class TestInvoiceSingleton(APITestCase):
    def test_get(self):
        invoice = self.create_invoice(
            order=self.create_order(
                festival=self.create_festival(
                    name='asd',
                    base_festival=self.create_base_festival(),
                ),
                user=self.create_user(normal_user=True, with_cart=True)
            ),
        )
        db.session.add(invoice)
        db.session.commit()
        response = self.api_request(
            'get',
            url_for(endpoint, invoice_id=invoice.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], invoice.id)
