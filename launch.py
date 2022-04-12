#!/usr/bin/python3
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
from core.Qt5.ghost_wire_gui import Ui_main_window
from core.utils.file_paths import DSFilePath
from PyQt5 import QtWidgets
import os
import sys
import signal

class StartUp:

    #Function will clear active connections text file to remove leftover connections
    def clear_active_conns_file(self):
        file_array = [DSFilePath().active_connections_file,
                      DSFilePath().bits_file,
                      DSFilePath().listening_sockets_file]
        for file in file_array:
            with open(file,'w') as file:
                file.close()

class ShutDown:
    #Function will find the pid of the program and kill it completely. Leaves no child process's behind
    def kill_pid(self):
        pid = os.getpid()           #Get the pid of the parent process
        os.kill(pid,signal.SIGTERM) #Kill the process and all subprocess's


def launch_program():
    StartUp().clear_active_conns_file()     #Clear active conns file of old connections so the ui doesnt add false connections
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()
    ui = Ui_main_window()
    ui.setupUi(main_window)
    main_window.show()
    app.exec_()
    ShutDown().kill_pid()                   #Kill the pid of the program else it will hang after the windows closed and has to be killed manually

if __name__ == '__main__':
    launch_program()
