# -*- coding: utf-8 -*-

import unittest
from unittest.mock import patch
import copy

from falcon.testing.client import TestClient

from app.main import App

from app.middleware import DatabaseSession, AuthMiddleware, LoginResource, JSONTranslator
from app.database import db_session, init_session
from app.api import Collection, Item

from app.models import Customer
import json
from datetime import datetime, timedelta

CurrentTime = datetime.utcnow()

class BaseTestCase(unittest.TestCase):

    datetime_patch = patch('app.middleware.auth.datetime')

    def setUp(self):

        self.app = TestApp(App)
        self.token = self.app.post_json(
                path='/login',
                body={"username":"test_api"},
                params=None,
                headers={"Content-Type": "application/json"},
            )
        self.dt = self.datetime_patch.start()
        self.dt.utcnow.return_value = CurrentTime
    
    def tearDown(self):
        self.datetime_patch.stop() 

class TestApp(object):

    def __init__(self, api_class):
        middleware = [AuthMiddleware(), JSONTranslator(), DatabaseSession(db_session)]
        self.app = api_class(middleware=middleware)
        self.client = TestClient(self.app)
        

    def get_headers(self, headers):
        all_headers = {}

        if headers:
            all_headers.update(copy.deepcopy(headers))

        return all_headers

    def get(self, path, params=None, headers=None):
        return self.client.simulate_get(
            path,
            params=params,
            headers=self.get_headers(headers)
        )

    def post(self, path, body=None, params=None, headers=None):
        return self.client.simulate_post(
            path,
            body=body,
            params=params,
            headers=self.get_headers(headers)
        )

    def post_json(self, path, body, params=None, headers=None):
        return self.post(path, json.dumps(body), params, headers)