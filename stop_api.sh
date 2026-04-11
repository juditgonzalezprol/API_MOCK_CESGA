#!/usr/bin/env bash
# stop_api.sh  —  Para la API y el tunnel
pkill -f "uvicorn app.main:app" 2>/dev/null && echo "API parada" || echo "API no estaba corriendo"
pkill -f "cloudflared tunnel" 2>/dev/null && echo "Tunnel parado" || echo "Tunnel no estaba corriendo"
