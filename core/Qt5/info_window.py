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
from ..utils.file_paths import BGPath
from ..Qt5.icons import IconObj
from PyQt5 import QtCore

class Ui_information_window(object):
    def setupUi(self, information_window):
        information_window.setObjectName("information_window")
        information_window.setWindowIcon(IconObj().main_window_icon)
        information_window.resize(628, 327)
        information_window.setStyleSheet(f"background-image: url({BGPath().qWire_info_bg});")

        self.retranslateUi(information_window)
        QtCore.QMetaObject.connectSlotsByName(information_window)

    def retranslateUi(self, information_window):
        _translate = QtCore.QCoreApplication.translate
        information_window.setWindowTitle(_translate("information_window", "qWire Information"))


