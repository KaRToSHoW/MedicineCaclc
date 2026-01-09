#!/bin/bash

# Start both Metro Bundler and Web Proxy Server concurrently

# Set backend API port for frontend config
export APP_PORT=8000

# Start Metro Bundler in background
echo "🚀 Starting Metro Bundler on port 3001..."
./scripts/start-expo.sh > /tmp/metro.log 2>&1 &
METRO_PID=$!

# Wait for Metro to be ready
echo "⏳ Waiting for Metro Bundler to start..."
for i in {1..30}; do
  if curl -s http://localhost:3001 > /dev/null 2>&1; then
    echo "✅ Metro Bundler is ready on port 3001"
    break
  fi
  sleep 1
done

# Start Web Proxy Server
echo "🌐 Starting Web Proxy Server on port 3000..."
node scripts/web-proxy-server.js &
PROXY_PID=$!

# Wait for proxy to be ready
sleep 2
if curl -s http://localhost:3000 > /dev/null 2>&1; then
  echo "✅ Web Proxy Server is ready on port 3000"
else
  echo "❌ Failed to start Web Proxy Server"
  kill $METRO_PID $PROXY_PID 2>/dev/null
  exit 1
fi

# Keep running and forward signals
echo ""
echo "═══════════════════════════════════════════"
echo "  🏥 Медицинский Калькулятор"
echo "═══════════════════════════════════════════"
echo "  📱 Metro Bundler:  http://localhost:3001"
echo "  🌐 Web Interface:  http://localhost:3000"
echo "═══════════════════════════════════════════"
echo ""
echo "Press Ctrl+C to stop all servers"

# Cleanup on exit
trap "echo '\n🛑 Stopping servers...'; kill $METRO_PID $PROXY_PID 2>/dev/null; exit" INT TERM

# Wait for processes
wait
