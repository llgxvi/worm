### python
People choose python for its simplicity (like implicit typing);
this should also be the guiding principle in `if` condition - 
unless necessary, make it as short as possible.

Some function will trim its string argument,
problem is we'll never remember which one.
Intuition doesn't always work (I thought this function should do it for me 🤷🏿).
It's a good consideration until it becomes just one more memory load.
Just trim all string (input) first.

```
❌ None == ''
❌ 'xxx' == True
❌ [] == ''
✅ not [] == True
✅ [] * 2 == []
✅ [None] * 2 == [None, None]
```

`int('  1  ')` strip first

`os.chdir('  /  ')` won't trim for you

`open(' x.jpg  ')` raise error

`os.chdir('~')`
https://stackoverflow.com/questions/41733251/os-chdir-to-relative-home-directory-home-usr

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
⚠️ If somehow (unlikely) there are consecutive sendall (bad design) happening,
time interval (time.sleep) may be necessary.

### python crypto
https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

`pip3 install pycrypto`

⚠️ If one side regenerates cipher pair, the other side needs too.

### subprocess
https://docs.python.org/3/library/subprocess.html#popen-constructor

Subprocess change directory
https://stackoverflow.com/questions/21406887/subprocess-changing-directory

```
p = sp.Popen('xxx', shell=True)
p.communicate() # (None, None)

p = sp.Popen('xxx', shell=True, stdout=sp.PIPE)
p.communicate() # (b'', None)

p = sp.Popen('xxx', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
p.communicate() # (b'', b'')
```
