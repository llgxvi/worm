from base64 import b64encode, b64decode

def encode(cipher, data):
  data = cipher.encrypt(data)
  data = b64encode(data)
  return data

def decode(decipher, data):
  data = b64decode(data)
  data = decipher.decrypt(data)
  return data
