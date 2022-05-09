<p align="center">
  <img
       src = "https://user-images.githubusercontent.com/90923369/158807109-8ddabced-898a-47a8-bb50-99c519515d50.png"
   >
</p>  

# qWire  
A Remote Access Kit for Windows.

# About qWire
qWire is a remote access kit for Windows. The purpose of this project is to work on my skills related to coding and explore the different ways remote access software can be put together. This project uses a basic client-server model. The code has been commented to the best of my ability at the time of creation as
I have found it's near impossible to remember what your code does after stepping away from a project for a certain period of time.

# How to setup qWire
Setup instructions will not be provided on this repository. The code is posted for educational purposes only. If you the reader would like to set up qWire, you are free to do so at your own will. Reading through the source code will help you understand how the program works.

# Support
This software is provided "as-is" with no support to the end user. The end user is free to modify the software as they see fit. Requests for support will not be fulfilled.

# Legal Notice
If you're looking for an open-source project to abuse, Look elsewhere. The author of qWire is not responsible for the illicit use of this program. As stated above, there is no support provided for this program. If you use or modify this code to attack computer systems, that is entirely on you. The author does not support, condone or encourage the illicit use of this software. Any attempts to do so are strongly discouraged by the author. This project is for educational purposes only.

# Environment
Created with Python 3.9.X  

Client tested on:  
* Windows 10 x64
* Windows 7 Ultimate SP1 x64

Server tested on:  
* Debian 

# Features at release 1.0.0
* Power Management (Shutdown/Reboot)
* Python Meterpreter Shell
* PowerShell Shell
* Screenshot
* BSoD
* Simple Networking (Disconnect/Reconnect/Ping)
* Encrypted Communications
* Hardcoded enumeration command
* DNS Update (Via DuckDNS)
* Multi Client Server
* Agent Builder (Compiler not included)
* GUI Application (qt)

# Update 1.0.1
* Added discord notifications option via discord server webhook
* Reconfigured controller buttons to become menu buttons in the top left of the main GUI
* Added update log to keep track of what has been done to the program
* Increased verbosity of the Console Log Window
* Added "Task Manager" to client menu in Enumeration > Task Manager
* Encryption iterations for agent builder now configurable in settings
* Main window now dispalys build number ex: qWire CnC Build: 101
* Agent variable length is now configurable in Settings > Builder > Variable Length

# Update 1.0.2
* Fixed various bugs related to the network interface
* Various other bug fixes
* Re-arranged main gui widgets
* Main gui now has a maximum size
* Connection & Task Manager widgets will now highlight the entire row
* Added meterpreter shellcode injector in the Task Manager 
* Added x64/Reverse TCP payload to injector
* Added CMD Shell to Shells > System Shells

# Update 1.0.21
* Re-organized code for GUI's
* Re-structured some of the file hierarchy around the builder and the GUI's
* Added webcam snapshot feature to surveillance
* Re-Structured Surveillance menu.
    * Surveillance > Desktop > Screenshot
    * Surveillance > Webcam > Snapshot
* Various code optimizations
* Fixed issue with agent disconnecting when server shuts down during initial handshake

# Update 1.0.22
* Tested agent on Windows 7 Ultimate SP1. Working. 
* Re-coded task manager on client and server
* Optimized context menu code. Menu now loads instantly
* Tested powershell reg key peristence on Windows 7. Working.
* Created python injector in Task Manager. Can inject python code into process's.
* Added CMD, PS and Python Meterpreter shells to the python injector

# Update 1.0.23
* Created elevation module for the agent
    * Elevation > UAC > [modules]
* Added eventvwr and compmgmt to elevation modules