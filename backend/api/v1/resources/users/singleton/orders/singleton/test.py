from flask import url_for

from backend import db
from backend.testing import APITestCase


endpoint = 'v1.userordersingleton'


class TestUserOrderSingleton(APITestCase):
    def test_get(self):
        user = self.create_user(normal_user=True, with_cart=True)
        order = self.create_order(
            event=self.create_event(name='asdf'),
            user=user,
        )
        db.session.add(order)
        db.session.add(user)
        db.session.commit()
        response = self.api_request(
            'get',
            url_for(endpoint, user_id=user.id, order_id=order.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], order.id)
