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
from PyQt5 import QtCore, QtWidgets
from ..Qt5.icons import IconObj
from ..logging.logging import DNSconfigs

class Ui_domains_window(object):

    def __init__(self):
        self.current_domains = DNSconfigs().retrieve_dns_domains() #Current domains array

    #Function will remove item from domains list and domains.txt file
    def remove_domain_from_list(self):
        domain = self.domains_list.takeItem(self.domains_list.currentRow()).text() #Get the domain from the selected row on button press
        DNSconfigs().remove_domain_from_file(domain)                               #Remove array from the configs file

    #Function will add domain to the domains file
    def add_domain_to_file(self,domain):
        self.domains_list.addItem(domain)           #Add domain to domains list gui
        DNSconfigs().add_domain_to_file(domain)     #Add the domain to the domain file
        self.new_domain_input.clear()               #Clear the domain input bar

    def setupUi(self, domains_window):
        domains_window.setObjectName("domains_window")
        domains_window.resize(282, 247)
        domains_window.setWindowIcon(IconObj().duck_dns_icon)
        self.domains_list = QtWidgets.QListWidget(domains_window)
        self.domains_list.setGeometry(QtCore.QRect(0, 10, 281, 171))
        self.domains_list.setObjectName("domains_list")
        for domain in self.current_domains:             #get domains in the domain array
            self.domains_list.addItem(domain)           #append the array to the domains list
        self.new_domain_input = QtWidgets.QLineEdit(domains_window)
        self.new_domain_input.setGeometry(QtCore.QRect(0, 210, 201, 31))
        self.new_domain_input.setObjectName("new_domain_input")
        self.add_domain_button = QtWidgets.QPushButton(domains_window,clicked=lambda: self.add_domain_to_file(self.new_domain_input.text()))
        self.add_domain_button.setGeometry(QtCore.QRect(210, 210, 31, 31))
        self.add_domain_button.setObjectName("add_domain_button")
        self.del_domain_button = QtWidgets.QPushButton(domains_window,clicked=lambda: self.remove_domain_from_list())
        self.del_domain_button.setGeometry(QtCore.QRect(250, 210, 31, 31))
        self.del_domain_button.setObjectName("del_domain_button")

        self.retranslateUi(domains_window)
        QtCore.QMetaObject.connectSlotsByName(domains_window)

    def retranslateUi(self, domains_window):
        _translate = QtCore.QCoreApplication.translate
        domains_window.setWindowTitle(_translate("domains_window", "DNS Domains"))
        self.add_domain_button.setText(_translate("domains_window", "+"))
        self.del_domain_button.setText(_translate("domains_window", "-"))