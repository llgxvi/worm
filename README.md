### python
`not [] is True`

```
[] * 2 is []
[None] * 2 is [None, None]
```

int() will strip first
`int('  1  ')`

`os.chdir('  /  ')` won't trim for you

### socket
**https://docs.python.org/2/howto/sockets.html**
https://docs.python.org/3/library/socket.html

bind() empty string
https://stackoverflow.com/questions/39815633/i-have-get-really-confused-in-ip-types-with-sockets-empty-string-local-host

settimeout(v)
```
v = 0:    non blocking
v > 0:    raise socket.timeout error after v seconds
v = None: blocking
```

### python crypto
https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

`pip3 install pycrypto`

⚠️ If one side regenerates cipher pair, the other side needs too

### subprocess
https://docs.python.org/3/library/subprocess.html#popen-constructor

Subprocess change directory
https://stackoverflow.com/questions/21406887/subprocess-changing-directory
