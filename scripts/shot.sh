#!/bin/bash
# Captura headless del juego. uso: shot.sh "<query>" out.png [virtual_time_ms]
cd /home/omarchy/Projects/pj-vibe-game
python3 -m http.server 8089 >/dev/null 2>&1 &
PID=$!
sleep 1
timeout 120 chromium --headless=new --disable-gpu --window-size=960,540 --virtual-time-budget=${3:-3000} --screenshot="$2" "http://127.0.0.1:8089/?$1" >/dev/null 2>&1
kill $PID 2>/dev/null
