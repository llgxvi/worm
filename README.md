### python
`not [] is True`

```
[] * 2 is []
[None] * 2 is [None, None]
```

int() will strip first
`int('  1  ')`

`os.chdir('  /  ')` won't trim for you

open(' x.jpg  ') raise error

⚠️ Blocking socket needs to work with KeyboardInterupt (ctrl + c)

### socket
https://docs.python.org/2/howto/sockets.html
https://docs.python.org/3/library/socket.html
https://docs.python.org/3/library/signal.html

bind() empty string
https://stackoverflow.com/questions/39815633/i-have-get-really-confused-in-ip-types-with-sockets-empty-string-local-host

settimeout(v)
```
v = 0:    non blocking
v > 0:    raise socket.timeout error after v seconds
v = None: blocking
```

sendall()
⚠️ If somehow (unlikely) there are consecutive sendall happening,
time interval (time.sleep) is necessary.

### python crypto
https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

`pip3 install pycrypto`

⚠️ If one side regenerates cipher pair, the other side needs too

### subprocess
https://docs.python.org/3/library/subprocess.html#popen-constructor

Subprocess change directory
https://stackoverflow.com/questions/21406887/subprocess-changing-directory
