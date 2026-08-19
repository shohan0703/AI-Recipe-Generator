#!/bin/bash

# Virtual Framebuffer চালু
Xvfb :99 -screen 0 1280x800x24 &
sleep 2

# Window Manager চালু
fluxbox &
sleep 1

# আপনার Python GUI অ্যাপ চালু
python3 main.py &
sleep 1

# VNC Server চালু
x11vnc -display :99 -forever -shared -rfbport 5900 &
sleep 1

# Web Proxy (noVNC) চালু
websockify --web=/usr/share/novnc/ 10000 localhost:5900 --default-path=vnc.html
