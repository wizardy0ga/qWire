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
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from playsound import playsound

import notify2
import os

class ErrorHandling():
    #Function will raise an error. Needs an icon
    def raise_error(self,error_text,error_more_information,window_title):
        msg = QtWidgets.QMessageBox()
        icon = QtGui.QIcon(f'{os.getcwd()}/core/Qt5/img/disconnect_icon.png') #Manually retrieve icon since importing causes circular import
        msg.setWindowIcon(icon)                                 #Set window icon to red x used from disconnect icon
        msg.setIcon(QtWidgets.QMessageBox.Critical)             #Set message icon
        msg.setText(error_text)                                 #Set error text
        msg.setInformativeText(error_more_information)          #Add more information to box
        msg.setWindowTitle(window_title)                        #Set window title
        msg.exec_()                                             #Show message

class Notifications():

    #Function will notify user of new connection
    def notify_new_connection(self,system_name,Location,IP_address):
        notify2.init('New Connection')      #Init notification object
        notification = notify2.Notification("New Connection",f"{system_name}\n{Location}\n{IP_address}",icon=f"{os.getcwd()}/core/Qt5/img/computer_icon.png") #Set details
        notification.show()                 #Show notification
        notification.set_timeout(3000)      #Set timeout
        playsound(f'{os.getcwd()}/core/utils/notify.wav') #Play notification sound
        notify2.uninit()                                            #Uninit the object

    #Function will raise a notification
    def raise_notification(self,notify_text,window_title):
        icon_path = os.path.join(f'{os.getcwd()}/core/Qt5/img/check_mark.png')
        icon = QtGui.QIcon(icon_path)
        notification = QtWidgets.QMessageBox()
        notification.setWindowIcon(icon)
        notification.setIcon(QtWidgets.QMessageBox.Information)
        notification.setText(notify_text)
        notification.setWindowTitle(window_title)
        notification.exec_()

class Validation():

    #Function will validate port number. Valid port will return true, invalid will return false
    def Validate_port_number(self,port_number):
        try:
            port_number = int(port_number)                                      #Check if port is an integer
            if port_number < 1 or int(port_number) > 65535:                     #If ports less than 1 or greater than 65535
                ErrorHandling().raise_error('Invalid Port Number.',             #Raise error
                                            'Port must be in range 1 - 65535.',
                                            'Bad Port Number')
                return False                                                    #Return false
            return True                                                         #Else if port is valid, return true
        except ValueError:                                                      #If port is not integer
            ErrorHandling().raise_error('Port must be integer.',                #Raise error
                                            '',
                                            'Invalid Data Type')
            return False                                                        #Return false

    #Function will validate file extention parameter
    def validate_extention(self,file_name,file_extention):
        try:
            split_file = str(file_name).split('.')  #If file name can be indexed by the .
            if split_file[1] == file_extention:     #If the 2nd index is == file extention parameter
                return True                         #return true
            return False                            #else return false
        except IndexError:                          #If their is no .
            return False                            #Return false