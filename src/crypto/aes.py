import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
import streamlit as st

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

security_key = hashlib.sha256(st.secrets["security_key"].encode("utf-8")).digest()


def encrypt(raw, key = security_key):
    raw = str.encode(pad(raw))  # convert str to byte
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw)).decode('utf-8')


def decrypt(enc, key = security_key):
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:])).decode('utf-8')