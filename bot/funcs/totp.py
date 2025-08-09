import base64
import hmac
import struct
import time
from hashlib import sha1


def is_base32(s: str) -> bool:
    try:
        base64.b32decode(s.upper().replace(" ", ""), casefold=True)
        return True
    except Exception:
        return False


def totp_now(base32_secret: str, digits: int = 6, interval: int = 30) -> str:
    key = base64.b32decode(base32_secret.upper().replace(" ", ""), casefold=True)
    counter = int(time.time() // interval)
    msg = struct.pack(">Q", counter)
    hmac_digest = hmac.new(key, msg, sha1).digest()
    offset = hmac_digest[-1] & 0x0F
    code_int = (
        ((hmac_digest[offset] & 0x7F) << 24)
        | (hmac_digest[offset + 1] << 16)
        | (hmac_digest[offset + 2] << 8)
        | (hmac_digest[offset + 3])
    )
    code = str(code_int % (10**digits)).zfill(digits)
    return code


def seconds_remaining(interval: int = 30) -> int:
    now = int(time.time())
    return interval - (now % interval)


if __name__ == "__main__":
    raise RuntimeError("This module should be run only via main.py")
