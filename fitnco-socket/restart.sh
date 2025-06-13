#!/bin/bash

# Ortam değişkenlerini düzgünce ayarla
export PATH="/home/fitnco/fitnco-python/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/bin"

# Port 5005'i kullanan işlemi öldür
pid=$(lsof -ti:5005)
if [ -n "$pid" ]; then
    echo "Killing PID $pid"
    kill -9 "$pid"
fi

# 1-2 saniye bekle
sleep 2

# Sanal ortamı aktive etmeden doğrudan venv içindeki python'ı kullan
nohup /home/fitnco/fitnco-python/venv/bin/python /home/fitnco/fitnco-python/fitnco-socket/fit-socket.py >> /home/fitnco/fitnco-python/fitnco-socket/audit-socket.log 2>&1 &
