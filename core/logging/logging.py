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
from ..utils.utils import ErrorHandling,Notifications
from ..utils.file_paths import DSFilePath,CFGFilePath
from datetime import datetime

class LoggingUtilitys():

    # Function will return a full string of desired directory
    def get_misc_file_path_str(self, file_path_from_working_dir):
        current_dir = os.path.join(os.getcwd())                                 #Get the current directory
        target_file_path = str(f'{current_dir}/{file_path_from_working_dir}')   #Prepare target file path string
        return target_file_path                                                 #Return the filepath string

    #Function will return date and time string when it is executed
    def get_date_time_string(self):
        moment = datetime.now()                                                 #Get date time string from current moment
        date_time_string = moment.strftime("%m/%d/%y %H:%M:%S")                 #Format the string
        return date_time_string                                                 #Return the date time string

    #Function will read a file and return the string data
    def retrieve_file_data(self,file_path):
        with open(file_path,'r') as file:               #Open file
            data = file.read()                          #Read & store data in var
            file.close()                                #Close the file
        return data                                     #Return the data

    #Function will write data parameter to file parameter
    def write_data_to_file(self,file_path,data):
        with open(file_path,'w') as file:               #Open file
            file.write(data)                            #Write data
            file.close()                                #Close file

class NetworkingConfigs():

    #Function will write the listening port for the shells functions
    def write_shell_lport(self,lport):
        LoggingUtilitys().write_data_to_file(CFGFilePath().shells_lport_file,lport)

    #Function will retrieve the and return the lport for shells from the lport.txt file
    def retrieve_shell_lport(self):
        lport = LoggingUtilitys().retrieve_file_data(CFGFilePath().shells_lport_file) #Retrieve lport file data
        return lport                                                    #return the lport

    #Function checks for existing port in config file and returns boolean value
    def check_config_for_existing_port(self, port):
        sockets = LoggingUtilitys().retrieve_file_data(CFGFilePath().server_sockets) #Get the server sockets
        for listener in sockets.split('\n'):                                  #For each port in the file split by a new line
            if listener == port:                                           #If the port on file is == to the port passed as a parameter
                return False                                               #Return false
        return True                                                        #Else if port is not found, return false

    #Function will add port to config file
    def add_port_to_config_file(self, port):
        if NetworkingConfigs().check_config_for_existing_port(port) == True:    #If the port parameter is not currently existent,
            with open(CFGFilePath().server_sockets, 'a') as port_config_file:   #Open the server sockets file in append mode
                port_config_file.write(f'{port}\n')                             #Write the port and new line
                port_config_file.close()                                        #Close the file
                return True #Return true if we could successfully add port to ports.txt. this means the port does not exist already
        else:
            #Raise error saying the listener exists if the port check function returns false
            ErrorHandling().raise_error('Listener Already Exists',
                                        '',
                                        'Already Exists')
            return False #Return false if port already exists in ports.txt. this stops the port from being added to ports display

    # Function will remove port from config file. This is for deleting listeners from the port display widget
    def remove_port_from_config_file(self, port):
        current_ports = LoggingUtilitys().retrieve_file_data(CFGFilePath().server_sockets).split('\n') #get the current ports form the config file
        for listener in current_ports:              # For the listeners in the ports array split by \n
            if listener == port:                    # if the listener is == to the port parameter
                current_ports.remove(listener)      # Remove the listener from the ports array
        with open(CFGFilePath().server_sockets, 'w') as port_config_file:    #Open the server sockets file
            for port in current_ports:                                       #For each port in current ports array
                port_config_file.write(port+'\n')                            #write the port
            port_config_file.close()                                         #Close the file

    #Function will write selected interface to interface file
    def write_network_interface(self,interface):
        LoggingUtilitys().write_data_to_file(CFGFilePath().current_interface,interface)

    #Function will retrieve network interface card from interface file
    def retrieve_network_interface(self):
        interface = LoggingUtilitys().retrieve_file_data(CFGFilePath().current_interface)   #Retrieve the interface from the cfg file
        return interface                                                                    #Return the interface string

    #Function will write the length of data parameter to the bits file for the data txrx label on the main gui
    def write_data_length(self,data_length):
        current_length = LoggingUtilitys().retrieve_file_data(DSFilePath().bits_file)       #Get current length of contents in file
        if current_length == '':                                                            #If it's not set
            current_length = 0                                                              #current length == 0
        byte_length = int(data_length)+int(current_length)                                  #get length in bytes of data parameter and data in bits file
        LoggingUtilitys().write_data_to_file(DSFilePath().bits_file,str(byte_length))       #Log the new data size in bytes to the bits file

    #Function will write the exfil port to exfil_port.txt
    def write_exfil_port(self,port_number):
        LoggingUtilitys().write_data_to_file(CFGFilePath().exfil_port_file,str(port_number))

    #Function will return port number of exfil port from txt file
    def retrieve_exfil_port(self):
        exfil_port = LoggingUtilitys().retrieve_file_data(CFGFilePath().exfil_port_file)
        return exfil_port

    #Function will write the stream port to the stream_port.txt file
    def write_stream_port(self,port_number):
        LoggingUtilitys().write_data_to_file(CFGFilePath().stream_port_file,str(port_number))

    #Function will return the stream port number from the txt file
    def retrieve_stream_port(self):
        stream_port = LoggingUtilitys().retrieve_file_data(CFGFilePath().stream_port_file)
        return stream_port

    #Function will record listening socket, Logically broken right now as only way to close socket is by killing program
    def record_listening_socket(self,port_number):
        LoggingUtilitys().write_data_to_file(DSFilePath().listening_sockets_file,port_number)


