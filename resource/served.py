import json

from flask_restful import Resource, reqparse
from firebase_admin import db

from .queue import __format__, __id__

__ref__ = 'database/served'


class Served(Resource):
    _ref = db.reference(__ref__)
    _parser = reqparse.RequestParser()

    def __init__(self):
        print(__format__)
        for key in __format__:
            self._parser.add_argument(key)

        self._parser.add_argument(__id__)

    def post(self):
        from .queue import __is_complete__, __rasio__, __ref__ as queue

        args = self._parser.parse_args()
        if args[__is_complete__] == 'true':
            """
            Delete Item on Reference.
            And then Push Items to 'database/served' reference
            """
            db.reference(queue).child(args[__id__]).delete()

            args[__rasio__] = json.loads(args[__rasio__].replace("'", "\""))
            self._ref.push(args)

            message = 'Success Do Operation'

        else:
            message = 'Failed Do Operation'

        return {'response': { 'status': 'OK', 'message': message} }, 200
