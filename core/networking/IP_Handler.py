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
# Build:  1.0.1
# -------------------------------------------------------------
import netifaces
import requests
import os

from ..logging.logging import NetworkingConfigs

class NicHandler:
    #Function will return array with all interfaces found in linux directory
    def get_all_interfaces(self):
        interfaces = os.listdir('/sys/class/net') #list all interfaces in net dir
        return interfaces                         #Return interface array

#Function checks the value of the host and then returns IP values if called for
    def validate_host(self,host):
        if host == 'Local IP':                    #If the host value is == local IP
            host = IPAddress().get_local_ip_from_interface() #set host to local ip address
        elif host == 'Public IP':                 #If the host is public IP,
            host = IPAddress().get_public_ip_string()        #set the host to the local ip
        return host                               #Return the value of host

class IPAddress:

    #Function will return public IP string
    def get_public_ip_string(self):
        public_ip_string = requests.get('http://ident.me').text   #Get the public ip string
        return public_ip_string                                         #Return the public ip string

    #Function will return local ip from interface in cfg file
    def get_local_ip_from_interface(self):
        current_interface = NetworkingConfigs().retrieve_network_interface()        #get the current interface from the cfg file
        interface_dict = netifaces.ifaddresses(current_interface)                   #get dict value from current interface
        interface = interface_dict[2]                                               #Index the dict
        strip = interface[0]                                                        #Index again
        local_ip = strip.get('addr')                                                #Get the local ip assigned to the 'addr' value
        return local_ip                                                             #Return the local ip string

    #Funtion will get the geolocation of an ip address
    def get_ip_geolocation(self, ip_address):
        self.ip_location = requests.get(f'http://ip-api.com/json/{str(ip_address)}').json() #send get request to api with ip address and parse in json format
        if self.ip_location['status'] == 'fail':                                            #if the status is failed
            return ''                                                                       #return empty string
        else:
            return self.ip_location                                                         #else return the geolocation from the address