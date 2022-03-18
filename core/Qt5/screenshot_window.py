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
from PyQt5 import QtCore
from ..utils.file_paths import DSFilePath
from ..Qt5.icons import IconObj
from PIL import Image

class Ui_screenshot_window(object):

    #Function will get the size of the screenshot to define the borders of the window
    def get_image_size(self):
        image = Image.open(DSFilePath().streaming_frame)        #Create image object
        self.width, self.height = image.size                    #Capture width and height of image object

    def setupUi(self, Dialog):
        Dialog.setObjectName("ss_window")
        Dialog.setWindowIcon(IconObj().screenshot_icon)
        self.get_image_size()
        Dialog.resize(self.width,self.height)
        Dialog.setStyleSheet(f"background-image: url({DSFilePath().streaming_frame});")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("ss_window", "Screenshot"))
