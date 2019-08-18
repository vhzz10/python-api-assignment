# -*- coding: utf-8 -*-

import falcon
import json

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict
    
from app.errors import NotSupportedError
from sqlalchemy.ext.declarative import DeclarativeMeta

def new_alchemy_encoder():
    # http://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if obj in _visited_objs:
                    return None
                _visited_objs.append(obj)

                # an SQLAlchemy class
                fields = {}
                for field in [
                    x for x in dir(obj) if not x.startswith("_") and x != "metadata"
                ]:
                    fields[field] = obj.__getattribute__(field)
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


class BaseResource(object):
    HELLO_WORLD = {
        "server": "Falcon API",
        "database": "Customer",
    }

    def to_json(self, body_dict):
        return json.dumps(body_dict)

    def from_db_to_json(self, db):
        return json.dumps(db, cls=new_alchemy_encoder())

    def on_error(self, res, error=None):
        res.status = error["status"]
        meta = OrderedDict()
        meta["code"] = error["code"]
        meta["message"] = error["message"]

        obj = OrderedDict()
        obj["meta"] = meta
        res.body = self.to_json(obj)

    def on_success(self, res, data=None):
        res.status = falcon.HTTP_200
        meta = OrderedDict()
        meta["code"] = 200
        meta["message"] = "OK"

        obj = OrderedDict()
        obj["meta"] = meta
        obj["data"] = data
        res.body = self.to_json(obj)

    def on_get(self, req, res):
        raise NotSupportedError(method="GET", url=req.path)

    def on_post(self, req, res):
        raise NotSupportedError(method="POST", url=req.path)

    def on_put(self, req, res):
        raise NotSupportedError(method="PUT", url=req.path)

    def on_delete(self, req, res):
        raise NotSupportedError(method="DELETE", url=req.path)