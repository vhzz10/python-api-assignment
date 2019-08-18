PYTHON API ASSIGNMENT
===============================
For testing - this app is running with risk security.

Requirements
============
This project uses [virtualenv](https://virtualenv.pypa.io/en/stable/) as isolated Python environment for installation and running. Therefore, [virtualenv](https://virtualenv.pypa.io/en/stable/) must be installed. And you may need a related dependency library for a PostgreSQL database. See [install.sh](https://github.com/ziwon/falcon-rest-api/blob/master/install.sh) for details.


Installation
============

Install all the python module dependencies in requirements.txt

```
chmod +x install.sh
```

```
  ./install.sh
```

Start server

```
  ./bin/run.sh start
```

PG_HBA CONFIG
=====
```
  # IPv4 local connections:
    host    all   all         127.0.0.1/32        trust
```

POSTMAN CONFIG
=====
Use file VietHoa.postman_collection.json to import to Postman.

UNIT TEST CASE
=====
```
  1. Test Login - Get Token
  2. Test Create success
  3. Test Create failed by Token Expired - Use Mock to control exp time of generating jwt token.
```

Changed
=====
```
  1. Call JWT Token from header, not store on Cookie.
```

Usage
=====

LOGIN
```shell
curl -XPOST http://api.myvnc.com:8071/login -H "Content-Type: application/json" -d '{"username":"test_api"}'
```

- Response
```
{
    "meta": {
        "code": 200,
        "message": "OK"
    },
    "data": {
        "Token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkZW50aWZpZXIiOiJ0ZXN0X2FwaSIsImV4cCI6MTU2MjA1NjAxNH0.pI-Ik2GGSBrkC3jMu-EB5hFTUmWfR3X-qT1ykuUC__E"
    }
}
```




CREATE
```shell
curl -XPOST http://api.myvnc.com:8071/customer -H "Content-Type: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkZW50aWZpZXIiOiJ0ZXN0X2FwaSIsImV4cCI6MTU2MjA1NjAxNH0.pI-Ik2GGSBrkC3jMu-EB5hFTUmWfR3X-qT1ykuUC__E" -d '{"dob": "2019-01-01", "name": "test1"}'
```

- Reponse
```
{
    "meta": {
        "code": 200,
        "message": "OK"
    },
    "data": {
        "dob": "2019-01-01",
        "name": "test1"
    }
}
```




READ

```shell
curl -XGET http://api.myvnc.com:8071/customer -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkZW50aWZpZXIiOiJ0ZXN0X2FwaSIsImV4cCI6MTU2MjA1NjAxNH0.pI-Ik2GGSBrkC3jMu-EB5hFTUmWfR3X-qT1ykuUC__E"
```

- Reponse

```
{
    "meta": {
        "code": 200,
        "message": "OK"
    },
    "data": [
        {
            "name": "test1",
            "dob": "2019-01-01"
        }
    ]
}

```



UPDATE
```shell
curl -XPUT http://api.myvnc.com:8071/customer/1 -H "Content-Type: application/json" -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkZW50aWZpZXIiOiJ0ZXN0X2FwaSIsImV4cCI6MTU2MjA1NjAxNH0.pI-Ik2GGSBrkC3jMu-EB5hFTUmWfR3X-qT1ykuUC__E" -d '{"dob": "2019-01-10", "name": "test1"}'
```

- Reponse
```
{
    "meta": {
        "code": 200,
        "message": "OK"
    },
    "data": {
        "name": "test2",
        "dob": "2019-01-01"
    }
}
```



DELETE
```shell
curl -XDELETE http://api.myvnc.com:8071/customer/1 -H "Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkZW50aWZpZXIiOiJ0ZXN0X2FwaSIsImV4cCI6MTU2MjA1NjAxNH0.pI-Ik2GGSBrkC3jMu-EB5hFTUmWfR3X-qT1ykuUC__E"
```

- Reponse
```
{
    "meta": {
        "code": 200,
        "message": "OK"
    },
    "data": null
}
```
