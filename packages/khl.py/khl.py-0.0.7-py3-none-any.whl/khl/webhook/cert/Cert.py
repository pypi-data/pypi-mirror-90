import base64

from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding


class Cert:
    def __init__(self, *,
                 client_id: str, client_secret: str,
                 token: str, verify_token: str,
                 encrypt_key: str = ''):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token
        self.verify_token = verify_token
        self.encrypt_key = encrypt_key

    def decrypt(self, data: bytes) -> str:
        if not self.encrypt_key:
            return ''
        data = base64.b64decode(data)
        data = AES.new(key=self.encrypt_key.encode('utf-8').ljust(32, b'\x00'),
                       mode=AES.MODE_CBC, iv=data[0:16]).decrypt(base64.b64decode(data[16:]))
        data = Padding.unpad(data, 16)
        return data.decode('utf-8')
