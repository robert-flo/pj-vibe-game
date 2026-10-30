#!/bin/bash
# Captura headless del juego. uso: shot.sh "<query>" out.png [virtual_time_ms]
cd /home/omarchy/Projects/pj-vibe-game
PORT=8091
python3 -m http.server $PORT >/dev/null 2>&1 &
PID=$!
sleep 0.5
timeout 35 chromium --headless=new --use-gl=angle --use-angle=swiftshader --enable-unsafe-swiftshader --window-size=960,540 --virtual-time-budget=${3:-2500} --screenshot="$2" "http://127.0.0.1:$PORT/?$1" >/dev/null 2>&1
kill $PID 2>/dev/null || true
