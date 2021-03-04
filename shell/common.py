import os
import re
import socket
from codec import encode, decode

pr = print
cls = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def _input(s=''):
  if s:
    s += ': '
  while True:
    i = input(s)
    i = i.strip()
    if i:
      break
  i = re.sub('\s+', ' ', i, 1)
  return i

EOD = b'EOD-EOD-EOD' # end of data
EOF = b'EOF-EOF-EOF' # end of file
EFN = b'EFN-EFN-EFN' # end of file name

def Send(sock, cipher, data, fn=None):
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
    return -1

  return 0

def Receive(sock, decipher):
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

    # TODO
    # if the last recv does not end with EOD
    # script will stuck at next recv (blocking)
    # one scenario is cipher pair out of sync

  pr('⬇️⬇️ recv:', data[-30:])

  if not data:
    return b''

  if data and not data.endswith(EOD):
    pr('⚠️ Data not end with EOD')
    return b''

  d = data[:-len(EOD)]

  if d.endswith(EOF):
    d = d[:-len(EOF)]
    d = d.split(EFN, 1)
    d[0] = d[0].decode()
  else:
    d = d.decode()

  return d
