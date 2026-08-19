#!/bin/bash

# Virtual Framebuffer
Xvfb :99 -screen 0 1280x800x24 &
sleep 2

# Window Manager
fluxbox &
sleep 1

# VNC Server
x11vnc -display :99 -forever -shared -rfbport 5900 &
sleep 1

# Python GUI App
python3 main.py &
sleep 2

# Web Proxy (Main Foreground Process)
websockify --web=/usr/share/novnc/ 10000 localhost:5900 --default-path=vnc.html
