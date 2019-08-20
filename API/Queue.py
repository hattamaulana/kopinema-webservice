from flask_restful import Resource, reqparse
from firebase_admin import db
from datetime import datetime


__ref__ = 'database/queue'
__id__ = 'id'
__name__ = 'name'
__time__ = 'time'
__id_board__ = 'id_board'
__is_complete__ = 'is_complete'
__rasio__ = 'rasio'
__rasio_water__ = 'water'
__rasio_coffee__ = 'coffee'

__format__ = {
    __name__: '',
    __time__: '',
    __id_board__: '',
    __is_complete__: '',
    __rasio__: {
        __rasio_water__: '',
        __rasio_coffee__: ''
    }
}


class Queue(Resource):
    _ref = db.reference(__ref__)

    def get(self, id):
        res = []
        snapshot = self._ref.get()

        if len(snapshot) > 0:
            for i in snapshot:
                if snapshot[i][__id_board__] == id:
                    snapshot[i][__id__] = i
                    res.append(snapshot[i])

            res = sorted(res, key=lambda key: key[__time__])

            if len(res) > 0:
                return {'response': {'status': 'OK', 'data': res[0]}}, 200

            else:
                return {'response': {'status': 'OK', 'data': 'empty'}}, 200

        else:
            return {'response': {'status': 'OK', 'data': 'empty'}}, 200
