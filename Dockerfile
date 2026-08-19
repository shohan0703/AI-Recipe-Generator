FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# প্রয়োজনীয় সিস্টেম প্যাকেজ ও Tkinter ইনস্টল
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-tk \
    xvfb \
    x11vnc \
    novnc \
    websockify \
    fluxbox \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ফাইল কপি ও ডিপেন্ডেন্সি ইনস্টল
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

# noVNC পোর্ট ৭৮৬০ (Hugging Face-এর ডিফল্ট পোর্ট)
EXPOSE 7860

# Virtual Display এবং noVNC চালু করার স্টার্টআপ স্ক্রিপ্ট
CMD Xvfb :99 -screen 0 1280x800x24 & \
    sleep 2 && \
    fluxbox & \
    python3 main.py & \
    x11vnc -display :99 -forever -shared -rfbport 5900 & \
    /usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 7860