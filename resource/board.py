from flask_restful import Resource, reqparse
from firebase_admin import db

__ref__= 'database/board'
__id__ = 'id'
__is_active__ = 'is_active'
__on_proccess__ = 'on_process'

__format__ = {
    __id__: '',
    __is_active__: '',
    __on_proccess__: ''
}


class Board(Resource):
    _ref = db.reference(__ref__)
    _parser = reqparse.RequestParser()

    def __init__(self):
        self._parser.add_argument(__id__)
        self._parser.add_argument(__is_active__)
        self._parser.add_argument(__on_proccess__)

    def post(self):
        data = self._parser.parse_args()
        exists = False
        snapshot = self._ref.get()

        for id in snapshot:
            if snapshot[id][__id__] == data[__id__]:
                exists = True

        if exists:
            self._ref.child(data[__id__]).update({
                __format__[__is_active__]: data[__is_active__],
                __format__[__on_proccess__]: 'false'
            })

        else:
            format = __format__
            format[__id__] = data[__id__]
            format[__is_active__] = 'false'
            format[__on_proccess__] = 'false'

            self._ref.push(format)

        return {'response': 'OK'}, 200
