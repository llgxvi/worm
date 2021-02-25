import os
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

Encode = lambda c, x: b64encode(c.encrypt(x))
Decode = lambda c, x: c.decrypt(b64decode(x))

def pr(s):
  print(s)

def get_cipher():
  # TODO
  key = 'xxxx cccc vvvv b'
  iv  = 'gggg hhhh jjjj k'
  cipher = AES.new(key, AES.MODE_CFB, iv)
  return cipher

# clear
if os.name == 'posix':
  s = 'clear' # linux
if os.name == 'nt':
  s = 'cls'   # windows
clear = lambda: os.system(s)

# TODO
cipher = get_cipher()
decipher = get_cipher()

# data: cmd/data
def Send(sock, data, end='EOFEOFEOFEOFEOFX'):
  if end:
    data += end
  sock.sendall(Encode(cipher, data))

def Receive(sock, end=b'EOFEOFEOFEOFEOFX'):
  data = []

  d = sock.recv(1024)
  while(d):
    dec = Decode(decipher, d)
    data.append(dec)
    if data[-1] == end:
      break
    else:
      d = sock.recv(1024)

  return ''.join(data[:-1])

if __name__ == '__main__':
  a = Encode(cipher, 'abc')
  b = Decode(decipher, a)
  pr(a)
  pr(b)
