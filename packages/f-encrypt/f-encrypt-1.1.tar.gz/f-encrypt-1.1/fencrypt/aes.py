""" AES cipher methods """
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


ENCODING = "UTF-8"


def _pad(raw64):
    """ AES uses blocks of 16 chars at a time. Pad the block out with extra chars if needed.

        The argument raw64 expects a base64 string in ENCODING format (see constants)
    """
    # AES.block_size == 16
    block_size = AES.block_size
    # use a different padding char depending on the strings length mod 16
    pad_chr = chr(block_size - len(raw64) % block_size)
    # pad_length is the # of chars to add to bring the raw str to a multiple of 16 chars
    pad_length = (block_size - len(raw64)) % 16
    padding = pad_length * pad_chr
    return raw64 + padding


def _unpad(padded):
    """ Remove the padding applied by _pad() """
    return padded[:-ord(padded[len(padded) - 1:])]


def encrypt(secret_key, plaintext_bytes):
    """ Encrypt given plaintext and return as base64 string """
    pt_b64 = base64.b64encode(plaintext_bytes).decode(ENCODING)
    key = hashlib.sha256(secret_key.encode()).digest()
    padded_pt = _pad(pt_b64)
    init_vector = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    encoded_pt = padded_pt.encode()
    ciphertext = cipher.encrypt(encoded_pt)
    ct_b64 = base64.b64encode(init_vector + ciphertext)
    return ct_b64.decode(ENCODING)


def decrypt(secret_key, ct_b64):
    """ Decrypt given base64 ciphertext and return plaintext string """
    ct_decoded = base64.b64decode(ct_b64)
    init_vector = ct_decoded[: AES.block_size]
    key = hashlib.sha256(secret_key.encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, init_vector)
    encoded_padded_b64_pt = cipher.decrypt(ct_decoded[AES.block_size:])
    padded_b64_pt = encoded_padded_b64_pt.decode(ENCODING)
    b64_pt = _unpad(padded_b64_pt)
    return base64.b64decode(b64_pt)
