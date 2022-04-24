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
import os

from PyQt5 import QtCore,QtWidgets
from core.utils.file_paths import DSFilePath,ClientPath
from core.Qt5.icons import IconObj,ImageObj
from core.logging.logging import LoggingUtilitys
from core.builder.utils.encryption import Scrambler
from core.utils.utils import Notifications

from PIL import Image

class Ui_image_data_window(object):

    #Function will get the size of the screenshot to define the borders of the window
    def get_image_size(self):
        image = Image.open(DSFilePath().streaming_frame)        #Create image object
        self.width, self.height = image.size                    #Capture width and height of image object

    #Function will save a file to the image_data directory with a random string for the name
    def save_raw_file(self):
        file_path = f'{ClientPath().image_data_dir}{Scrambler().scrambleVar(7)}.jpg'
        original_image_data = LoggingUtilitys().receive_file_bytes(DSFilePath().streaming_frame)
        LoggingUtilitys().write_bytes_to_file(file_path,original_image_data)
        #os.remove(DSFilePath().streaming_frame)
        Notifications().raise_notification(
            f'Saved file as {file_path}',
            'Success'
        )

    def setupUi(self, Dialog):
        """
        Initialize UI parameters
        """
        Dialog.setObjectName("ss_window")
        Dialog.setWindowIcon(IconObj().screenshot_icon)
        """
        Get the image size, resize the window to the size of the photo
        and set the style sheet to the photo from the client
        """
        self.get_image_size()
        Dialog.resize(self.width,self.height)
        Dialog.setStyleSheet(f"background-image: url({DSFilePath().streaming_frame});")
        """
        Create menu bar for window
        """
        self.menu_bar = QtWidgets.QMenuBar(Dialog)
        self.menu_bar.setGeometry(QtCore.QRect(0,0,self.width,24))
        self.menu_bar.setObjectName('menu_bar')
        self.save_file = QtWidgets.QAction(Dialog,triggered=lambda: self.save_raw_file())
        self.save_file.setObjectName('save_file')
        self.menu_bar.addAction(self.save_file)
        """
        Finish setting up UI
        """
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.save_file.setText(_translate("ss_window", "Save"))
        Dialog.setWindowTitle(_translate("ss_window", "Image Data"))
