```
❌ None == ''
❌ []   == ''

❌ ''     == True
❌ 'xxx'  == True
❌ []     == True
❌ [1, 2] == True

ℹ️ [] * 2 == []
ℹ️ [None] * 2 == [None, None]

pip3 install pycrypto
```

- https://docs.python.org/2/howto/sockets.html
- https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
- https://stackoverflow.com/questions/21406887/subprocess-changing-directory
- https://stackoverflow.com/questions/39815633/i-have-get-really-confused-in-ip-types-with-sockets-empty-string-local-host

settimeout(v)
```
v = 0:    non blocking
v > 0:    raise socket.timeout error after v seconds
v = None: blocking
```

```
p = sp.Popen('xxx', shell=True)
p.communicate() # (None, None)

p = sp.Popen('xxx', shell=True, stdout=sp.PIPE)
p.communicate() # (b'', None)

p = sp.Popen('xxx', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
p.communicate() # (b'', b'')
```
