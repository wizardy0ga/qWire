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
from PyQt5 import QtCore, QtGui, QtWidgets
from ..logging.logging import ConsoleWindow,LoggingUtilitys
from ..Qt5.duck_dns_token_window import Ui_dns_token_window
from ..Qt5.domains_window import Ui_domains_window
from ..Qt5.webhook_window import Ui_webhook_dialog
from ..Qt5.icons import IconObj
from ..utils.utils import Validation,Notifications, ErrorHandling
from ..utils.file_paths import BGPath,CFGFilePath
from ..logging.logging import NetworkingConfigs,DNSconfigs,DiscordCFG
from ..networking.IP_Handler import NicHandler

class Ui_settings_window(object):

    #Function will update the encryption iterations function for the builder
    def set_encryption_iterations(self):
        iteration_count = self.iteration_rounds_input.text()                #Get user input from box
        if Validation().validate_integer(iteration_count) == True:          #If the validation returns true
            LoggingUtilitys().write_data_to_file(CFGFilePath().iterations_file,     #Log the data
                                                     str(iteration_count))
            Notifications().raise_notification(f'Updated encryption iteration count to {str(iteration_count)}', #Raise notification
                                                   'Success')
            ConsoleWindow().log_to_console(f'Updated encryption iteration count to {str(iteration_count)}') #Log to console
        else:                                                   #Else if validation returns false and data is not integer
            ErrorHandling().raise_error('iteration count must be integer',      #Raise error
                                      '',
                                      'Invalid Data Type')
            ConsoleWindow().log_to_console('Could not update iteration count for crypter') #Log to console

    #Function will set the variable length for the agent builder
    def set_variable_length(self):
        var_len = self.var_len_input.text()                     #Get the value of the variable length box
        if Validation().validate_integer(var_len) == True:      #If the validation function returns true
            LoggingUtilitys().write_data_to_file(CFGFilePath().var_len_file,str(var_len))   #Log the value
            Notifications().raise_notification(f'Updated variable length to {var_len}',     #Raise notification
                                               'Success')
            ConsoleWindow().log_to_console(f'Updated agent variable length to {var_len}')   #Log to console
        else:                                                   #Else if the validation returns false,
            ErrorHandling().raise_error('Variable length must be integer',                  #Raise error
                                        '',
                                        'Invalid Data Type')
            ConsoleWindow().log_to_console('Could not update agent variable length')        #Log to console

    #Function will change the stream port
    def change_stream_port(self):
        port = self.stream_port_input.text()                #Get port
        if Validation().Validate_port_number(port):         #if the port is valid
            NetworkingConfigs().write_stream_port(port)     #write the port
            Notifications().raise_notification(f'Updated streaming port to {port}','Success')   #Notify the user
            ConsoleWindow().log_to_console(f'Client stream port updated to {port}')             #Log to console

    #Function will change the exfiltration port
    def change_exfil_port(self):
        port = self.exfil_port_input.text()                 #Get port
        if Validation().Validate_port_number(port):         #If the port is valid
            NetworkingConfigs().write_exfil_port(port)      #Write the port
            Notifications().raise_notification(f'Updated exfiltration port to {port}','Success')    #Notify user
            ConsoleWindow().log_to_console(f'Client exfiltration port updated to {port}')


    #Function will validate given port and write it to the file if the function returns true
    def change_shell_port(self):
        port = self.shell_port_input.text()                    #Get the text in the box
        if Validation().Validate_port_number(port):            #Validate it. If port is valid
            NetworkingConfigs().write_shell_lport(port)        #write the port
            Notifications().raise_notification(f'Updated shell port to {port}','Success')  #Notify user
            ConsoleWindow().log_to_console(f'Client shell port updated to {port}')         #Log to console

    #Function will change the shell domain for powershell and meterpreter shells
    def change_host_domain(self):
        host = NicHandler().validate_host(self.host_combobox.currentText())#Get the current text from domain combo box
        if host == '':                                                     #If the host is an empty string,
            ErrorHandling().raise_error('Could not update host IP/Domain',   #Raise an error
                                      'Invalid host string',
                                      'Host Error')
            ConsoleWindow().log_to_console('Error updating client shell connection string') #Log to console
        else:
            DNSconfigs().write_shell_domain(host)                #Write the domain to the shell config file
            Notifications().raise_notification(f'Updated shell host to {host}','Success')   #Inform user
            ConsoleWindow().log_to_console(f'Changed shell host to {host}')                 #Log event to console

    #Function will change the network interface that the server operates on
    def change_network_interface(self):
        interface = self.nic_combo_box.currentText()                #Retrieve interface
        NetworkingConfigs().write_network_interface(interface)      #Write interface to the config file
        Notifications().raise_notification(f'Updated network interface to {interface}','Success') #Notify user
        ConsoleWindow().log_to_console(f'Updated network interface for server to {interface}') #Log event

    #Function will turn discord notifications on/off
    def set_discord_notification(self):
        choice = self.enable_discord_combobox.currentText()         #Get choice from combobox

        if DiscordCFG().retrieve_webhook() != '':                   #If the webhook file does not contain empty string
            DiscordCFG().set_discord_notification(choice)               #Set the choice in the notification file
            Notifications().raise_notification(f'Discord notifications are now {choice}','Success') #Notify user
            ConsoleWindow().log_to_console(f'Discord notifications are now {choice}') #Log event to console

        else:                                                       #Else if webhook file is empty string,
            ErrorHandling().raise_error('Invalid Webhook',
                                        'Webhook can not be empty string.\n\nCould not enable discord notifications',
                                        'Webhook Error')             # Raise Error
            DiscordCFG().set_discord_notification('Disabled')        # Set notifications to disabled
            self.enable_discord_combobox.setCurrentText('Disabled')  # Return the combobox to disabled setting
            ConsoleWindow().log_to_console('Webhook error. Discord notifications disabled.') #Log event to console

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
        self.callback_groupbox = QtWidgets.QGroupBox(self.logging_tab)
        self.callback_groupbox.setGeometry(QtCore.QRect(10, 10, 171, 111))
        self.callback_groupbox.setObjectName("callback_groupbox")
        self.clear_logs_button = QtWidgets.QPushButton(self.callback_groupbox,
                                                       clicked=lambda: ConsoleWindow().clear_console_logs())
        self.clear_logs_button.setGeometry(QtCore.QRect(10, 30, 151, 31))
        self.clear_logs_button.setObjectName("clear_logs_button")
        self.discord_groupbox = QtWidgets.QGroupBox(self.logging_tab)
        self.discord_groupbox.setGeometry(QtCore.QRect(10, 140, 171, 121))
        self.discord_groupbox.setObjectName("discord_groupbox")
        self.webhook_button = QtWidgets.QPushButton(self.discord_groupbox,clicked=lambda: self.open_new_window(Ui_webhook_dialog))
        self.webhook_button.setGeometry(QtCore.QRect(30, 90, 101, 27))
        self.webhook_button.setObjectName("webhook_button")
        self.enable_discord_combobox = QtWidgets.QComboBox(self.discord_groupbox)
        self.enable_discord_combobox.setGeometry(QtCore.QRect(8, 30, 151, 27))
        self.enable_discord_combobox.setObjectName("comboBox")
        self.enable_discord_combobox.addItem('Disabled')
        self.enable_discord_combobox.addItem('Enabled')
        self.enable_discord_combobox.setCurrentText(DiscordCFG().get_setting_string())
        self.update_discord_button = QtWidgets.QPushButton(self.discord_groupbox,clicked=lambda: self.set_discord_notification())
        self.update_discord_button.setGeometry(QtCore.QRect(30, 60, 101, 27))
        self.update_discord_button.setObjectName("update_discord_combobox")
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
        self.builder_tab = QtWidgets.QWidget()
        self.builder_tab.setObjectName("builder_tab")
        self.encryption_groupbox = QtWidgets.QGroupBox(self.builder_tab)
        self.encryption_groupbox.setGeometry(QtCore.QRect(10, 10, 141, 101))
        self.encryption_groupbox.setObjectName("encryption_groupbox")
        self.iterations_label = QtWidgets.QLabel(self.encryption_groupbox)
        self.iterations_label.setGeometry(QtCore.QRect(10, 30, 71, 19))
        self.iterations_label.setObjectName("iterations_label")
        self.iteration_rounds_input = QtWidgets.QLineEdit(self.encryption_groupbox)
        self.iteration_rounds_input.setGeometry(QtCore.QRect(80, 30, 51, 27))
        self.iteration_rounds_input.setObjectName("iteration_rounds_input")
        self.iteration_rounds_input.setText(LoggingUtilitys().retrieve_file_data(
            CFGFilePath().iterations_file
        ))
        self.update_iterations_button = QtWidgets.QPushButton(self.encryption_groupbox,clicked=lambda: self.set_encryption_iterations())
        self.update_iterations_button.setGeometry(QtCore.QRect(80, 60, 51, 27))
        self.update_iterations_button.setObjectName("update_iterations_button")
        self.var_length_groupbox = QtWidgets.QGroupBox(self.builder_tab)
        self.var_length_groupbox.setGeometry(QtCore.QRect(170, 10, 161, 101))
        self.var_length_groupbox.setObjectName("var_length_groupbox")
        self.update_var_len_button = QtWidgets.QPushButton(self.var_length_groupbox,clicked=lambda: self.set_variable_length())
        self.update_var_len_button.setGeometry(QtCore.QRect(100, 60, 51, 27))
        self.update_var_len_button.setObjectName("update_var_len_button")
        self.var_len_input = QtWidgets.QLineEdit(self.var_length_groupbox)
        self.var_len_input.setGeometry(QtCore.QRect(100, 30, 51, 27))
        self.var_len_input.setObjectName("var_len_input")
        self.var_len_input.setText(LoggingUtilitys().retrieve_file_data(CFGFilePath().var_len_file))
        self.var_len_label = QtWidgets.QLabel(self.var_length_groupbox)
        self.var_len_label.setGeometry(QtCore.QRect(30, 30, 51, 19))
        self.var_len_label.setObjectName("var_len_label")
        self.settings_tabs.addTab(self.builder_tab, "")
        self.retranslateUi(settings_window)
        self.settings_tabs.setCurrentIndex(0) #Pick which tab to open the settings window on
        QtCore.QMetaObject.connectSlotsByName(settings_window)

    def retranslateUi(self, settings_window):
        _translate = QtCore.QCoreApplication.translate
        settings_window.setWindowTitle(_translate("settings_window", "qWire Settings"))
        self.callback_groupbox.setTitle(_translate("settings_window", "Callback Window"))
        self.clear_logs_button.setText(_translate("settings_window", "Clear Console Logs"))
        self.discord_groupbox.setTitle(_translate("settings_window", "Discord Notifications"))
        self.webhook_button.setText(_translate("settings_window", "Webhook"))
        self.update_discord_button.setText(_translate("settings_window", "Update"))
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
        self.encryption_groupbox.setTitle(_translate("settings_window", "Encryption"))
        self.iterations_label.setText(_translate("settings_window", "Iterations"))
        self.settings_tabs.setTabText(self.settings_tabs.indexOf(self.builder_tab),
                                      _translate("settings_window", "Builder"))
        self.update_iterations_button.setText(_translate("settings_window", "Update"))
        self.var_length_groupbox.setTitle(_translate("settings_window", "Variable Length"))
        self.update_var_len_button.setText(_translate("settings_window", "Update"))
        self.var_len_label.setText(_translate("settings_window", "Length"))