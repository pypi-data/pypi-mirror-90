#  Copyright (c) 2021. Alexander Eisele <alexander@eiselecloud.de>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from dataclasses import dataclass, field

from cryptobox._cbox import lib, ffi


@dataclass
class PreKey:
    id: int = field()
    data: bytes = field()


class CBox:
    def __init__(self):
        self._ptr_ptr = ffi.new("struct CBox * *")
        self._init = False

    def file_open(self, path: str):
        r = lib.cbox_file_open(path.encode("utf8"), self._ptr_ptr)
        self._init = True
        print(r)

    @property
    def _ptr(self):
        if self._init:
            return self._ptr_ptr[0]
        else:
            raise Exception("CBox not initialized")

    def decrypt(self, from_: str, sender: str, text: bytes) -> bytes:
        sid = generate_session_id(from_, sender)
        session = self.session_from_message(sid, text)
        return session.get_message()

    def encrypt(self, user_id: str, client_id: str, pre_key: PreKey, text: bytes) -> bytes:
        sid = generate_session_id(user_id, client_id)
        session = self.session_from_prekey(sid, pre_key.data)
        return session.encrypt(text)

    def close(self):
        r = lib.cbox_close(self._ptr)

    def new_pre_key(self, pre_key_id: int) -> PreKey:
        vec = CBoxVec()
        r = lib.cbox_new_prekey(self._ptr, pre_key_id, vec._ptr_ptr)
        return PreKey(id=pre_key_id, data=vec.bytes())

    def new_last_pre_key(self) -> PreKey:
        return self.new_pre_key(lib.CBOX_LAST_PREKEY_ID)

    def session_from_prekey(self, session_id: str, prekey: bytes):
        session = CBoxSession(self)
        r = lib.cbox_session_init_from_prekey(
            self._ptr,
            session_id.encode("utf8"),
            prekey,
            len(prekey),
            session._ptr_ptr
        )
        session._init = True
        return session

    def session_from_message(self, session_id: str, cipher: bytes):
        session = CBoxSession(self)
        vec = CBoxVec()
        size = ffi.new("size_t *")
        size_p = len(cipher)
        r = lib.cbox_session_init_from_message(
            self._ptr,
            session_id.encode("utf8"),
            cipher,
            size_p,
            session._ptr_ptr,
            vec._ptr_ptr
        )
        session._init = True
        session._message = vec.bytes()
        return session


def generate_session_id(user_id: str, client_id):
    return f"{user_id}_{client_id}"


class CBoxVec:
    def __init__(self):
        self._ptr_ptr = ffi.new("struct CBoxVec * *")

    @property
    def _ptr(self):
        return self._ptr_ptr[0]

    def len(self):
        return lib.cbox_vec_len(self._ptr)

    def bytes(self) -> bytes:
        arr = ffi.unpack(lib.cbox_vec_data(self._ptr), self.len())
        return bytes(arr)


class CBoxSession:
    def __init__(self, cbox: CBox):
        self._ptr_ptr = ffi.new("struct CBoxSession * *")
        self._init = False
        self.cbox = cbox
        self._message: bytes = b''

    @property
    def _ptr(self):
        if self._init:
            return self._ptr_ptr[0]
        else:
            raise Exception("CBox not initialized")

    def get_message(self):
        return self._message

    def decrypt(self, cipher: bytes) -> bytes:
        vec = CBoxVec()
        r = lib.cbox_decrypt(
            self._ptr,
            cipher,
            len(cipher),
            vec._ptr_ptr
        )
        return vec.bytes()

    def encrypt(self, text: bytes) -> bytes:
        vec = CBoxVec()
        r = lib.cbox_encrypt(
            self._ptr,
            text,
            len(text),
            vec._ptr_ptr
        )
        return vec.bytes()
