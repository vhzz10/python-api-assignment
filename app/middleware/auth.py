# -*- coding: utf-8 -*-

import jwt

from app.errors import UnauthorizedError, AppError
from app.config import SECRET_KEY, TOKEN_EXPIRES

from app.api import BaseResource

from passlib.hash import sha256_crypt
from datetime import datetime, timedelta
import json

DEFAULT_TOKEN_OPTS = {"name": "auth_token", "location": "header"}

class LoginResource(BaseResource):

    def __init__(self, get_user, secret, token_expiration_seconds, token_opts):
        self.get_user = get_user
        self.secret = SECRET_KEY
        self.token_expiration_seconds = TOKEN_EXPIRES
        self.token_opts = token_opts or DEFAULT_TOKEN_OPTS

    def on_post(self, req, res):
        user_req = req.context['data']
        if 'username' not in user_req:
            raise UnauthorizedError('Missing username, please try again - %s' % (req.context))
        username = user_req["username"]
        user = self.get_user("username")
        if user == username:
            self.add_new_jwtoken(res, user)
        else:
            raise UnauthorizedError('Wrong Login Username - %s - %s' % (username, user))
        

    # given a user identifier, this will add a new token to the response
    # Typically you would call this from within your login function, after the
    # back end has OK'd the username
    def add_new_jwtoken(self, res, user_identifier=None):
        # add a JSON web token to the response headers
        if not user_identifier:
            raise Exception('Empty user_identifer passed to set JWT')
        token = jwt.encode({'user_identifier': user_identifier,
                            'exp': datetime.utcnow() + timedelta(
                                seconds=self.token_expiration_seconds)},
                           self.secret,
                           algorithm='HS256').decode("utf-8")
        self.token_opts.update({
            "value": token,
        })

        if self.token_opts.get('location', 'header') == 'header':
            res.body = json.dumps({
                self.token_opts['name']: self.token_opts['value']
                })
            self.on_success(res, {'Token': self.token_opts['value']})
        else:
            raise AppError('Unrecognized jwt token location specifier')


class AuthMiddleware(object):

    def process_request(self, req, res, resource=None):
        if req.auth is not None:
            token = req.auth
            if token and not self._token_is_valid(token):
                raise UnauthorizedError("Invalid auth token: %s" % req.auth)
            if token is None:
                raise UnauthorizedError("Invalid auth token: %s" % req.auth)
            else:
                options = {'verify_exp': True}
                req.context["auth_user"] = jwt.decode(token, SECRET_KEY,
                                                        verify='True',
                                                        algorithms=['HS256'],
                                                        options=options)
        else:
            req.context["auth_user"] = None

    def _token_is_valid(self, token):
        try:
            options = {'verify_exp': True}
            jwt.decode(
                token, SECRET_KEY,
                verify='True',
                algorithms=['HS256'],
                options=options)
            return True
        except jwt.DecodeError as err:
            return False