from Crypto.Cipher import AES
from base64 import b64encode, b64decode

encode = lambda c, x: b64encode(c.encrypt(x))
decode = lambda c, x: c.decrypt(b64decode(x))

def get_cipher():
  key = b'xxxx cccc vvvv b'
  iv  = b'gggg hhhh jjjj k'
  cipher = AES.new(key, AES.MODE_CFB, iv)
  return cipher

cipher = get_cipher()
decipher = get_cipher()
