#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# deploy_local.sh  —  Levanta la API + tunnel público en un paso
# Uso: ./deploy_local.sh
# ─────────────────────────────────────────────────────────────────
set -e
cd "$(dirname "$0")"

VENV="venv"
PORT=8000

# ── 1. Activar entorno virtual ────────────────────────────────────
if [ ! -d "$VENV" ]; then
  echo "[1/4] Creando virtualenv..."
  python3 -m venv "$VENV"
  source "$VENV/bin/activate"
  pip install -q -r requirements.txt
else
  source "$VENV/bin/activate"
fi

# ── 2. Parar instancias anteriores ───────────────────────────────
echo "[2/4] Limpiando procesos anteriores..."
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "cloudflared tunnel" 2>/dev/null || true
sleep 1

# ── 3. Arrancar API en background ────────────────────────────────
echo "[3/4] Arrancando API en puerto $PORT..."
# caffeinate evita que el Mac entre en reposo mientras la API está activa
nohup caffeinate -i uvicorn app.main:app --host 0.0.0.0 --port $PORT \
  --log-level info > /tmp/cesga_api.log 2>&1 &
API_PID=$!
echo "  API PID: $API_PID"

# Esperar a que la API esté lista
for i in {1..15}; do
  if curl -sf http://localhost:$PORT/health > /dev/null 2>&1; then
    echo "  API lista ✓"
    break
  fi
  sleep 1
done

# ── 4. Arrancar tunnel público ────────────────────────────────────
echo "[4/4] Creando tunnel público (Cloudflare)..."
cloudflared tunnel --url http://localhost:$PORT --no-autoupdate \
  > /tmp/cesga_tunnel.log 2>&1 &
TUNNEL_PID=$!

# Esperar URL del tunnel
echo "  Esperando URL del tunnel..."
for i in {1..20}; do
  URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' /tmp/cesga_tunnel.log 2>/dev/null | head -1)
  if [ -n "$URL" ]; then
    break
  fi
  sleep 1
done

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  API DESPLEGADA Y ACCESIBLE EXTERNAMENTE"
echo ""
echo "  URL pública:   $URL"
echo "  URL local:     http://localhost:$PORT"
echo "  Docs:          $URL/docs"
echo "  Health:        $URL/health"
echo ""
echo "  Logs API:    tail -f /tmp/cesga_api.log"
echo "  Logs Tunnel: tail -f /tmp/cesga_tunnel.log"
echo ""
echo "  Para parar: pkill -f uvicorn; pkill -f cloudflared"
echo "═══════════════════════════════════════════════════════════════"

# Guardar PIDs
echo "$API_PID" > /tmp/cesga_api.pid
echo "$TUNNEL_PID" > /tmp/cesga_tunnel.pid

# Guardar URL en el Escritorio para fácil acceso
cat > ~/Desktop/CESGA_API_URL.txt <<URLEOF
═══════════════════════════════════════════
  CESGA API — URL PÚBLICA ACTIVA
═══════════════════════════════════════════
  URL:   $URL
  Docs:  $URL/docs

  Activa desde: $(date '+%A %d/%m/%Y %H:%M')
  Se apaga: domingo 10:00
═══════════════════════════════════════════
URLEOF

# Notificación macOS con la URL
osascript -e "display notification \"$URL\" with title \"CESGA API activa\" subtitle \"Docs: $URL/docs\" sound name \"Glass\"" 2>/dev/null || true
