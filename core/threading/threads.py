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
import threading
from PyQt5 import QtCore

#Thread for running background tasks. Qt does not run well with the pythons threading libs
class ProcessRunnable(QtCore.QRunnable):
    def __init__(self, target, args):
        QtCore.QRunnable.__init__(self)
        self.t = target
        self.args = args

    def run(self):
        self.t()

    def start(self):
        QtCore.QThreadPool.globalInstance().start(self)

class MultiThreading():
    #Function will create a thread for functions with no arguments
    def create_background_thread(self,function):
        thread = threading.Thread(target=function)
        thread.daemon = True
        thread.start()

    #Function will create a thread for functions that take a single argument
    def create_background_thread_arg(self,function,argument):
        arguments = [argument]
        thread = threading.Thread(target=function,args=arguments)
        thread.daemon = True
        thread.start()

    #Function will create a thread for functions with two arguments
    def create_background_thread_arg_arg(self,function,arg1,arg2):
        arguments = [arg1,arg2]
        thread = threading.Thread(target=function,args=arguments)
        thread.daemon = True
        thread.start()