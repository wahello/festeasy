import datetime

from backend import db
from backend.models import Event, User, Order
from backend.models import Cart
from backend.utils import ModelTestCase


class TestOrder(ModelTestCase):
    def test_create_order(self):
        """ Test that an Order can be created.
        """
        
        event = self.create_event(name='test')
        user = self.create_user()
        order = self.create_order(user=user, event=event)
        db.session.add(order)
        db.session.commit()

        fetched_order = Order.query.one()
        self.assertEqual(fetched_order, order)

    def test_order_deletion_keeps_users_and_events(self):
        """ Test that deleting an Order which has 
        users does not delete those users.
        """
        event = self.create_event(name='test')
        order = self.create_order(event=event)
        user = self.create_user(orders=[order])
        db.session.add(user)
        db.session.commit()

        self.assertEqual(User.query.one(), user)
        self.assertEqual(User.query.one().orders, [order])

        db.session.delete(order)
        db.session.commit()

        self.assertIsNone(Order.query.first())

        self.assertEqual(User.query.one(), user)
        self.assertEqual(User.query.one().orders, list())

        self.assertEqual(Event.query.one(), event)

