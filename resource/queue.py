"""
Class ini digunakan untuk menghandle semua request pada route /queue/<id>.
Dimana parameter id yang dibutuhkan adalah Id dari Board/Device IoT.
Method yang disediakan pada Route ini adalah :
- GET

Route ini digunakan untuk :
Mengambil data berdasarkan waktu yang pertama kali disimpan.
"""

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
        """
        Fungsi merupakan blueprint untuk menghandle
        requests GET dengan parameter id yaiut ID dari Board/Device IoT.

        Pada method ini akan terjadi operasi seperti :
        - Mengambil data dari Firebase Realtime Database dengan
          reference /database/queue.

        - Melakukan Searching data sesuai dengan
          parameter id.

        - Melakukan Sorting berdasarkan time.

        :return: JSON Format, Jika tidak ada kesalahan operasi
            seharusnya akan memberikan response data yang
            pertama dari hasil sorting dan status success.
        """
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
