```
❌ False == ''
❌ True  == ''
❌ None  == ''
❌ []    == ''
❌ ()    == ''
❌ {}    == ''

❌ 'xxx'  == True
❌ ''     == True
❌ [1, 2] == True
❌ []     == True

ℹ️ [] * 2 == []
ℹ️ [None] * 2 == [None, None]
```

```
pip3 install pycrypto
```

```
# settimeout(v)

v = 0:    non blocking
v > 0:    raise socket.timeout error after v seconds
v = None: blocking
```

```
# Popen

p = sp.Popen('', shell=True)
p.communicate()
(None, None)

p = sp.Popen('', shell=True, stdout=sp.PIPE)
p.communicate()
(b'', None)

p = sp.Popen('', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
p.communicate()
(b'', b'')
```

- https://docs.python.org/3/howto/sockets.html
- https://stackoverflow.com/questions/39815633/i-have-get-really-confused-in-ip-types-with-sockets-empty-string-local-host
- https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
- https://stackoverflow.com/questions/21406887/subprocess-changing-directory
