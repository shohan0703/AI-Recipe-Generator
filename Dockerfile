FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# ১. প্রয়োজনীয় সিস্টেম প্যাকেজ এবং Tkinter ইনস্টল
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    fluxbox \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ২. পাইথন ডিপেন্ডেন্সি ইনস্টল
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# ৩. প্রজেক্টের বাকি সকল ফাইল কপি করা
COPY . .

# ৪. Render-এর জন্য ডিফল্ট পোর্ট
EXPOSE 10000

# ৫. Virtual Display, VNC এবং Web Server চালু করার কমান্ড
CMD Xvfb :99 -screen 0 1280x800x24 & \
    sleep 2 && \
    fluxbox & \
    python3 main.py & \
    x11vnc -display :99 -forever -shared -rfbport 5900 & \
    websockify --web=/usr/share/novnc/ 10000 localhost:5900
