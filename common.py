import os
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

encode = lambda c, x: b64encode(c.encrypt(x))
decode = lambda c, x: c.decrypt(b64decode(x))

pr = lambda s: print(s)

def clear():
    if os.name == 'nt':
      s = 'cls'
    else: 
      s = 'clear'
    os.system(s)

EOD = b'EOD-EOD-EOD'
EOF = b'EOF-EOF-EOF'
FN = b'FN-FN-FN'

# TODO
def get_cipher():
  key = 'xxxx cccc vvvv b'
  iv  = 'gggg hhhh jjjj k'
  cipher = AES.new(key, AES.MODE_CFB, iv)
  return cipher

# TODO
cipher = get_cipher()
decipher = get_cipher()

def Send(sock, data, fn=None):
  if not fn:
    data = data.encode()
  else:
    data = data + FN + fn + EOF

  data += EOD

  try:
    sock.sendall(Encode(cipher, data))
  except:
    pass

def Receive(sock):
  data = b''

  while(True):
    try:
      d = sock.recv(1024)
    except:
      pr('⚠️ recv error')
      return ''

    if not d:
      pr('🥅 recv empty')
      return ''

    print('⬇️ recv:', len(d), d[:20])

    data += Decode(decipher, d)
    if data.endswith(EOD):
      break

  data = data[:-len(EOD)]
  if data.endswith(EOF):
    return data[:-len(EOF)].split(FN)
  else: 
    return data.decode()
