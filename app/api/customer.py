# -*- coding: utf-8 -*-

import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator
from cerberus.errors import ValidationError

from app.api import BaseResource
from app.models import Customer
from app.errors import (
    AppError,
    InvalidParameterError,
    CustomerNotExistsError,
    UnauthorizedError,
)
from webargs import fields
from webargs.falconparser import use_args




FIELDS = {
    "name": {"type": "string", "required": True, "minlength": 1, "maxlength": 20},
    "dob": {"type": "string", "required": True},
}


def validate_user_create(req, res, resource, params):
    schema = {
        "name": FIELDS["name"],
        "dob": FIELDS["dob"],
    }

    v = Validator(schema)
    if not v.validate(req.context["data"]):
        raise InvalidParameterError(v.errors)


def auth_required(req, res, resource, params):
    if req.context["auth_user"] is None:
        raise UnauthorizedError()


class Collection(BaseResource):
    """
    Handle for endpoint: /customer
    """

    @falcon.before(auth_required)
    @falcon.before(validate_user_create)
    def on_post(self, req, res):
        session = req.context["session"]
        customer_req = req.context["data"]
        if customer_req:
            customer = Customer()
            customer.name = customer_req["name"]
            customer.dob = customer_req["dob"]
            session.add(customer)
            self.on_success(res, req.context["data"])
        else:
            raise InvalidParameterError(req.context["data"])

    @falcon.before(auth_required)
    def on_get(self, req, res):
        session = req.context["session"]
        customers = session.query(Customer).all()
        if customers:
            obj = [cus.to_dict() for cus in customers]
            self.on_success(res, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, req, res):
        pass

    @falcon.before(auth_required)
    def on_delete(self, req, res):
        pass


class Item(BaseResource):
    """
    Handle for endpoint: /customer/{cus_id}
    """

    @falcon.before(auth_required)
    def on_get(self, req, res, cus_id):
        session = req.context["session"]
        try:
            customer = Customer.find_one(session, cus_id)
            self.on_success(res, customer.to_dict())
        except NoResultFound:
            raise CustomerNotExistsError("customer id: %s" % cus_id)

    @falcon.before(auth_required)
    def on_put(self, req, res, cus_id):
        session = req.context["session"]
        customer_req = req.context["data"]
        try:
            customer = Customer.find_update(session, cus_id, customer_req)
            self.on_success(res, customer.to_dict())
        except NoResultFound:
            raise CustomerNotExistsError("customer id: %s" % cus_id)

    @falcon.before(auth_required)
    def on_delete(self, req, res, cus_id):
        session = req.context["session"]
        try:
            customer = Customer.find_one(session, cus_id)
            session.delete(customer)
            self.on_success(res, None)
        except NoResultFound:
            raise CustomerNotExistsError("customer id: %s" % cus_id)

