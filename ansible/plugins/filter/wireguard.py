import base64

from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat


def wg_pubkey(privkey):
    privkey_data = base64.b64decode(privkey.encode("ascii"))
    x = X25519PrivateKey.from_private_bytes(privkey_data)
    p = x.public_key()
    pubkey_data = p.public_bytes(Encoding.Raw, PublicFormat.Raw)
    pubkey = base64.b64encode(pubkey_data)
    return pubkey.decode("ascii")


class FilterModule:
    def filters(self):
        return {"wg_pubkey": wg_pubkey}
