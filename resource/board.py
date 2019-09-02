"""
Class ini digunakan untuk menghandle semua request pada route /board.
Method yang disediakan pada Route ini adalah :
- POST

Route ini digunakan untuk :
Memanipulasi data board (Device IoT)
seperti status active, on process.
"""

from flask_restful import Resource, reqparse
from firebase_admin import db

__ref__= 'database/board'
__id__ = 'id'
__is_active__ = 'active'
__on_proccess__ = 'OnProcess'

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
        """
        Fungsi merupakan blueprint untuk menghandle
        requests POST.

        Pada method ini akan terjadi operasi seperti :
        - Mengambil data dari Firebase Realtime Database dengan
          reference /database/board.

        - Melakukan Searching apakah parameter id yang diterima
          sudah ada atau belum ada.

        - Jika Hasil searching menyatakan sudah ada di database maka,
          Akan Mengupdate data yang diperlukan.

        - Namun jika hasil searchingnya menyatakan belum ada maka,
          akan menambahkan data baru ke dalam database dengan
          id data yang unik.

        :return: JSON Format, Jika tidak ada kesalahan operasi
            seharusnya akan memberikan response success.
        """
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
