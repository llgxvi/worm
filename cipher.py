from Crypto.Cipher import AES

key = b'xxxx cccc vvvv b'
iv  = b'gggg hhhh jjjj k'

def get_cipher():
  global key, iv
  return AES.new(key, AES.MODE_CFB, iv)

if __name__ == '__main__':
  c1 = get_cipher()
  c2 = get_cipher()
  c3 = get_cipher()

  a = c1.encrypt('abc')
  b = c1.encrypt('abc')
  c = c2.decrypt(a)
  d = c2.decrypt(a)
  e = c3.decrypt(a)
  f = c3.decrypt(b)

  print(a) # b'\xb2\x9f\xa4'
  print(b) # b'\xa7;:'
  print(c) # b'abc'
  print(d) # b't85'
  print(e) # b'abc'
  print(f) # b'abc'
