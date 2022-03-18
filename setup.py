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
from subprocess import run
from core.utils.file_paths import CFGFilePath
from core.utils.file_paths import DSFilePath

import argparse

#Define graphic string
graphic_string = """
   ._________________.
   |.---------------.|
   ||  qWire Setup  ||
   ||   -._ .-.     ||
   ||   -._| | |    ||
   ||   -._|"|"|    ||
   ||   -._|.-.|    ||
   ||_______________||
   /.-.-.-.-.-.-.-.-.\\
  /.-.-.-.-.-.-.-.-.-.\\
 /.-.-.-.-.-.-.-.-.-.-.\\
/______/__________\_____\\
\_______________________/\n"""

#Define desciption string
description_string = """------------------------------------------------------------------------
qWire setup script. Use 'python3 setup.py -h' for options else,
run 'python3 setup.py' to run everything automatically. 
The setup script is currently configured for the aptitude package manager. 
------------------------------------------------------------------------
[+] Author: Slizbinksman
[+] Github: https://github.com/slizbinksman
------------------------------------------------------------------------"""

#Define package manager array
package_array = ['python3-pip',
                 'gnome-terminal']


#Define array of librarys
library_array = ['cryptography',
                 'notify2',
                 'playsound',
                 'pyqt5',
                 'pillow',
                 'requests',
                 'netifaces']

#Define cfg files array
conifguration_files = [CFGFilePath().domains_file,
                       CFGFilePath().stream_port_file,
                       CFGFilePath().exfil_port_file,
                       CFGFilePath().server_sockets,
                       CFGFilePath().dns_token,
                       CFGFilePath().current_interface,
                       CFGFilePath().chosen_domain,
                       CFGFilePath().shells_lport_file]

#Define data storage files array
data_storage_files = [DSFilePath().active_connections_file,
                      DSFilePath().bits_file,
                      DSFilePath().listening_sockets_file,
                      DSFilePath().console_output_file]


#Function will make a blank copy of required text files
def setup_files(file_array):
    for file in file_array:
        with open(file, 'w') as new_file:
            new_file.close()
        print(f'[+] Created new file: {file}')

#Function will insatll a library with various commands passed as a parameter
def install_library(command,array):
    for lib in array:
        run(f'{command} {lib}',shell=True)

#Main
if __name__ == '__main__':
    #Create arguments for script
    parser = argparse.ArgumentParser(description=f'{graphic_string}{description_string}',formatter_class=argparse.RawTextHelpFormatter)
    installer = parser.add_argument_group('Installer Actions')
    installer.add_argument('--files',action='store_true',help='Create setup files')
    installer.add_argument('--pip',action='store_true',help='Install python library\'s')
    installer.add_argument('--packages',action='store_true',help='Install linux based packages via apt')
    args = parser.parse_args()
    #If files arg is true,create/overwrite current cfg files
    if args.files:
        setup_files(conifguration_files)
        setup_files(data_storage_files)
        exit()
    #If pip arg is true, install librarys from array
    if args.pip:
        install_library('pip install',library_array)
        exit()
    #If packages arg is true, install packages from array
    if args.packages:
        install_library('sudo apt install -y',package_array)
        exit()
    #If nothing is selected at the cli
    else:
        #Install all librarys and create required files
        install_library('sudo apt install -y',package_array)
        install_library('pip install', library_array)
        setup_files(conifguration_files)
        setup_files(data_storage_files)