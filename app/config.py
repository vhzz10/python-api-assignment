# -*- coding: utf-8 -*-

# TOKEN
SECRET_KEY = "wV7BGdgauWIRbZQHKDKb3keE_BXObJ3"
TOKEN_EXPIRES = 600

# DB Config
DB_NAME = "customer"
DB_USER = "postgres"
DB_PASSWORD = False
DB_HOST = "127.0.0.1"
DB_PORT = 5432
DB_AUTOCOMMIT = True

DATABASE_URL = 'postgresql://%s@%s/%s' % (DB_USER, DB_HOST, DB_NAME)
