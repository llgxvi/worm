#!/usr/bin/env python3

import sys
import time
import socket
from cipher import get_cipher
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
    while True:
      o = input('\rEnter option: ') # \r clears print of ctrl + c (^C)
      o = o.strip()
      if o:
        break

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
    try:
      data = Receive(sock, decipher)
    except Exception as e:
      pr('⚠️', e)
      active = False
      close(sock, client)
      break

    if not data:
      pr('⚠️ Client disconnected')
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
      continue # ‼️ file transmission related data come immediately after

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
      fn = nc[3:].strip()
      try:
        f = open(fn, 'rb')
        d = f.read()
        f.close()
        Send(sock, cipher, d, fn)
        time.sleep(1)
      except Exception as e:
        pr('⚠️', e)
        Send(sock, cipher, 'pwd') # TODO

    else:
      Send(sock, cipher, nc)
