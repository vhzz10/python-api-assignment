# -*- coding: utf-8 -*-

import unittest
import requests
from unittest.mock import patch
import json

from .app import BaseTestCase
from app.main import App
from app.config import SECRET_KEY, TOKEN_EXPIRES

from app.database import db_session, init_session 
from app.models import Customer
from app.middleware import auth as _token

from falcon import testing

from datetime import datetime, timedelta
import random
from faker import Faker
import jwt


CurrentTime = datetime.utcnow()


class BasicTest(BaseTestCase):

    fake = Faker()
    
    def get_valid_token(self):
        valid_token = self.token.json['data']['Token']
        return valid_token

    def gen_dob(self):
        cur_time = CurrentTime
        return datetime(random.randrange(1911,cur_time.year), random.randrange(1, 12), random.randrange(1, 28))


    # Test status code Login
    def test_login(self):
        
        # Assert that the request-response cycle completed successfully with status code 200.
        self.assertEquals(self.token.status_code, 200)

    # Test create customer success
    def test_create_success(self):
        fake_name = self.fake.name()
        dob = self.gen_dob().strftime('%Y-%m-%d')

        req_create = self.app.post_json(
                path='/customer',
                body={"dob": dob, "name": fake_name},
                params=None,
                headers={"Authorization": self.get_valid_token(), "Content-Type": "application/json"},
        )

        self.assertEquals(req_create.status_code, 200)
        self.assertDictEqual(req_create.json['data'], {'name': fake_name, 'dob': dob})

    # Test fail token
    def test_fail_token(self):
        fake_name = self.fake.name()
        dob = self.gen_dob().strftime('%Y-%m-%d')
        time_expired = CurrentTime - timedelta(seconds=TOKEN_EXPIRES * 2 + 1)
        with patch.object(_token.datetime, 'utcnow', return_value=time_expired):
            self.token = self.app.post_json(
                path='/login',
                body={"username":"test_api"},
                params=None,
                headers={"Content-Type": "application/json"},
            )
        with self.assertRaises(jwt.ExpiredSignatureError):
            req_create = self.app.post_json(
                    path='/customer',
                    body={"dob": dob, "name": fake_name},
                    params=None,
                    headers={"Authorization": self.token.json['data']['Token'], "Content-Type": "application/json"},
            )


if __name__ == "__main__":
    unittest.main()
