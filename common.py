from Crypto.Cipher import AES
from base64 import b64encode, b64decode

Encode = lambda c, x: b64encode(c.encrypt(x))
Decode = lambda c, x: c.decrypt(b64decode(x))

def pr(s):
  # TODO
  print(s)

def get_cipher():
  # TODO
  key = 'xxxx cccc vvvv b'
  iv  = 'gggg hhhh jjjj k'
  cipher = AES.new(key, AES.MODE_CFB, iv)
  return cipher

# TODO
cipher = get_cipher()
decipher = get_cipher()

def Send(sock, data):
  sock.sendall(Encode(cipher, data))

def Receive(sock):
  data = ''

  d = sock.recv(1024)
  print('🥃 sock.recv: ', d)
  while(True):
    data += Decode(decipher, d).decode('utf-8')
    if data.endswith('EODXXX'):
      break
    d = sock.recv(1024)
    print('🥃 sock.recv: ', d)

  return data[:-6]