class DNSconfigs():
    #Function will return token string value from token file
    def retrieve_dns_token(self):
        dns_token = LoggingUtilitys().retrieve_file_data(CFGFilePath().dns_token)
        return dns_token

    #Function will write new token to dns token config file
    def write_new_token(self,new_token):
        LoggingUtilitys().write_data_to_file(CFGFilePath().dns_token,new_token)

    #Function will retrieve domains, append them to an array and return the array
    def retrieve_dns_domains(self):
        domain_array = []                               #Create domain array
        domains = LoggingUtilitys().retrieve_file_data(CFGFilePath().domains_file)
        for domain in domains.split('\n'):                  #For domains in the array split by a new line
            if domain != '':                                #If the domain is not an empty string
                domain_array.append(domain)                 #Append the data to the array
        return domain_array                                 #Return the array value

    #Function will remove domain passed as parameter from domains file
    def remove_domain_from_file(self,domain_to_remove):
        domains_on_file = self.retrieve_dns_domains()                   #Get dns domain array with function
        for domain in domains_on_file:                                  #For the domains in the array
            if domain == domain_to_remove:                              #If the domain == the domain parameter
                domains_on_file.remove(domain)                          #Remove the domain to the array
        with open(CFGFilePath().domains_file,'w') as domains_file: #Overwrite the domains file,
            for domain in domains_on_file:                              #For domain in the array
                domains_file.write(f'{domain}\n')                       #Write the domain to the file
            domains_file.close()                                        #Close the file

    #Function will add a domain to the domains file
    def add_domain_to_file(self,domain_to_add):
        with open(CFGFilePath().domains_file,'a') as domain_file:       #Open domain cfg file in append mode
            domain_file.write(f'{domain_to_add}\n')                     #Add the domain to the file with new line
            domain_file.close()                                         #Close the file

    #Function will retrieve the selected domain for the shells action
    def retrieve_domain_for_shell(self):
        domain = LoggingUtilitys().retrieve_file_data(CFGFilePath().chosen_domain)  #Retrieve chosen domain for shells
        return domain                                                               #Return the domain string

    #Function will write the chosen domain for the shells action
    def write_shell_domain(self,domain):
        LoggingUtilitys().write_data_to_file(CFGFilePath().chosen_domain,domain)

class ConsoleWindow():
    #function overwrites console log file to clear the console window
    def clear_console_logs(self):
        with open(DSFilePath().console_output_file, 'w') as file:                   #Open the file in write mode to overwite data
            file.close()                                                            #Close the file
        Notifications().raise_notification('Console logs have been cleared.','success') #Raise notification

    #Function writes string to file which will be read to update console window on main window
    def log_to_console(self,data_to_log):
        with open(DSFilePath().console_output_file,'a') as console_output:                          #Open console data storage file
            console_output.write(f'[{LoggingUtilitys().get_date_time_string()}] {data_to_log}\n')   #append the string to file
            console_output.close()                                                                  #Close the file

class ClientWindow:
    #Function records active connection in the active connections file
    def record_active_connection(self,info_array):
        array = []  #Create array
        with open(DSFilePath().active_connections_file,'a') as file:
            for info in info_array:                                    #Loop through info pieces in array received from sockets
                info = str(info).strip("'").strip(' ').replace("'",'') #Remove extra spaces and characters from array items
                array.append(info.strip('\n'))                         #Strip '\n' from string and append the info to the other array
            if array != '[]':                                          #If the array is not empty
                file.write(str(array)+'\n')                            #Write the array to the file
            file.close()

    #Function will remove connection from array by the encryption_key
    def remove_active_connection(self,address_array,encryption_key):
        for list in address_array:                  #Loop through client info arrays
            if list[8] == encryption_key:              #If the system name in the list equals the system name give to the parameter
                address_array.remove(list)          #Remove the last from the array
        with open(DSFilePath().active_connections_file,'w') as file:             #Clear the file by overwriting it in write mode
            for line in address_array:                             #For each list of client info in the array
                line = str(line).replace('" ','').replace('"\'','').replace('\'"','')
                file.write(line+'\n')                              #Write it to the file with a new line
            file.close()

class DiscordCFG():

    #Function will set the discord notifications to on or off
    def set_discord_notification(self,choice):
        LoggingUtilitys().write_data_to_file(CFGFilePath().discord_setting,choice)

    #Function will return bool if based on notification setting of enabled/disabled
    def retrieve_notification_setting(self):
        setting = LoggingUtilitys().retrieve_file_data(CFGFilePath().discord_setting).lower() #Retrieve data in file
        if setting == 'enabled':                        #If the data in the file is "enabled"
            return True                                 #Return true
        return False                                    #Anything else, return false

    #Function will return the raw string of what's on the discord notifications setting file
    def get_setting_string(self):
        return LoggingUtilitys().retrieve_file_data(CFGFilePath().discord_setting)

    #Function will record the discord webhook to the webhook file
    def record_webhook(self,webhook):
        LoggingUtilitys().write_data_to_file(CFGFilePath().discord_webhook,webhook)

    #Function will return the contents of the webhook file
    def retrieve_webhook(self):
        return LoggingUtilitys().retrieve_file_data(CFGFilePath().discord_webhook)