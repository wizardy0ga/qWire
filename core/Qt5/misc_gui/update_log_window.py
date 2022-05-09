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
from core.Qt5.icons import IconObj
from core.utils.file_paths import BGPath


BUILD_100 = ['Build 1.0.0',
            'March 18th, 2022',
            'Initial release of qWire version 1.0.0']

BUILD_101 = ['Build 1.0.1',
             'March 30th, 2022',
             'Added discord notifications option via discord server webhook',
             'Reconfigured controller buttons to become menu buttons in the top left of the main GUI',
             'Added update log to keep track of what has been done to the program',
             'Increased verbosity of the Console Log Window',
             'Added "Task Manager" to client menu in Enumeration > Task Manager',
             'Encryption iterations for agent builder now configurable in settings',
             'Main window now dispalys build number ex: qWire CnC Build: 101',
             'Agent variable length is now configurable in Settings > Builder > Variable Length']

BUILD_102 = ['Build 1.0.2',
             'April 12th, 2022',
             'Fixed various bugs related to the network interface',
             'Other bug fixes',
             'Re-arranged main gui widgets. Main gui now has a maximum size',
             'Connection & Task Manager widgets will now highlight the entire row when an item is clicked',
             'Added meterpreter shellcode injector in the Task Manager',
             'Added x64/Reverse TCP payload to injector',
             'Added CMD Shell to Shells > System Shells']


BUILD_1021 = ['Build 1.0.21',
              'April 23rd 2022',
              're-organized code for GUI\'s',
              'Re-structured some of the file hierarchy around the builder and the GUI\'s',
              'Added webcam snapshot feature to surveillance',
              'Re - Structured Surveillance menu',
              '    Surveillance > Desktop > Screenshot',
              '    Surveillance > Webcam > Snapshot',
              'Various code optimizations',
              'Fixed issue with agent disconnecting when server shuts down during initial handshake'
              ]

BUILD_1022 = ['Build 1.0.22',
              'April 27th, 2022',
              'Tested agent on Windows 7 Ultimate SP1',
              'Re-coded task manager on client and server',
              'Optimized context menu code. Menu now loads instantly',
              'Test powershell reg key peristence on Windows 7. Working.',
              'Added python injector to Task Manager',
              'Added CMD, PS and Meterpreter shells to python injector']

BUILD_1023 = ['Build 1.0.23',
              'May 9th, 2022',
              'Created elevation module for agent.',
              '    Elevation > UAC > [exploits]',
              'Created two UAC elevation modules. Compmgmt & Eventvwr.',
              ]

MASTER_ARRAY = [BUILD_100,
                BUILD_101,
                BUILD_102,
                BUILD_1021,
                BUILD_1022,
                BUILD_1023]

class Ui_update_log_window(object):

    #Function will generate banner string with release date and build version
    def generate_version_banner(self,build_version,release_date):
        banner = f"""##########################################
{build_version}|-|-|-|-|-|-|-|{release_date}
##########################################"""
        return banner

    #Function will append banner for each update array and add the updates in the array under the banner
    def record_updates_to_log(self,updates_array):
        for array in updates_array:                                         #For update array in master array
            banner = self.generate_version_banner(array[0],array[1])        #Generate banner with build and date as first and second indeces in array
            for line in banner.split('\n'):                                 #For each line in banner split by new line
                self.update_log_widget.addItem(line)                        #Add line
            for update in array[2:]:                                        #For each update in the update array that is past the second index
                update_item = QtWidgets.QListWidgetItem(IconObj().sync_icon,update) #Create item obj with icon
                self.update_log_widget.addItem(update_item)                      #Log the update

    def setupUi(self, update_log_window):
        """
        Initialize UI parameters
        """
        update_log_window.setObjectName("update_log_window")
        update_log_window.resize(877, 565)
        update_log_window.setWindowIcon(IconObj().sync_icon)
        """
        Create widget objects
        """
        self.update_log_widget = QtWidgets.QListWidget(update_log_window)
        """
        Set widget geometry
        """
        self.update_log_widget.setGeometry(QtCore.QRect(10, 10, 861, 551))
        """
        Set widget object names
        """
        self.update_log_widget.setObjectName("update_log_widget")
        """
        Finish setting up UI
        """
        self.update_log_widget.setStyleSheet(f"background-image: url({BGPath().black_box});")
        self.record_updates_to_log(MASTER_ARRAY)
        self.retranslateUi(update_log_window)
        QtCore.QMetaObject.connectSlotsByName(update_log_window)

    def retranslateUi(self, update_log_window):
        _translate = QtCore.QCoreApplication.translate
        update_log_window.setWindowTitle(_translate("update_log_window", "Update Log"))
