from flask import url_for

from backend import db
from backend.testing import APITestCase


endpoint = 'v1.festivalsingleton'


class TestFestivalSingleton(APITestCase):
    def test_get(self):
        festival = self.create_festival(
            pre_populate=True,
            base_festival=self.create_base_festival(),
        )
        db.session.add(festival)
        db.session.commit()
        response = self.api_request(
            'get',
            url_for(endpoint, festival_id=festival.id),
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], festival.id)

    def test_patch(self):
        new_name = 'aaa'
        festival = self.create_festival(
            pre_populate=True,
            name='bbb',
            base_festival=self.create_base_festival(),
        )
        db.session.add(festival)
        db.session.commit()
        response = self.api_request(
            'patch',
            url_for(endpoint, festival_id=festival.id),
            data=dict(
                name=new_name,
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], new_name)
