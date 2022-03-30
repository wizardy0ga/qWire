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
from ..utils.file_paths import BGPath
from ..Qt5.icons import IconObj
from PyQt5 import QtCore
from PIL import Image

class Ui_information_window(object):
    #Function will get the size of the screenshot to define the borders of the window
    def get_image_size(self):
        image = Image.open(BGPath().qWire_info_bg)        #Create image object
        self.width, self.height = image.size                    #Capture width and height of image object

    def setupUi(self, information_window):
        self.get_image_size()
        information_window.setObjectName("information_window")
        information_window.setWindowIcon(IconObj().main_window_icon)
        information_window.resize(self.width,self.height)
        information_window.setStyleSheet(f"background-image: url({BGPath().qWire_info_bg});")

        self.retranslateUi(information_window)
        QtCore.QMetaObject.connectSlotsByName(information_window)

    def retranslateUi(self, information_window):
        _translate = QtCore.QCoreApplication.translate
        information_window.setWindowTitle(_translate("information_window", "qWire Information"))


