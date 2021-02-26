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

# TODO
def get_cipher():
  key = 'xxxx cccc vvvv b'
  iv  = 'gggg hhhh jjjj k'
  cipher = AES.new(key, AES.MODE_CFB, iv)
  return cipher

# TODO
cipher = get_cipher()
decipher = get_cipher()

def Send(sock, data, flag=0):
  if flag == 0:
    data = data.encode()

  data += b'EOD-EOD-EOD'

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
      return ''

    if not d:
      pr('🥅 recv empty')
      return ''

    print('⬇️ recv:', len(d), d[:20])

    data += Decode(decipher, d)
    if data.endswith(b'EOD-EOD-EOD'):
      break

  data = data[:-11]
  if data.endswith(b'EOF-EOF-EOF'):
    return data[:-11].split('FILENAME')
  else: 
    return data.decode()
