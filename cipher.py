from Crypto.Cipher import AES

key = b'xxxx cccc vvvv b'
iv  = b'gggg hhhh jjjj k'

def get_cipher(key, iv):
  return AES.new(key, AES.MODE_CFB, iv)

if __name__ == '__main__':
  cipher = get_cipher(key, iv)
  decipher = get_cipher(key, iv)

  a = cipher.encrypt('abc')
  b = decipher.decrypt(a)
  
  print(a, b)
  
