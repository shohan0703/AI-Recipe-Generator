FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99

# প্রয়োজনীয় প্যাকেজসমূহ ইনস্টল
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

# ডিপেন্ডেন্সি ইনস্টল
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# সব ফাইল কপি করা
COPY . .

# entrypoint.sh কে এক্সিকিউটেবল পারমিশন দেওয়া
RUN chmod +x /app/entrypoint.sh

EXPOSE 10000

# entrypoint স্ক্রিপ্ট চালানো
CMD ["/app/entrypoint.sh"]
