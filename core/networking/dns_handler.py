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
import requests
from ..networking.IP_Handler import IPAddress
from ..logging.logging import DNSconfigs,ConsoleWindow
from ..utils.file_paths import CFGFilePath
from ..utils.utils import Notifications,ErrorHandling

class DomainHandler():

    #Function will read domains from config file and then update them with the token read from the token file
    def update_dns_domain(self):
        domain_array = []           #Create local domain array
        with open(CFGFilePath().domains_file) as domain_file: #Open domains text file
            domains = domain_file.read()            #Get data inside the file
            if domains == '':                       #If domain file is empty string, meaning no domains
                domain_file.close()                 #Close file
                ErrorHandling().raise_error('No domains to update','Please add a domain.','Domain Error') #Raise error
                return                              #Return
            else:
                for domain in domains.split('\n'):      #For domains seperated by new lines
                    if domain != '':                    #Ignore the domain if its and empty string
                        domain_array.append(domain)     #Append to array if its not empty string
                domain_file.close()                     #Close the domains file
        public_ip = IPAddress().get_public_ip_string()  #Get the public ip of the host machine
        token = DNSconfigs().retrieve_dns_token()       #Retrieve dns token for file
        if token == '':                                 #If token is empty string, meaning no token present
            ErrorHandling().raise_error('DuckDNS Token not found.','Please add a token.','Token Error') #Raise error
            return                                  #Return
        else:
            for domain in domain_array:                     #For each domain
                request_data = {
                    "domains": [domain],                    #Domain
                    "token": token,                         #Token
                    "ip": public_ip,                        #Public ip string
                }
                web_reponse = requests.get("https://www.duckdns.org/update", request_data) #Send post request with the data
                if web_reponse.text != 'OK':                                                #If the web response is invalid
                    ConsoleWindow().log_to_console(f'Failed to update domain: {domain}!')   #Log that domain could not be updated
                    ErrorHandling().raise_error('Failed to update domain.', 'Check your token or domain name.','DNS Update Failed')    #Notify user
                    return                                                                  #Return to other function
                ConsoleWindow().log_to_console(f'Updated {domain} to {public_ip}') #Log event to console window
            Notifications().raise_notification('Domains have been updated', 'Success') #Notify user when process is finished