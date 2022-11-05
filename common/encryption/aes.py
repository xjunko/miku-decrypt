from Crypto.Cipher import AES

# Constant
KEY: str = ""
IV: str = ""

# Global
crypt: AES = AES.new(KEY.encode(), AES.MODE_CBC, IV.encode())


def encrypt(data: bytes) -> bytes:
    pad = 16 - len(data) % 16
    pad = pad.to_bytes(1, "big") * pad

    return crypt.encrypt(data + pad)


def decrypt(data: bytes) -> bytes:
    data = crypt.decrypt(data)
    return data[: -data[-1]]
