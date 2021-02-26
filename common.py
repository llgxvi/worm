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
  if type(data).__name__ == 'str':
    data = data.encode()
  data += b'EODXXX'
  sock.sendall(Encode(cipher, data))

def Receive(sock):
  data = b''

  while(True):
    try:
      d = sock.recv(1024)
    except:
      # TODO
      break

    if not d:
      print('🥅 recv empty')
      break

    print('⬇️ recv:', len(d), d[:20])

    data += Decode(decipher, d)
    if data.endswith(b'EODXXX'):
      break

  return data[:-6]
