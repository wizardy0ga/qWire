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
# Build:  1.0.23
# -------------------------------------------------------------
from cryptography.fernet import Fernet
from core.logging.logging import NetworkingConfigs

class Encryption:
    # Function will generate a new encryption key and return it
    def create_encryption_key(self):
        key = Fernet.generate_key()     #Generate key
        return key                      #Return key

    # Function will take key and data, encrypt the data and return the encrypted data value
    def encrypt_data(self, key, data_to_encrypt):
        crypter_object = Fernet(key)                            #Create crypter object
        encoded_data = data_to_encrypt.encode()                 #Encode input data
        encrypted_data = crypter_object.encrypt(encoded_data)   #Encrypt data
        NetworkingConfigs().write_data_length(len(encrypted_data)) #Record length of data for data txrx on gui
        return encrypted_data                                   #Return the data

class Decryption:
    # Function will take key and data, decrypt the data and return the decrypted data value
    def decrypt_data(self, key, data_to_decrypt):
        if data_to_decrypt != b'':                     #Make sure data is not an empty byte string as it will throw a token error if it trys to decrypt empty byte string
            crypter_object = Fernet(key)                                #Create crypter obj
            NetworkingConfigs().write_data_length(len(data_to_decrypt)) #Record length of data for data txrx on gui
            decrypted_data = crypter_object.decrypt(data_to_decrypt)    #Decrypt data
            plaintext = decrypted_data.decode()                         #Decode the data
            return plaintext                                            #Return plaintext