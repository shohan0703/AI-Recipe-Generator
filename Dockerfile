FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99

# ১. প্রয়োজনীয় প্যাকেজ ইনস্টল
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

# ২. ডিপেন্ডেন্সি ইনস্টল
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

# ৩. Virtual Display সেট করে অ্যাপ ও noVNC চালু করা
CMD Xvfb :99 -screen 0 1280x800x24 & \
    sleep 2 && \
    fluxbox & \
    sleep 1 && \
    python3 main.py & \
    x11vnc -display :99 -forever -shared -rfbport 5900 & \
    websockify --web=/usr/share/novnc/ 10000 localhost:5900 --default-path=vnc.html
