import falcon

from app.middleware import DatabaseSession, AuthMiddleware, LoginResource, JSONTranslator
from app.database import db_session, init_session

from app.api import Collection, Item
from app.errors import AppError
from passlib.hash import sha256_crypt
from app.config import SECRET_KEY, TOKEN_EXPIRES

USERS = {
        "username": "test_api",
        }   

COOKIE_OPTS = {"name": "my_auth_token",
               "max_age": 86400,
               "path": "/customer",
               "http_only": True,
               "value": "",
               }

login = LoginResource(USERS.get, SECRET_KEY, TOKEN_EXPIRES, token_opts=COOKIE_OPTS)

class App(falcon.API):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)

        self.add_route('/login', login)
        self.add_route("/customer", Collection())
        self.add_route("/customer/{cus_id}", Item())

        self.add_error_handler(AppError, AppError.handle)


init_session()

middleware = [AuthMiddleware(), JSONTranslator(), DatabaseSession(db_session)]
application = App(middleware=middleware)


if __name__ == "__main__":
    from wsgiref import simple_server

    httpd = simple_server.make_server("127.0.0.1", 8071, application)
    httpd.serve_forever()