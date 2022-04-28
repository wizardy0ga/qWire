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
from ..logging.logging import LoggingUtilitys
from PyQt5.QtGui import QIcon,QPixmap

#Create icon object with icons
class IconObj:

    def __init__(self):
        self.port_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/socket_icon.png'))
        self.system_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/computer_icon.png'))
        self.msf_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/msf_icon.png'))
        self.python_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/python_icon.png'))
        self.shells_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/shells_icon.png'))
        self.ps_shell_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/powershell_icon.png'))
        self.reconnect_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/reconnect_icon.png'))
        self.ping_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/ping_icon.png'))
        self.net_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/networking_icon.png'))
        self.bsod_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/bsod_icon.png'))
        self.shutdown_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/shutdown_icon.png'))
        self.magn_glass_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/magn_glass_icon.png'))
        self.screenshot_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/screenshot_icon.png'))
        self.surveillance_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/surveillance_icon.png'))
        self.disconnect_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/disconnect_icon.png'))
        self.builder_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/hammer_icon.png'))
        self.main_window_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/main_window_icon.png'))
        self.info_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/info_icon.png'))
        self.settings_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/settings_icon.png'))
        self.duck_dns_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/duck_dns_icon.png'))
        self.satellite_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/satellite_icon.png'))
        self.sat_win_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/satellite_win_icon.png'))
        self.sync_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/sync_icon.png'))
        self.admin_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/admin_icon.png'))
        self.discord_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/discord_logo.png'))
        self.update_log_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/update_log_icon.png'))
        self.task_manager_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/task_man_icon.png'))
        self.kill_task_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/task_kill_icon.png'))
        self.injector_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/injector_icon.png'))
        self.shellcode_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/shellcode_icon.png'))
        self.cmd_shell_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/cmd_shell_icon.png'))
        self.microsoft_logo_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/microsoft_logo.png'))
        self.windows_10_logo = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/windows_10_logo.png'))
        self.webcam_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/webcam_icon.png'))
        self.file_icon = QIcon(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/file_ex_icon.png'))


#Create image object with image file paths. This should be moved to utils/file_paths
class ImageObj:

    def __init__(self):
        self.sysinfo_win_bg_path = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/sysinfo_win_bg.jpg')
        self.grey_box = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/grey_box.jpg')
        self.gwa_ascii_art = LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/qWire_logo.png')
        self.spinning_globe_gif = LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/spinning_globe.gif') #Gif file

#Create pixmap object
class PixmapObj:
    def __init__(self):
        self.net_pixmap = QPixmap(LoggingUtilitys().get_misc_file_path_str('core/Qt5/img/networking_icon.png'))
        self.socket_pixmap = QPixmap(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/socket_icon.png'))
        self.nic_pixmap = QPixmap(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/nic_icon.png'))
        self.listener_pixmap = QPixmap(LoggingUtilitys().get_misc_file_path_str('/core/Qt5/img/satellite_icon.png'))