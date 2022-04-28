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
from PyQt5 import QtCore, QtWidgets, Qt
from core.Qt5.icons import IconObj
from core.utils.file_paths import DSFilePath
from core.logging.logging import LoggingUtilitys
from os import remove

class Ui_host_info_window(object):
    def setupUi(self, host_information_window):
        """
        Initialize our UI parameters
        """
        host_information_window.setObjectName("host_information_window")
        host_information_window.resize(916, 712)
        host_information_window.setStyleSheet(f"background-color:blue;")
        host_information_window.setWindowIcon(IconObj().system_icon)
        """
        Create list object, set geometry and object name
        """
        self.host_info_list = QtWidgets.QListWidget(host_information_window)
        self.host_info_list.setGeometry(QtCore.QRect(0, 0, 921, 711))
        self.host_info_list.setObjectName("host_info_list")
        """
        Populate our window with the information from the client
        and complete the UI setup
        """
        self.display_system_info()
        self.retranslateUi(host_information_window)
        QtCore.QMetaObject.connectSlotsByName(host_information_window)

    def retranslateUi(self, host_information_window):
        _translate = QtCore.QCoreApplication.translate
        host_information_window.setWindowTitle(_translate("host_information_window", "Host Information"))
        remove(DSFilePath().sys_info_file)

    #Function will display the system info extracted from agent in gui
    def display_system_info(self):
        system_info = LoggingUtilitys().retrieve_file_data(DSFilePath().sys_info_file) #Get the sys info file written from the client
        for line in system_info.split('\n'):
            new_item = QtWidgets.QListWidgetItem(line)              #Create item object
            new_item.setBackground(Qt.Qt.transparent)               #Make background transparent
            self.host_info_list.addItem(new_item)                   #Append the item
