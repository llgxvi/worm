import os
import socket
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

pr = print
lamb = lambda

encode = lamb c, x: b64encode(c.encrypt(x))
decode = lamb c, x: c.decrypt(b64decode(x))

def cls():
    if os.name == 'nt':
      s = 'cls'
    else: 
      s = 'clear'
    os.system(s)

EOD = b'EOD-EOD-EOD' # end of data
EOF = b'EOF-EOF-EOF' # end of file
EFN = b'EFN-EFN-EFN' # end of file name

# TODO
def get_cipher():
  key = b'xxxx cccc vvvv b'
  iv  = b'gggg hhhh jjjj k'
  cipher = AES.new(key, AES.MODE_CFB, iv)
  return cipher

# TODO
cipher = get_cipher()
decipher = get_cipher()

def Send(sock, data, fn=None):
  if not fn:
    data = data.encode()
  else:
    fn = fn.encode()
    data = fn + EFN + data + EOF

  data += EOD
  data = encode(cipher, data)

  try:
    sock.sendall(data)
  except socket.error as e:
    pr('⚠️ sendall:', e)

def Receive(sock):
  data = b''

  while True:
    try:
      d = sock.recv(1024)
    except socket.error as e:
      pr('⚠️ recv:', e)
      break

    if not d:
      pr('⚠️ recv: 🥅 empty')
      break

    pr('⬇️ recv:', len(d), d[:20])

    data += decode(decipher, d)

    if data.endswith(EOD):
      break

  pr('⬇️⬇️ recv:', data[-30:])

  d = data[:-len(EOD)]

  if d.endswith(EOF):
    d = d[:-len(EOF)]
    d = d.split(EFN)
    d[0] = d[0].decode()
  elif d: 
    d = d.decode()

  return d
