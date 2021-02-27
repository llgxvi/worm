from Crypto.Cipher import AES

key = b'xxxx cccc vvvv b'
iv  = b'gggg hhhh jjjj k'

def get_cipher(key, iv):
  return AES.new(key, AES.MODE_CFB, iv)


if __name__ == '__main__':
  c1 = get_cipher(key, iv)
  c2 = get_cipher(key, iv)
  c3 = get_cipher(key, iv)

  a = c1.encrypt('abc')
  b = c1.encrypt('abc')
  c = c2.decrypt(a)
  d = c2.decrypt(a)
  e = c3.decrypt(a)

  print(a)
  print(b)
  print(c)
  print(d)
  print(e)
